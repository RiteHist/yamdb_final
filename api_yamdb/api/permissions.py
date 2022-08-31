from rest_framework.permissions import SAFE_METHODS, BasePermission


class AnonReadOnlyOrOwnerAdminModerator(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return (obj.author == request.user
                    or request.user.is_admin
                    or request.user.is_moderator
                    or request.user.is_superuser)
        return True
