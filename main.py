from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
from os import getenv
from datetime import datetime


load_dotenv()

app = Flask(__name__)

# Config flask instance
app.config["SECRET_KEY"] = getenv("key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = getenv("email")
app.config["MAIL_PASSWORD"] = getenv("email_password")

db = SQLAlchemy(app)
mail = Mail(app)

# Set db table
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))
    

# Main page (form)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save user data in db when get POST request (by pressing submit button)
        
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        occupation = request.form["occupation"]
        
        # Send user data to the db table
        form = Form(first_name=first_name, last_name=last_name,email=email,
            date=datetime.strptime(date, "%Y-%m-%d"), occupation=occupation)
        
        db.session.add(form)
        db.session.commit()
        
        # Send confirmation e-mail to the user
        email_body = f"""Thank you for your submission, {first_name}
        
        Here is your information:
        Name: {first_name} {last_name}
        E-mail: {email}
        Available date: {date}
        Occupation: {occupation}
        
        Best regards, [insert generic company name]"""
        
        message = Message(subject="Thanks for your submission!",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=email_body)
        mail.send(message)
                
        flash(f"{first_name}, your form was submitted successfully!", "success")
        
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=5001, debug=True)