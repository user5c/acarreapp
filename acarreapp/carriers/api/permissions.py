from rest_framework import permissions


class IsClient(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        has_client_group = request.user.groups.filter(name="client")

        return bool(has_client_group)
