from flask_sqlalchemy import SQLAlchemy

# 原理：在这里只定义 db 对象，不给它关联具体的 app
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))