from rest_framework.permissions import BasePermission


class UserIsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "customer"
