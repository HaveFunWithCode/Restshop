from django.contrib.auth.models import User
from rest_framework import permissions
from .models import ProductUnit


class IsSupplierOrAdminOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the suppliers and admin
        sellers=[u.seller.user for u  in obj.product_unit.all()]
        return request.user in sellers or request.user.is_superuser


