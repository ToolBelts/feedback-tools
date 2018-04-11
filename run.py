# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template, request, flash, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import redirect, secure_filename
from integration.mail import send_mail
from integration.bucket import create_file

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.secret_key = 'FEEDBACK-SECRET'

# CONFIGURATION

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_DBNAME'] = 'feedback_secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/feedback_secret'

mongo = PyMongo(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def index():
    output = []
    feedback_secret = mongo.db.users
    for pessoas in feedback_secret.find():
        output.append({'name': pessoas['name'], 'email': pessoas['email'], 'image': pessoas['cloudinary']['url']})
    return render_template("index.html", titulo="Feedback Anônimo", pessoas=output)


@app.route("/new-user", methods=['POST'])
def new_user():
    name = request.form.get('name')
    email = request.form.get('email')
    file = request.files['file']

    file_path = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    feedback_secret = mongo.db.users
    feedback_secret.insert({'name': name, 'email': email, 'cloudinary': create_file(file_path)})
    flash('Usuário cadastrado com sucesso')
    return redirect(url_for('index'))


@app.route("/new-feedback", methods=['POST'])
def new_feedback():
    feedback = request.form.get('feedback')
    email = request.form.get('email-to-feedback')

    feedback_secret = mongo.db.feedbacks
    feedback_secret.insert({'feedback': feedback, 'email': email})

    send_mail(email, feedback)

    flash('Feedback registrado com sucesso!')
    return redirect(url_for('index'))


app.run(debug=True, port=8090)
