from django.urls import path
from orders.api.views import OrderListCreateView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='orders'),

]
