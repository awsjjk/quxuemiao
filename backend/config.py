import os

basedir = os.path.abspath(os.path.dirname(__file__))

# MySQL 连接配置
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
MYSQL_DB = os.environ.get('MYSQL_DB', 'quxuemiao')

SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    '?charset=utf8mb4'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'quxuemiao-secret-key-change-in-prod')
JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
