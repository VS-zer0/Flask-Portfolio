from flask_admin.contrib.sqla import ModelView
from models import Attachments

class WorkAdmin(ModelView):
    inline_models = (Attachments,)
    column_list = ('title', 'content', 'link', 'type',
                   'subject.name', 'course.name', 'date')
    column_labels = {'title': 'Work Title', 'content': 'Description',
                     'link': 'Link','type': 'Type', 'subject.name': 'Subject',
                     'course.name': 'Course', 'date': 'Date'}
    column_filters = ('course.name', 'subject.name', 'title')

class SubjectAdmin(ModelView):
    column_list = ('name',)
    column_labels = {'name': 'Subject Name',}
    column_filters = ('name',)
    
class CourseAdmin(ModelView):
    column_list = ('name',)
    column_labels = {'name': 'Name'}
    column_filters = ('name',)
    
    