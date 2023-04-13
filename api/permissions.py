from rest_framework.permissions import BasePermission
from .models import CustomUser


class IsFarmerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_farmer)


class IsBuyerUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_buyer)

class IsTransporterUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_transporter)