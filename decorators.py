from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from RestaurantManagement.models import Restaurant

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def role_and_restaurant_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            restaurant_id = kwargs.get('pk')
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            if not request.user.restaurants.filter(id=restaurant.id).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator