from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Demand, Parent

demand_bp = Blueprint('demand', __name__)


@demand_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.user_type != 1:
        return jsonify({"code": 403, "msg": "仅家长可发布需求"}), 403

    parent = Parent.query.filter_by(user_id=user_id).first()
    data = request.get_json()

    demand = Demand(
        parent_id=parent.id,
        title=data.get('title', ''),
        subject=data.get('subject', ''),
        grade=data.get('grade', ''),
        description=data.get('description', ''),
        address=data.get('address', ''),
        location=data.get('location', ''),
        time_slots=data.get('time_slots', []),
        duration=data.get('duration'),
        frequency=data.get('frequency', ''),
        budget=data.get('budget'),
        requirements=data.get('requirements', ''),
        tags=data.get('tags', []),
        is_urgent=data.get('is_urgent', False),
        status=1
    )
    db.session.add(demand)
    db.session.commit()
    return jsonify({"code": 200, "msg": "需求发布成功", "data": {"id": demand.id}}), 200


@demand_bp.route('/list', methods=['GET'])
@jwt_required()
def list_demands():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.user_type == 1:
        parent = Parent.query.filter_by(user_id=user_id).first()
        demands = Demand.query.filter_by(parent_id=parent.id).order_by(Demand.create_time.desc()).all()
    else:
        return jsonify({"code": 400, "msg": "暂不支持此角色查看需求"}), 400

    result = [{
        'id': d.id, 'title': d.title, 'subject': d.subject,
        'grade': d.grade, 'location': d.location, 'budget': float(d.budget) if d.budget else None,
        'status': d.status, 'tags': d.tags, 'is_urgent': d.is_urgent,
        'match_status': d.match_status, 'create_time': d.create_time.isoformat()
    } for d in demands]
    return jsonify({"code": 200, "data": result}), 200


@demand_bp.route('/<int:demand_id>', methods=['GET'])
@jwt_required()
def detail(demand_id):
    d = Demand.query.get(demand_id)
    if not d:
        return jsonify({"code": 404, "msg": "需求不存在"}), 404
    return jsonify({"code": 200, "data": {
        'id': d.id, 'title': d.title, 'subject': d.subject,
        'grade': d.grade, 'description': d.description, 'address': d.address,
        'location': d.location, 'time_slots': d.time_slots,
        'duration': d.duration, 'frequency': d.frequency,
        'budget': float(d.budget) if d.budget else None,
        'requirements': d.requirements, 'tags': d.tags,
        'is_urgent': d.is_urgent, 'status': d.status,
        'match_status': d.match_status, 'match_result': d.match_result,
        'create_time': d.create_time.isoformat()
    }}), 200


@demand_bp.route('/<int:demand_id>', methods=['PUT'])
@jwt_required()
def update(demand_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    parent = Parent.query.filter_by(user_id=user_id).first()
    d = Demand.query.get(demand_id)
    if not d or d.parent_id != parent.id:
        return jsonify({"code": 404, "msg": "需求不存在或无权修改"}), 404
    if d.status not in (1,):
        return jsonify({"code": 400, "msg": "当前状态不可修改"}), 400

    data = request.get_json()
    updatable = ['title', 'subject', 'grade', 'description', 'address', 'location',
                 'time_slots', 'duration', 'frequency', 'budget', 'requirements', 'tags', 'is_urgent']
    for field in updatable:
        if field in data:
            setattr(d, field, data[field])

    if data.get('cancel'):
        d.status = 4  # 已取消

    db.session.commit()
    return jsonify({"code": 200, "msg": "需求修改成功"}), 200
