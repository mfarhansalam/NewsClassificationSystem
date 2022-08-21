from app import db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


feedback = db.Table('feedback',
    db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('sentiment_id',db.Integer,db.ForeignKey('sentiment.id')),
    
    )


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    sentiments = db.relationship("Sentiment",secondary=feedback)
    def __init__(self,name, email, password):
        
        self.name = name
        self.email = email
        self.password = password


class Sentiment(db.Model):
    __tablename__ = 'sentiment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), unique=True)
    label = db.Column(db.String(1000), unique=True) 

    def __init__(self,text, label ):
        self.text = text
        self.label = label