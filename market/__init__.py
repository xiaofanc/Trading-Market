from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# make app recognize its database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'f595e088df5d3e1cc981fa8d'
db = SQLAlchemy(app)
app.app_context().push()

from market import routes