from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Class for determining perms for moderators."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Class for determining perms for course and lesson owners."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
