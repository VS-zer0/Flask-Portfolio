from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    
    
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum('Link', 'Embed Document', 'Embed Repl.it'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject')
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course')
    
    attachments = db.relationship('Attachments', cascade="all,delete", backref='work')
    
    def __repr__(self):
        return self.title


class Attachments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    
    
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return self.name
    
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return self.name
    
    