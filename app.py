from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from os import getenv
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("FLASK_S_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQL_DB_URI")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = getenv("EMAIL")
app.config["MAIL_PASSWORD"] = getenv("GMAIL_APP_PASSWORD")
db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_format = datetime.strptime(date, '%Y-%m-%d')
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_format, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        body = f"""
        Received application mail\n
        Details:\n
        First name: {first_name}\n
        Last name: {last_name}\n
        Date: {date_format}\n
        Occupation: {occupation}
"""
        message = Message(subject="New application form",
                       sender=getenv("EMAIL"),
                       recipients=[email],
                       body=body
                       )
        mail.send(message=message)

        flash("User data submitted successfully.", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5905)
