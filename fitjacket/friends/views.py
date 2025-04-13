from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from friends.models import Friendship
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def friends_view(request):
    current_user = request.user
    # Get all friendships where the current user is user1 or user2
    friendships = Friendship.objects.filter(
        Q(user1=current_user) | Q(user2=current_user)
    )
    # Extract the other user in each friendship
    friends = []
    for friendship in friendships:
        if friendship.user1 == current_user:
            friends.append(friendship.user2)
        else:
            friends.append(friendship.user1)
    return render(request, 'friends/social.html',{'friends': friends})


@login_required
def search_friends(request):
    current_user = request.user
    query = request.GET.get('q', '').strip()

    # Retrieve friends of the current user
    friendships = Friendship.objects.filter(
        Q(user1=current_user) | Q(user2=current_user)
    )
    friend_ids = set()
    for friendship in friendships:
        # Add the friend user id (the one that is not the current user)
        friend_ids.add(friendship.user1.id if friendship.user1 != current_user else friendship.user2.id)

    # Also exclude the current user from search results
    friend_ids.add(current_user.id)

    potential_friends = User.objects.none()  # default empty queryset
    if query:
        # Searching by username, first name, or last name
        potential_friends = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            userprofile__isnull=False
        ).exclude(id__in=friend_ids)

    context = {
        'potential_friends': potential_friends,
        'query': query,
    }
    return render(request, 'friends/search.html', context)

@login_required
def add_friend(request, user_id):
    target_user = User.objects.get(id=user_id)
    current_user = request.user

    # Prevent self-add and duplicates
    if current_user != target_user:
        # Sort users to match the Friendship model's ordering
        u1, u2 = sorted([current_user, target_user], key=lambda u: u.id)
        Friendship.objects.get_or_create(user1=u1, user2=u2)

    return redirect('friends')

@login_required
def remove_friend(request, user_id):
    target_user = User.objects.get(id=user_id)
    current_user = request.user

    # Sort users to match the Friendship model's ordering
    u1, u2 = sorted([current_user, target_user], key=lambda u: u.id)
    Friendship.objects.filter(user1=u1, user2=u2).delete()

    return redirect('friends')
