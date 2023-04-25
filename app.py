from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

app.config.from_pyfile('configs.py')

db = SQLAlchemy(app)

#Token de segurança
csrf = CSRFProtect(app)

from view import *

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
