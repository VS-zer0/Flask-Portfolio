from flask import Flask, render_template
from flask_admin import Admin
from models import db, Work, Attachments, Subject, Course
from views import WorkAdmin, SubjectAdmin, CourseAdmin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaZe.db'
db.init_app(app)


@app.route('/')
def home():
    subjects = Subject.query.all()
    return render_template('base.html', subjects=subjects)


@app.route('/<int:subj_id>/')
def works(subj_id):
    works = Work.query.filter_by(subject_id = subj_id).order_by(Work.date.desc()).all()
    courses = list(dict.fromkeys([work.course for work in works]))
    subjects = Subject.query.all()
    return render_template('works/index.html', courses=courses, subjects=subjects, works=works)


@app.route('/<int:subj_id>/<int:crs_id>/')
def works_course(subj_id, crs_id):
    all_works = Work.query.filter_by(subject_id = subj_id).order_by(Work.date.desc()).all()
    works = Work.query.filter_by(subject_id = subj_id, course_id=crs_id).order_by(Work.date.desc()).all()
    courses = list(dict.fromkeys([work.course for work in all_works]))
    subjects = Subject.query.all()
    return render_template('works/index.html', courses=courses, subjects=subjects, works=works)


@app.route('/<int:subj_id>/<int:crs_id>/<int:work_id>/')
def work_detail(subj_id, crs_id, work_id):
    subjects = Subject.query.all()
    works = Work.query.filter_by(subject_id=subj_id).all()
    work = Work.query.filter_by(id=work_id).first()
    attachments = Attachments.query.filter_by(work_id=work_id).all()
    return render_template('work_detail/index.html', works=works, subjects=subjects, work=work, attachments=attachments)


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