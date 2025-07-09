from rest_framework import generics
from orders.models import Order
from orders.api.serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from offers.models import OfferDetail
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from orders.api.permissions import UserIsCustomer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer_user=self.request.user) | Order.objects.filter(business_user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [UserIsCustomer()]

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data['offer_detail_id']
        offerDetail = OfferDetail.objects.get(id=offer_detail_id)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offerDetail.offers.all().first().user,
            offer_detail=offerDetail,
            status="in_progress",
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        response = {
            "id": order.id,
            "customer_user": order.customer_user.id,
            "business_user": order.offer_detail.offers.all().first().user.id,
            "title": order.offer_detail.title,
            "revisions": order.offer_detail.revisions,
            "delivery_time_in_days": order.offer_detail.delivery_time_in_days,
            "price": order.offer_detail.price,
            "features": order.offer_detail.get_features(),
            "offer_type": order.offer_detail.offer_type,
            "status": order.status,
            "created_at": order.created_at,
            "updated_at": order.updated_at
        }

        return Response(response, status=status.HTTP_201_CREATED)
