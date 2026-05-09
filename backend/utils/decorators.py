from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User


def role_required(*roles):
    """roles: 1=家长, 2=家教, 3=管理员"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if not user or user.user_type not in roles:
                from flask import jsonify
                return jsonify({"code": 403, "msg": "权限不足"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
