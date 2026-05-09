from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, User, Parent, Tutor
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

    # user_type 约定：1 为普通用户/家长，2 为家教（根据你 models.py 的定义）
    # 或者前端传 'parent', 'tutor'，这里做个转换
    raw_user_type = data.get('user_type', 1)

    # 1. 基本校验
    if not username or not password:
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    # 2. 查重：用户名、手机号、邮箱通常都是唯一的
    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "msg": "用户名已存在"}), 400

    if phone and User.query.filter_by(phone=phone).first():
        return jsonify({"code": 400, "msg": "该手机号已被注册"}), 400

    # 3. 存入数据库 (使用事务处理多表关联)
    try:
        # 创建基础用户记录
        new_user = User(
            username=username,
            password=password,  # 建议之后使用 generate_password_hash(password)
            phone=phone,
            email=email,
            user_type=raw_user_type,
            status=1,  # 默认激活状态
            create_time=datetime.now()
        )
        db.session.add(new_user)
        # flush 会模拟提交获取自增 ID，但不会真正结束事务
        db.session.flush()

        # 根据用户类型，初始化对应的身份表
        if raw_user_type == 1:
            # 初始化家长档案
            new_parent = Parent(user_id=new_user.id)
            db.session.add(new_parent)
        elif raw_user_type == 2:
            # 初始化家教档案
            new_tutor = Tutor(
                user_id=new_user.id,
                verification_status=0  # 初始为未认证
            )
            db.session.add(new_tutor)

        # 真正提交到数据库
        db.session.commit()
        return jsonify({"code": 200, "msg": "注册成功！请前往登录"}), 200

    except Exception as e:
        db.session.rollback()  # 只要中间任何一个环节出错（如身份表创建失败），全部回滚
        # 打印错误原因方便调试
        print(f"Registration Error: {e}")
        return jsonify({"code": 500, "msg": "系统错误，注册失败"}), 500


@auth_bp.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "msg": "请求数据为空"}), 400

    # 更新 User 基础字段
    for field in ['phone', 'email', 'avatar', 'sex', 'birthday']:
        if field in data:
            setattr(user, field, data[field])

    # 更新角色详情
    if user.user_type == 1:  # 家长
        parent = Parent.query.filter_by(user_id=user.id).first()
        if parent:
            for field in ['real_name', 'address', 'location', 'children_info', 'preference']:
                if field in data:
                    setattr(parent, field, data[field])
    elif user.user_type == 2:  # 家教
        tutor = Tutor.query.filter_by(user_id=user.id).first()
        if tutor:
            for field in ['real_name', 'school', 'major', 'grade', 'education',
                          'skills', 'teaching_exp', 'introduction', 'certificates',
                          'location', 'available_time', 'hourly_rate']:
                if field in data:
                    setattr(tutor, field, data[field])

    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "资料更新成功"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": f"更新失败: {str(e)}"}), 500
