from django.urls import path
from user_auth.api import views

urlpatterns = [
    path('registration/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]
