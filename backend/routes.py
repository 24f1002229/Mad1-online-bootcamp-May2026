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
            return redirect(url_for("user"))
        elif user and user.role == 0:
            return redirect(url_for("admin"))
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
        
@app.route("/admin")
def admin():
    courses = get_course()
    return render_template("admin.html", courses=courses)


def get_course(id=None):
    if id:
        return Course.query.filter_by(id=id).first()
    return Course.query.all()


@app.route("/user")
def user():
    courses = get_course()
    return render_template("User.html", courses=courses)