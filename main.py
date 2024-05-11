from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv
from datetime import datetime


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = getenv("key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))
    

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = Form(
            first_name = request.form["first_name"],
            last_name = request.form["last_name"],
            email = request.form["email"],
            date = datetime.strptime(request.form["date"], "%Y-%m-%d"),
            occupation = request.form["occupation"]
        )
        
        db.session.add(form)
        db.session.commit()
        
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=5001, debug=True)