from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends_view, name='friends'),
    path('search-friends/', views.search_friends, name='search_friends'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
]