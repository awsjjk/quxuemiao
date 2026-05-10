import sys
import logging
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_ACCESS_TOKEN_EXPIRES

# 配置日志 — 确保每次请求都打印到控制台
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES

db.init_app(app)
jwt = JWTManager(app)

# 记录每次请求
@app.before_request
def log_request():
    app.logger.info(f"--> {request.method} {request.path}")

from routes.auth import auth_bp
from routes.demand import demand_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(demand_bp, url_prefix='/api/demand')

from routes.match import match_bp
app.register_blueprint(match_bp, url_prefix='/api/match')

from routes.order import order_bp
app.register_blueprint(order_bp, url_prefix='/api/order')

from routes.rating import rating_bp
app.register_blueprint(rating_bp, url_prefix='/api/rating')

from routes.course import course_bp
app.register_blueprint(course_bp, url_prefix='/api/course')

from routes.message import message_bp
app.register_blueprint(message_bp, url_prefix='/api/message')

from routes.resource import resource_bp
app.register_blueprint(resource_bp, url_prefix='/api/resource')

from routes.payment import payment_bp
app.register_blueprint(payment_bp, url_prefix='/api/payment')

from routes.tutor_search import tutor_search_bp
app.register_blueprint(tutor_search_bp, url_prefix='/api/tutor')

from routes.ai_assistant import ai_assistant_bp
app.register_blueprint(ai_assistant_bp, url_prefix='/api/ai_assistant')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
