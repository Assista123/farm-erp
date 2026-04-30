from django.shortcuts import redirect
from functools import wraps


def get_worker_role(user):
    """Get the role of the logged in user from their linked Worker record."""
    try:
        return user.worker_profile.role
    except Exception:
        return None


def is_pen_worker(user):
    return get_worker_role(user) == 'pen_worker'


def is_supervisor(user):
    return get_worker_role(user) in ['supervisor', 'store_keeper']


def is_manager(user):
    return get_worker_role(user) == 'manager'


def is_director(user):
    return get_worker_role(user) == 'director'


def is_manager_or_above(user):
    return get_worker_role(user) in ['manager', 'director']


def is_supervisor_or_above(user):
    return get_worker_role(user) in ['supervisor', 'store_keeper', 'manager', 'director']


def role_required(*roles):
    """Decorator that restricts a view to users with specific roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role = get_worker_role(request.user)
            if role not in roles:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_user_context(user):
    """Returns context variables about the current user's role
    for use in templates."""
    role = get_worker_role(user)
    return {
        'user_role': role,
        'is_pen_worker': role == 'pen_worker',
        'is_supervisor': role in ['supervisor', 'store_keeper'],
        'is_manager': role == 'manager',
        'is_director': role == 'director',
        'is_manager_or_above': role in ['manager', 'director'],
        'is_supervisor_or_above': role in ['supervisor', 'store_keeper',
                                           'manager', 'director'],
    }