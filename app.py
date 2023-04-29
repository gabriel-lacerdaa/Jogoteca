from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('configs.py')
db = SQLAlchemy(app)
#Token de segurança
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from view_user import *
from view_games import *

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
