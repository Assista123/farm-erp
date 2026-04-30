from .permissions import get_user_context


def user_role_context(request):
    """Adds user role variables to every template context automatically."""
    if request.user.is_authenticated:
        return get_user_context(request.user)
    return {
        'user_role': None,
        'is_pen_worker': False,
        'is_supervisor': False,
        'is_manager': False,
        'is_director': False,
        'is_manager_or_above': False,
        'is_supervisor_or_above': False,
    }