import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db,User
from routes.auth import auth_bp  # 导入刚才写的蓝图

app = Flask(__name__)
CORS(app)

# 配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dev_database.db')
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

# 原理：将 db 绑定到当前的 app 上
db.init_app(app)
jwt = JWTManager(app)

# 原理：注册蓝图，并给它所有的路径统一加个前缀 '/api'
app.register_blueprint(auth_bp, url_prefix='/api')

with app.app_context():
    print("数据库连接地址:", app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()
    print("表已尝试创建！")

if __name__ == '__main__':

    app.run(debug=True)