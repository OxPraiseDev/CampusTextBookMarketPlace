from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatRoom, Message, Report
from apps.marketplace.models import Listing

@login_required
def inbox(request):
    rooms = ChatRoom.objects.filter(buyer=request.user) | ChatRoom.objects.filter(seller=request.user)
    rooms = rooms.order_by('-created_at')
    return render(request, 'inbox.html', {'rooms': rooms})

@login_required
def start_chat(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user == listing.seller:
        messages.error(request, "You cannot chat with yourself.")
        return redirect('home')

    if listing.listing_type == 'TRADE':
        return redirect('select_trade_book', listing_id=listing.id)
        
    room, created = ChatRoom.objects.get_or_create(
        buyer=request.user, seller=listing.seller, listing=listing
    )
    return redirect('view_chat', room_id=room.id)

@login_required
def select_trade_book(request, listing_id):
    target_listing = get_object_or_404(Listing, id=listing_id)
    my_listings = Listing.objects.filter(seller=request.user, status='ACTIVE')

    if not my_listings.exists():
        messages.warning(request, "You need an active listing to offer a trade! Post a book first.")
        return redirect('home')

    if request.method == 'POST':
        offered_id = request.POST.get('offered_listing')
        offered_listing = get_object_or_404(Listing, id=offered_id, seller=request.user)
        
        room, created = ChatRoom.objects.get_or_create(
            buyer=request.user, 
            seller=target_listing.seller, 
            listing=target_listing,
            offered_listing=offered_listing
        )
        return redirect('view_chat', room_id=room.id)

    return render(request, 'select_trade.html', {'target_listing': target_listing, 'my_listings': my_listings})

@login_required
def view_chat(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # FIX: Allow Admins (is_staff) to view ANY chat for moderation
    if not request.user.is_staff and request.user != room.buyer and request.user != room.seller:
        messages.error(request, "You are not authorized to view this chat.")
        return redirect('home')
    
    # Mark messages as read (only if the user is actually a participant)
    if request.user == room.buyer or request.user == room.seller:
        Message.objects.filter(room=room, is_read=False).exclude(sender=request.user).update(is_read=True)
    
    return render(request, 'chat.html', {'room': room})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender:
        message.is_deleted = True
        message.content = "This message was deleted."
        message.file_base64 = None
        message.message_type = 'text'
        message.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
            
    return redirect('view_chat', room_id=message.room.id)

@login_required
def mark_messages_read(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user == room.buyer or request.user == room.seller:
        Message.objects.filter(room=room, is_read=False).exclude(sender=request.user).update(is_read=True)
    return JsonResponse({'status': 'ok'})

@login_required
def confirm_transaction(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    if request.user == room.buyer:
        room.buyer_confirmed = True
    elif request.user == room.seller:
        room.seller_confirmed = True
    room.save()

    if room.buyer_confirmed and room.seller_confirmed:
        room.is_completed = True
        room.save()
        room.listing.status = 'SOLD'
        room.listing.save()
        if room.offered_listing:
            room.offered_listing.status = 'SOLD'
            room.offered_listing.save()
        messages.success(request, "Transaction successfully completed!")
    else:
        messages.info(request, "You have confirmed. Waiting for the other party...")
        
    return redirect('view_chat', room_id=room.id)

@login_required
def upload_chat_file(request, room_id):
    if request.method == 'POST' and request.FILES.get('file'):
        room = get_object_or_404(ChatRoom, id=room_id)
        file = request.FILES['file']
        msg_type = 'audio' if 'audio' in file.content_type else 'image'
        
        msg = Message.objects.create(
            room=room, 
            sender=request.user, 
            file=file, 
            message_type=msg_type,
            content=""
        )
        
        channel_layer = get_channel_layer()
        recipient = room.seller if request.user == room.buyer else room.buyer
        
        async_to_sync(channel_layer.group_send)(
            f'chat_{room.id}',
            {
                'type': 'chat_message',
                'message': "", 
                'username': request.user.username,
                'msg_id': str(msg.id),
                'file_url': msg.file.url,
                'message_type': msg.message_type
            }
        )
        
        async_to_sync(channel_layer.group_send)(
            f"user_{recipient.id}",
            {
                'type': 'send_notification',
                'sender': request.user.username,
                'room_id': str(room.id),
                'content': f"Sent an {msg_type}",
                'book_title': room.listing.book.title
            }
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def submit_report(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, id=room_id)
        reason = request.POST.get('reason')
        reported_user = room.seller if request.user == room.buyer else room.buyer
        
        Report.objects.create(
            room=room,
            reporter=request.user,
            reported_user=reported_user,
            reason=reason
        )
        messages.error(request, "Your report has been submitted to the Admin. We will review this chat.")
        return redirect('view_chat', room_id=room.id)