from django.urls import path
from . import views

urlpatterns = [
  #  path('', views.aiworkout_view, name='aiworkout'),
    path('', views.aiworkout_view, name='aiworkout'),
    path('log/', views.log_workout, name='log_workout'),
    path('chart/', views.workout_chart, name='workout_chart'),
    path('completed/', views.workout_completed, name='workout-completed'),
    path('log-bulk/', views.log_bulk_workout, name='log_bulk_workout'),
    path('badges/', views.badges_view, name='badges'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),

]