from rest_framework import permissions


class OwOrReadOnly(permissions.BasePermission):
    """
    Custom permission. Проверяет метод запроса и статус.
    Если все ок - далее выдается объект.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return (request.user.is_superuser
                    or obj.author == request.user)
        return False
