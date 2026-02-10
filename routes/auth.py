from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# 原理：创建一个蓝图对象。'auth' 是它的名字
auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()

    if user:
        # 原理：根据用户 ID 创建一个真正的加密 Token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "code": 200,
            "msg": "登录成功",
            "token": access_token,  # 发送加密后的长字符串
            "username": user.username
        })
    return jsonify({"code": 401, "msg": "报错"}), 401


@auth_bp.route('/user_info', methods=['GET'])
@jwt_required()  # 原理：这个装饰器会自动检查 Header 里的 Token 是否合法
def get_info():
    # 原理：从加密的 Token 中反向解析出当时存入的 user_id
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify({
        "code": 200,
        "data": {
            "username": user.username,
            "phone": user.phone,
            "email": user.email
        }
    })
    # 如果令牌不对，返回 403 (禁止访问)
    # return jsonify({"code": 403, "msg": "无效的令牌"}), 403


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 获取前端传来的字段
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    user_type = data.get('user_type', 'regular')  # 默认为普通用户

    # 1. 基本校验
    if not username or not password:
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    # 2. 查重：看看数据库里有没有同名的
    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "msg": "用户名已存在"}), 400

    # 3. 存入 SQLite 数据库
    try:
        new_user = User(
            username=username,
            password=password,  # 暂时明文，下一步再学加密
            phone=phone,
            email=email
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"code": 200, "msg": "注册成功！请前往登录"}), 200
    except Exception as e:
        db.session.rollback()  # 出错时回滚，保证数据库安全
        return jsonify({"code": 500, "msg": "系统错误"}), 500


@auth_bp.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    # 1. 获取当前登录用户的 ID（从 Token 解析）
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "用户不存在"}), 404

    # 2. 获取前端传来的新数据
    data = request.get_json()

    # 3. 更新字段（如果前端传了新值就改，没传就保持原样）
    if 'phone' in data:
        user.phone = data['phone']
    if 'email' in data:
        user.email = data['email']

    # 原理：SQLAlchemy 会监控对象的属性变化
    # 我们只需 commit，它会自动生成 UPDATE 语句发送给 SQLite
    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "资料更新成功"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "更新失败"}), 500