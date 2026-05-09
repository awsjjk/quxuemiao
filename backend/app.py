from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_ACCESS_TOKEN_EXPIRES

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES

db.init_app(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
