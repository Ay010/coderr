from rest_framework import generics
from orders.models import Order
from orders.api.serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from offers.models import OfferDetail
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from orders.api.permissions import UserIsCustomer, IsBusinessUser, isOrderAdmin
from user_auth.models import User


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer_user=self.request.user) | Order.objects.filter(business_user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [UserIsCustomer()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response_data = []
        for order in queryset:
            order_response = {
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
            response_data.append(order_response)

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if type(request.data.get('offer_detail_id')) != int:
            return Response({"error": "Offer detail id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        if not OfferDetail.objects.filter(id=request.data.get('offer_detail_id')).exists():
            return Response({"error": "Offer detail not found"}, status=status.HTTP_404_NOT_FOUND)

        offer_detail_id = request.data.get('offer_detail_id')
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


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [isOrderAdmin()]
        return [IsBusinessUser()]

    def get_object(self):
        try:
            return super().get_object()
        except Order.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        valid_statuses = ["in_progress", "completed", "cancelled"]

        if 'status' in request.data and request.data.get('status') in valid_statuses:
            order.status = request.data['status']
            order.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order.save()

            # Return the updated order with the same format as retrieve
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

            return Response(response, status=status.HTTP_200_OK)

        return Response({"error": "Valid status field is required"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class OrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        if User.objects.filter(id=user_id).exists():
            if User.objects.get(id=user_id).type == "business":
                order_count_filtered = Order.objects.filter(
                    business_user=user_id, status="in_progress").count()
            else:
                return Response({"error": "User is not a business user"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"order_count": order_count_filtered}, status=status.HTTP_200_OK)


class CompletedOrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        if User.objects.filter(id=user_id).exists():
            if User.objects.get(id=user_id).type == "business":
                order_count_filtered = Order.objects.filter(
                    business_user=user_id, status="completed").count()
            else:
                return Response({"error": "User is not a business user"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"completed_order_count": order_count_filtered}, status=status.HTTP_200_OK)
