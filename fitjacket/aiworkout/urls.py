from django.urls import path
from . import views

urlpatterns = [
  #  path('', views.aiworkout_view, name='aiworkout'),
    path('', views.aiworkout_view, name='aiworkout'),
    path('completed/', views.workout_completed, name='workout-completed'),


]