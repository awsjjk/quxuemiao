from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

db.init_app(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
