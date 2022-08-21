from flask import Flask
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__, instance_relative_config=True)
app.secret_key = "membuatLOginFlask1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/fypdb'
db = SQLAlchemy(app)


app.config.from_object('config')

from app import views
from app import models