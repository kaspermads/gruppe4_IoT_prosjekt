from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Tillatelse som kun tillater tilgang til superbrukere.
    """
    message = "Please contact your chief nurse for access."

    def has_permission(self, request, view):
        # Tillat kun superbrukere
        return request.user and request.user.is_superuser
