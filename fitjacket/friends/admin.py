from django.contrib import admin
from .models import Friendship, FriendRequest


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    actions = ['remove_selected_friendships']

    def remove_selected_friendships(self, request, queryset):
        """
        Deletes the selected friendships.
        """
        deleted_count = queryset.delete()
        self.message_user(request, f"Deleted {deleted_count[0]} friendship(s).")

    remove_selected_friendships.short_description = "Remove selected Friendships"


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['remove_selected_friend_requests']

    def remove_selected_friend_requests(self, request, queryset):
        """
        Deletes the selected friend requests.
        """
        deleted_count = queryset.delete()
        self.message_user(request, f"Deleted {deleted_count[0]} friend request(s).")

    remove_selected_friend_requests.short_description = "Remove selected Friend Requests"