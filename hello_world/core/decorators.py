from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def require_permission(permission):
    """
    Decorator to check if user has specific permission
    Usage: @require_permission('view_patient')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile'):
                messages.error(request, 'User profile not found. Please contact administrator.')
                return redirect('dashboard')

            if request.user.userprofile.has_permission(permission):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Access denied. Required permission: {permission}')
                return redirect('dashboard')
        return _wrapped_view
    return decorator

def require_role(role):
    """
    Decorator to check if user has specific role
    Usage: @require_role('doctor')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile'):
                messages.error(request, 'User profile not found. Please contact administrator.')
                return redirect('dashboard')

            if request.user.userprofile.role == role:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Access denied. Required role: {role}')
                return redirect('dashboard')
        return _wrapped_view
    return decorator

def require_any_permission(*permissions):
    """
    Decorator to check if user has any of the specified permissions
    Usage: @require_any_permission('view_patient', 'add_patient')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile'):
                messages.error(request, 'User profile not found. Please contact administrator.')
                return redirect('dashboard')

            user_permissions = request.user.userprofile.get_all_permissions()
            if any(perm in user_permissions for perm in permissions):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Access denied. Required permissions: {", ".join(permissions)}')
                return redirect('dashboard')
        return _wrapped_view
    return decorator

def require_module_access(module_name):
    """
    Decorator to check if user can access a specific module
    Usage: @require_module_access('patient_management')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile'):
                messages.error(request, 'User profile not found. Please contact administrator.')
                return redirect('dashboard')

            if request.user.userprofile.can_access_module(module_name):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Access denied. Cannot access module: {module_name}')
                return redirect('dashboard')
        return _wrapped_view
    return decorator