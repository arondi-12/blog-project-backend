from datetime import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  

    def set_password(self, password):
        if not self.is_valid_password(password):
            raise ValueError(
                "Password must be at least 8 characters long, include a letter, a number, and a special character."
            )
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def is_valid_password(password):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, password) is not None

    def is_admin(self):
        return self.role == 'admin'
    
    def is_author(self):
        return self.role == 'author'

    def get_role(self):
        return self.role



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(255), nullable=True)

    author = db.relationship('User', backref=db.backref('posts', lazy=True))
