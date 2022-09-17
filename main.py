import os
from flask import Flask, request, render_template, redirect, url_for, make_response
import pdfkit
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cv_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    email = db.Column(db.String)
    user_profile = db.Column(db.String)
    experience = db.Column(db.PickleType)
    skills = db.Column(db.String)
    education = db.Column(db.PickleType)

db.create_all()


@app.route('/', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        email = request.form.get('email')
        user_profile = request.form.get('profile')
        experience = request.form.get('experience')
        skills = request.form.get('skills')
        education = request.form.get('education')

        user = User(name=name, number=number, email=email, user_profile=user_profile, experience=experience.split(";"),
                    skills=skills, education=education.split(';'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('preview', id=user.id))

    else:
        return render_template('form.html')


@app.route('/preview/<id>')
def preview(id):
    user = User.query.filter(User.id == id).first()
    if user:
        CV_html = render_template('CV.html', user=user)
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        CV_pdf = pdfkit.from_string(CV_html, configuration=config)
        response = make_response(CV_pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=CV.pdf"
        return response
    else:
        return redirect(url_for('form'))





if __name__ == "__main__":
    app.run(debug=True)