# setting database models
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from app import app
import db
from flask_login import LoginManager
from flask import Flask

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    confirm_password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin' or 'client'

    def __repr__(self):
        return f'<User {self.username}>'
 
# class Policy(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     policy_name = db.Column(db.String(150), nullable=False)

#     #policy_details = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<Policy {self.policy_name}>'

# class Update(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), nullable=False)
#     content = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<Update {self.title}>'

# class Reccommendations(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     policy_name = db.Column(db.String(150), nullable=False)
#     policy_details = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<Reccommendations {self.policy_name}>'

# class Comments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<Comment {self.id} by User {self.user_id}>'