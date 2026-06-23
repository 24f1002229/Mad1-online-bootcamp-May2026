from flask import Flask
from backend.model import db

app = None

def setup():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key="mysecret1234"
    db.init_app(app)
    app.app_context().push()
    print("App is working!!")
    return app

app = setup()

from backend.routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(email="admin@gmail.com").first()
        if not admin: 
            admin = User(
                email = "admin@gmail.com",
                password = "1234",
                role = 0
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin added successfully !!")
        print("Admin already in database!!")    

    app.run(debug=True)