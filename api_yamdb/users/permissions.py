from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrAdmins(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        author = obj == request.user
        return author or request.user.is_admin or request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.is_admin
        )
