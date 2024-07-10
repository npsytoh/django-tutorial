from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.ProfileUpdateView.as_view(), name='profile-update'),
]