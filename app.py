from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_pyfile('configs.py')

db = SQLAlchemy(app)

from view import *

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
