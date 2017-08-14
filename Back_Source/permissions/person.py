from rest_framework import permissions


# Permission which can access Client
class ClientPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Clients').exists():
            # The clients can not delete it's account
            if request.method == "DELETE":
                return False
            else:
                return True
        elif request.user.groups.filter(name='Collaborators').exists():
            return True
        elif request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Clients').exists():
            # request.method == "GET" and
            if obj.user == request.user:
                return True
        elif request.user.groups.filter(name='Collaborators').exists() or request.user.is_superuser:
            return True
        return False


# Permission which can access drivers
class DriverPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Drivers').exists():
            return True
        elif request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Drivers').exists() or request.user.is_superuser:
            return True
        return False

