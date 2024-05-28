from flask import Flask, render_template
from flask_admin import Admin
from models import db, Work, Attachments, Subject, Course
from views import WorkAdmin, SubjectAdmin, CourseAdmin
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaZe.db'
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
db.init_app(app)


@app.route('/')
def home():
    courses = Course.query.all()
    return render_template('base.html', courses=courses)


@app.route('/<int:crs_id>/')
def subjects(crs_id):
    works = Work.query.filter_by(course_id = crs_id).order_by(Work.date.desc()).all()
    courses = Course.query.all()
    subjects = list(dict.fromkeys([work.subject for work in works]))
    return render_template('subject_list.html', courses=courses, subjects=subjects, works=works)


@app.route('/<int:crs_id>/<int:subj_id>/')
def works_course(subj_id, crs_id):
    all_works = Work.query.filter_by(course_id = crs_id).order_by(Work.date.desc()).all()
    works = Work.query.filter_by(subject_id = subj_id, course_id=crs_id).order_by(Work.date.desc()).all()
    courses = Course.query.all()
    subjects = list(dict.fromkeys([work.subject for work in all_works]))
    return render_template('work_list.html', courses=courses, subjects=subjects, works=works)


@app.route('/<int:crs_id>/<int:subj_id>/<int:work_id>/')
def work_detail(subj_id, crs_id, work_id):
    courses = Course.query.all()
    works = Work.query.filter_by(course_id=crs_id).all()
    work = Work.query.filter_by(id=work_id).first()
    attachments = Attachments.query.filter_by(work_id=work_id).all()
    return render_template('work_detail.html', works=works, courses=courses, work=work, attachments=attachments)


if __name__ == '__main__':
    from flask_admin import Admin
    from views import WorkAdmin, SubjectAdmin, CourseAdmin
    
    admin = Admin(app, name='Admin Panel')
    admin.add_view(WorkAdmin(Work, db.session))
    admin.add_view(SubjectAdmin(Subject, db.session))
    admin.add_view(CourseAdmin(Course, db.session))
    
    with app.app_context():
        db.create_all()
        
    app.run()
    
    