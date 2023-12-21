from flask_admin.contrib.sqla import ModelView
from models import Attachments
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


class WorkAdmin(AuthMixin, ModelView):
    inline_models = (Attachments,)
    column_list = ('title', 'content', 'link', 'type',
                   'subject.name', 'course.name', 'date')
    column_labels = {'title': 'Work Title', 'content': 'Description',
                     'link': 'Link','type': 'Type', 'subject.name': 'Subject',
                     'course.name': 'Course', 'date': 'Date'}
    column_filters = ('course.name', 'subject.name', 'title')


class SubjectAdmin(AuthMixin, ModelView):
    column_list = ('name',)
    column_labels = {'name': 'Subject Name',}
    column_filters = ('name',)
    
class CourseAdmin(AuthMixin, ModelView):
    column_list = ('name',)
    column_labels = {'name': 'Name'}
    column_filters = ('name',)