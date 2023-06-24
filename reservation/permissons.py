from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            # return request.user.is_authenticated
            return True
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return True
        elif view.action == 'destroy':
            return bool(request.user.is_superuser)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update']:
            return obj.user == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return bool(request.user.is_staff)
        else:
            return False

        # admin : del , PUT , POST
        # user :  GET , PUT


class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access to all users

        # Check if the user is a doctor
        user = request.user
        if user.is_authenticated and user.is_doctor:
            return True

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        elif view.action in ['update', 'partial_update', 'retrieve', 'destroy']:
            return request.user.is_staff or request.obj.doctor
        else:
            return False


class RetrieveOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'retrieve':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if view.action == 'retrieve':
            return True
        else:
            return False

class IsAdminOrUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        elif view.action in ['update', 'destroy', 'partial_update']:
            return request.user.is_staff

        elif view.action in ['retrieve']:
            return request.user.is_authenticated
        else:
            return False
