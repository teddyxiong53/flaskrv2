from flaskrv2 import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128)) # storage hash value
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
