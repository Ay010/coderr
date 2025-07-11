from rest_framework.permissions import BasePermission
from orders.models import Order


class UserIsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == "customer"


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'type') and request.user.type == "business"


class isOrderAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        order = Order.objects.filter(id=view.kwargs['pk']).first()
        if order is None:
            return True  # Erlaube Zugriff, damit die View selbst 404 handhaben kann

        return request.user == order.customer_user or request.user == order.business_user
