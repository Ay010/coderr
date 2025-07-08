from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print(request.user)
            print(request.user.type)
            return request.user.type == 'business'
        return False


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
