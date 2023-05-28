from rest_framework.permissions import BasePermission


class IsBanker(BasePermission):
    """
    Allows users if they are bankers
    """

    def has_permission(self, request, view):

        if request.user.user_type == "banker":
            return True
        return False


class IsProvider(BasePermission):
    """
    Allows users if they are Provider
    """

    def has_permission(self, request, view):

        if request.user.user_type == "provider":
            return True
        return False


class IsCustomer(BasePermission):
    """
    Allows users if they are Customer
    """

    def has_permission(self, request, view):

        if request.user.user_type == "customer":
            return True
        return False
