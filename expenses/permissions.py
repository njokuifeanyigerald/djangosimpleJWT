from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj.owner = request.user
        # return obj.owner
        # OR 
        return obj.owner  == request.user