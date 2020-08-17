from rest_framework import permissions


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """Object level permission"""
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        
        return request.user.is_staff or request.user == obj.author
    
