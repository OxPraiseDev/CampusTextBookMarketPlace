from django.db.models import Q
from .models import Message

def unread_messages(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(
            Q(room__buyer=request.user) | Q(room__seller=request.user),
            is_read=False
        ).exclude(sender=request.user).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}