from django.contrib import admin
from django.urls import path
from profiles.api.views import ProfileDetailView, ListBusinessProfilesView, ListCustomerProfilesView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', ListBusinessProfilesView.as_view(),
         name='list-business-profiles'),
    path('profiles/customer/', ListCustomerProfilesView.as_view(),
         name='list-customer-profiles'),

]
