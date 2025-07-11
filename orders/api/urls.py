from django.urls import path
from orders.api.views import OrderListCreateView, OrderDetailView, OrderCountView, CompletedOrderCountView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/',
         CompletedOrderCountView.as_view(), name='completed-order-count'),

]
