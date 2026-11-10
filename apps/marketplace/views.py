from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Listing, Book
from .forms import CreateListingForm
from apps.users.models import Student
from apps.interactions.models import Report

def home(request):
    listings_list = Listing.objects.filter(status='ACTIVE', is_flagged=False).order_by('-created_at')
    
    query = request.GET.get('q', '')
    condition = request.GET.get('condition', '')
    listing_type = request.GET.get('listing_type', '')
    
    if query:
        listings_list = listings_list.filter(
            Q(book__title__icontains=query) | 
            Q(book__author__icontains=query) | 
            Q(book__subject__icontains=query)
        )
    if condition:
        listings_list = listings_list.filter(condition=condition)
    if listing_type:
        listings_list = listings_list.filter(listing_type=listing_type)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('_book_grid.html', {'listings': listings_list}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'home.html', {
        'listings': listings_list,
        'query': query,
        'condition': condition,
        'listing_type': listing_type
    })

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            book, _ = Book.objects.get_or_create(
                isbn=form.cleaned_data['isbn'],
                defaults={
                    'title': form.cleaned_data['title'],
                    'author': form.cleaned_data['author'],
                    'edition': form.cleaned_data['edition'],
                    'subject': form.cleaned_data['subject'],
                }
            )
            Listing.objects.create(
                book=book, seller=request.user,
                listing_type=form.cleaned_data['listing_type'],
                asking_price=form.cleaned_data['asking_price'] if form.cleaned_data['listing_type'] == 'SELL' else None,
                condition=form.cleaned_data['condition'],
                description=form.cleaned_data['description'],
            )
            messages.success(request, "Your book is now live!")
            return redirect('home')
    else:
        form = CreateListingForm()
    return render(request, 'create_listing.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    listing_query = request.GET.get('listing_q', '')
    active_listings = Listing.objects.filter(status='ACTIVE', is_flagged=False).order_by('-created_at')
    if listing_query:
        active_listings = active_listings.filter(Q(book__title__icontains=listing_query) | Q(seller__username__icontains=listing_query))
    
    user_query = request.GET.get('user_q', '')
    all_users = Student.objects.all().order_by('-date_joined')
    if user_query:
        all_users = all_users.filter(Q(username__icontains=user_query) | Q(student_number__icontains=user_query))

    listing_paginator = Paginator(active_listings, 5)
    listing_page_number = request.GET.get('listing_page')
    active_listings_page = listing_paginator.get_page(listing_page_number)

    user_paginator = Paginator(all_users, 5)
    user_page_number = request.GET.get('user_page')
    all_users_page = user_paginator.get_page(user_page_number)

    return render(request, 'dashboard.html', {
        'flagged_listings': Listing.objects.filter(is_flagged=True),
        'active_listings': active_listings_page,
        'all_users': all_users_page,
        'reports': Report.objects.filter(is_resolved=False).order_by('-created_at'),
        'total_users': Student.objects.count(),
        'total_listings': Listing.objects.filter(status='ACTIVE').count(),
        'total_flagged': Listing.objects.filter(is_flagged=True).count(),
        'total_reports': Report.objects.filter(is_resolved=False).count(),
        'listing_query': listing_query,
        'user_query': user_query,
    })

@staff_member_required
def toggle_flag_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    listing.is_flagged = not listing.is_flagged
    listing.save()
    messages.warning(request, f"'{listing.book.title}' flag status updated.")
    return redirect('admin_dashboard')

@staff_member_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    listing.delete()
    messages.error(request, "Listing deleted.")
    return redirect('admin_dashboard')

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(Student, id=user_id)
    user.delete()
    messages.error(request, "User deleted.")
    return redirect('admin_dashboard')