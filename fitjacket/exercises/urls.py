from django.urls import path
from . import views

urlpatterns = [
    path('', views.exercise_list, name='exercise-list'),
    path('<str:exercise_id>/', views.exercise_detail, name='exercise-detail'),
]