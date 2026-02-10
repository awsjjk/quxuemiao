from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 原理：在这里只定义 db 对象，不给它关联具体的 app
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_info'  # Explicitly naming the table

    # Basic Information
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Increased length for hashed passwords
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(96), unique=True)
    avatar = db.Column(db.String(255))  # URL or file path

    # User Profile & Status
    user_type = db.Column(db.SmallInteger, default=1)  # e.g., 1 for regular, 2 for admin
    sex = db.Column(db.SmallInteger, default=0)  # e.g., 0: unknown, 1: male, 2: female
    birthday = db.Column(db.Date)
    status = db.Column(db.SmallInteger, default=1)  # e.g., 1: active, 0: disabled

    # Timestamps
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime)

    # Third-party Bindings & Account Linking
    qq_openid = db.Column(db.String(128), unique=True)
    wechat_openid = db.Column(db.String(128), unique=True)
    linked_account_id = db.Column(db.Integer)  # To associate with another user ID if needed

    def __repr__(self):
        return f'<User {self.username}>'