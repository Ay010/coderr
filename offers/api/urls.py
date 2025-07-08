from django.urls import path
from offers.api.views import OfferListCreateAPIView, OfferDetailDetailAPIView, SingleOfferAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', SingleOfferAPIView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailDetailAPIView.as_view(),
         name='offer-detail-detail'),

]
