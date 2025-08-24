from rest_framework import permissions
from .models import User

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_SUPERADMIN

class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_AGENT

class IsFarmer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_FARMER

class IsOwnerOrSuperAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.ROLE_SUPERADMIN:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False