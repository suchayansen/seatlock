
from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def role_required(*allowed_roles):
    """
    Restrict access to users with specific roles.
    Must be used below @route.
    """

    def decorator(view_function):

        @wraps(view_function)
        @login_required
        def wrapped_view(*args, **kwargs):

            if current_user.role not in allowed_roles:
                abort(403)

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator


def admin_required(view_function):
    return role_required("admin")(view_function)


def organizer_required(view_function):
    return role_required("organizer")(view_function)


def student_required(view_function):
    return role_required("student")(view_function)
