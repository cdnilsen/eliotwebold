from flask import Flask, flash, request, jsonify, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

UPLOAD_FOLDER = 'texts'
ALLOWED_EXTENTIONS = {'txt'}

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def mainPage():
    return render_template('index.html')

@app.route("/morphsearch", methods=['GET', 'POST'])
def morphsearch():
    if request.method == 'POST':
        return render_template(url_for('morphsearch.html'))

    return render_template('morphsearch.html')

@app.route("/searchenglish", methods=['GET', 'POST'])
def searchenglish():
    if request.method == 'POST':
        return render_template(url_for('searchenglish.html'))

    return render_template('searchenglish.html')


    
