from django.shortcuts import redirect
from functools import wraps


def get_worker_role(user):
    try:
        return user.worker_profile.role
    except Exception:
        return None


def is_pen_worker(user):
    return get_worker_role(user) == 'pen_worker'


def is_supervisor(user):
    return get_worker_role(user) in ['supervisor', 'store_keeper']


def is_manager(user):
    return get_worker_role(user) in ['manager', 'general_manager']


def is_director(user):
    return get_worker_role(user) == 'director'


def is_manager_or_above(user):
    return get_worker_role(user) in ['manager', 'general_manager', 'director']


def is_supervisor_or_above(user):
    return get_worker_role(user) in ['supervisor', 'store_keeper', 'manager',
                                      'general_manager', 'director']


def is_salesperson(user):
    return get_worker_role(user) == 'salesperson'


def is_accountant(user):
    return get_worker_role(user) == 'accountant'


def role_required(*roles):
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
    role = get_worker_role(user)
    return {
        'user_role': role,
        'is_pen_worker': role == 'pen_worker',
        'is_supervisor': role in ['supervisor', 'store_keeper'],
        'is_manager': role in ['manager', 'general_manager'],
        'is_director': role == 'director',
        'is_salesperson': role == 'salesperson',
        'is_accountant': role == 'accountant',
        'is_manager_or_above': role in ['manager', 'general_manager', 'director'],
        'is_supervisor_or_above': role in ['supervisor', 'store_keeper', 'manager',
                                            'general_manager', 'director'],
        'is_general_manager_or_above': role in ['general_manager', 'director'],
        'is_sales_or_above': role in ['salesperson', 'accountant',
                                       'general_manager', 'director'],
    }