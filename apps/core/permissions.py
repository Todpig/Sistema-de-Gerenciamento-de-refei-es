from rest_framework.permissions import BasePermission

class CheckUserCoordenator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_authenticated == True and request.user.coordenator == True:
            return True
        else:
            return False

class CheckUserChef(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_authenticated == True and request.user.chef == True:
            return True
        else:
            return False