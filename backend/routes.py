from flask import Flask, render_template, request, redirect, url_for
from app import app
from .model import *

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"] )
def Login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user and user.role == 1:
            return redirect(url_for("user", email=email))
        elif user and user.role == 0:
            return redirect(url_for("admin", email=email))
        else:
            return render_template("Login.html", msg= "Invalid user Register yourself first")
        
    return render_template("Login.html", msg="")


@app.route("/register", methods=["GET","POST"])
def Register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template("Register.html", msg="User already exists You can login yourself!!")
        newuser = User(email=email, password=password)
        db.session.add(newuser)
        db.session.commit()
        return render_template("Login.html", msg="you can continue with login!!")
    return render_template("Register.html")
        
@app.route("/Admin/<email>")
def admin(email):
    courses = get_course()
    return render_template("admin.html", courses=courses, email=email)


def get_course(id=None):
    if id:
        return Course.query.filter_by(id=id).first()
    return Course.query.all()


@app.route("/user/<email>")
def user(email):
    courses = get_course()
    return render_template("User.html", courses=courses, email=email)

@app.route("/add_course/<email>", methods=["GET","POST"])
def add_course(email):
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        description = request.form.get("description")
        newcourse = Course(id=id, name=name, description=description)
        db.session.add(newcourse)
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("add_course.html", email=email)


@app.route("/edit_course/<id>/<email>", methods=["GET","POST"])
def edit_course(email, id):
    c = get_course(id)
    if request.method=="POST":
        id = request.form.get("id")
        name = request.form.get("name")
        description = request.form.get("description")
        c.id = id
        c.name = name
        c.description = description
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("edit_course.html", email=email, course = c)


@app.route("/delete_course/<id>/<email>", methods=["GET","POST"])
def delete_course(email,id):
    dc = get_course(id)
    db.session.delete(dc)
    db.session.commit()
    return redirect(url_for("admin", email=email))


def get_question(id):
    questions = Question.query.filter_by(id=id).first()
    return questions


@app.route("/add_question/<course_id>/<email>", methods=["GET","POST"])
def add_question(course_id,email):
    if request.method == "POST":
        id = request.form.get("id")
        title = request.form.get("title")
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option_key = request.form.get("correct_option")
        correct_option_mapping = {"option1" : option1, "option2" : option2, "option3" : option3, "option4" : option4}
        correct_option = correct_option_mapping.get(correct_option_key, "")
        newquestion = Question(id=id, title=title, question_statement=question_statement, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option, course_id=course_id)
        db.session.add(newquestion)
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("add_question.html", course_id=course_id, email=email)


@app.route("/edit_question/<id>/<email>", methods=["GET","POST"])
def edit_question(id,email):
    ques = get_question(id)
    if request.method == "POST":
        id = request.form.get("id")
        title = request.form.get("title")
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")
        ques.id = id
        ques.title = title
        ques.question_statement = question_statement
        ques.option1 = option1
        ques.option2 = option2
        ques.option3 = option3
        ques.option4 = option4
        ques.correct_option = correct_option
        db.session.commit()
        return redirect(url_for("admin", email=email))
    return render_template("edit_question.html", question = ques, email=email)

@app.route("/delete_question/<id>/<email>", methods=["GET","POST"])
def delete_question(id,email):
    dq = get_question(id)
    db.session.delete(dq)
    db.session.commit()
    return redirect(url_for("admin",email=email))



        