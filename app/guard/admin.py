from flask import session, redirect
from functools import wraps


def admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['user']['type'] == 'admin':
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap
