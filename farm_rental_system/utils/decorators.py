from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response

from users.models import CustomUser


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('load_home_page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                try:
                    user = CustomUser.objects.get(id=request.user.id)
                    groups = user.groups.all()

                    for group in groups:
                        if group.name in allowed_roles:
                            return view_func(request, *args, **kwargs)

                except CustomUser.DoesNotExist:
                    pass  # Handle case where user does not exist
            # Handle unauthorized access
            return Response({'status': 403, 'message': 'You are not allowed to access this page'},
                            status=status.HTTP_403_FORBIDDEN)

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = request.user.groups.all()
        for group in groups:
            if group.name == 'admin':
                return view_func(request, *args, **kwargs)
        return redirect('tenant_home')

    return wrapper_func
