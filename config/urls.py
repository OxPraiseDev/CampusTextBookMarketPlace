from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.marketplace.views import (
    home, create_listing, admin_dashboard, 
    toggle_flag_listing, delete_listing, delete_user
)
from apps.interactions.views import (
    inbox, start_chat, view_chat, delete_message, 
    confirm_transaction, select_trade_book, mark_messages_read, 
    submit_report
)
from apps.users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', user_views.register_view, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('listing/create/', create_listing, name='create_listing'),
    
    # Chat & Inbox
    path('inbox/', inbox, name='inbox'),
    path('chat/<uuid:listing_id>/', start_chat, name='start_chat'),
    path('chat/room/<uuid:room_id>/', view_chat, name='view_chat'),
    path('chat/delete/<uuid:message_id>/', delete_message, name='delete_message'),
    path('chat/confirm/<uuid:room_id>/', confirm_transaction, name='confirm_transaction'),
    path('chat/select-trade/<uuid:listing_id>/', select_trade_book, name='select_trade_book'),
    path('chat/mark-read/<uuid:room_id>/', mark_messages_read, name='mark_messages_read'),
    path('chat/report/<uuid:room_id>/', submit_report, name='submit_report'),
    
    # Dashboard
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/flag/<uuid:listing_id>/', toggle_flag_listing, name='toggle_flag_listing'),
    path('dashboard/delete-listing/<uuid:listing_id>/', delete_listing, name='delete_listing'),
    path('dashboard/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('dashboard/edit-user/<int:user_id>/', user_views.edit_user_view, name='edit_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)