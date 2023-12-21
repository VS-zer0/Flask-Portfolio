from flask import Flask, render_template, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash, secrets
from flask_admin import Admin
from flask_login import login_user, LoginManager
from models import db, User, Work, Attachments, Subject, Course
from views import WorkAdmin, SubjectAdmin, CourseAdmin, UserAuth, AdminIndex
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaZe.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user):
    u = User.query.get(user)
    return UserAuth(u.id)

admin = Admin(app, name='Admin Panel', index_view=AdminIndex())

admin.add_view(WorkAdmin(Work, db.session))
admin.add_view(SubjectAdmin(Subject, db.session))
admin.add_view(CourseAdmin(Course, db.session))

@app.route('/')
def home():
    subjects = Subject.query.all()
    return render_template('base.html', subjects=subjects)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check the login credentials
        if check_password_hash(User.query.first().password, request.form['password']):
            # Save the login status in the session
            login_user(load_user(1))
            return redirect(url_for('admin.index'))
    return '''
        <form method="post">
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

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
    with app.app_context():
        db.create_all()
        # if not User.query.all():
        #     db.session.add(User(password = generate_password_hash(os.environ.get('Key'))))
        #     db.session.commit()
    app.run(host='0.0.0.0', debug=True)