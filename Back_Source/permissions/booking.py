from rest_framework import permissions


class BookingPermissions(permissions.BasePermission):
    message = 'You are not allowed to access to the request bookings.'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Clients').exists():
            if request.method == "GET":
                return True
        elif request.user.groups.filter(name='Collaborators').exists():
            return True
        elif request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print request.user
        print obj.client
        if request.user.groups.filter(name='Clients').exists():
            if request.method == "GET" and obj.client.user == request.user:
                return True
        elif request.user.groups.filter(name='Collaborators').exists() or request.user.is_superuser:
            return True
        return False


class VehiclePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Drivers').exists():
            if request.method == "GET":
                return True
        elif request.user.is_superuser:
            return True
        return False