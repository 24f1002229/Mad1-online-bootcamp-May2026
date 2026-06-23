from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    id = db.Column(db.Integer,nullable=False, primary_key=True)
    name = db.Column(db.String, nullable= False)
    description = db.Column(db.String)
    questions = db.relationship("Question", backref="course", cascade="all,delete", lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer,nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    question_statement = db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable = False)
    option2 = db.Column(db.String, nullable= False)
    option3 = db.Column(db.String)
    option4 = db.Column(db.String)
    correct_option = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp_of_attempt = db.Column(db.Time)
    total_scored = db.Column(db.Integer, default=00)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, default=1)
    scores = db.relationship("Scores", backref="user", cascade="all,delete", lazy=True)
