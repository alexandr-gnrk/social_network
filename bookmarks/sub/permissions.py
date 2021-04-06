from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.permissions import BasePermission


def allowed_users(allowed_roles=[]):
    """ User Role Based Permissions
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.first().name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # return HttpResponse('You are not Subscriber to view this page')
                return redirect('dashboard')
        return wrapped_view
    return decorator


class IsAuthenticatedAndSubscriber(BasePermission):
    """ The request is authenticated as a user and subscriber, or is a read-only request.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='subscribers').exists()
        )
