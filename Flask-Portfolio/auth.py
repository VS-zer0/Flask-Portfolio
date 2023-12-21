from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask_login import current_user
from flask_admin import AdminIndexView
from flask import redirect

class UserAuth(UserMixin):
    def __init__(self, id, active=True):
        self.id = id
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

class AuthMixin(object):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect('/login/')

class AdminIndex(AuthMixin, AdminIndexView):
    pass