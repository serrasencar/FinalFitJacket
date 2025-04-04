from django.urls import path
from . import views

urlpatterns = [
    path('', views.aiworkout_view, name='aiworkout'),
]