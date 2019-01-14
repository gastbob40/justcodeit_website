# This file contains the different models (data base) of the site

# Import
from flask_login import UserMixin
from site import db, login_manager

# Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Class (db)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    permission = db.Column(db.String(300), nullable=False)
    

    def __repr__(self):
        return self.username
