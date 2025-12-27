from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from itsdangerous import URLSafeSerializer

app = Flask(__name__)

app.config['SECRET_KEY']= 'URMUM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from routes import *

if __name__ == '__main__' :

  app.run(debug=True)



