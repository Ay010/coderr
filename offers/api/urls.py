from django.urls import path
from offers.api.views import OfferListCreateAPIView, OfferDetailDetailAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('offerdetails/<int:pk>/', OfferDetailDetailAPIView.as_view(),
         name='offer-detail-detail'),

]
