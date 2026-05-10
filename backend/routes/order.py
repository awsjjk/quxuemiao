from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Order, Demand, Parent, Tutor

order_bp = Blueprint('order', __name__)


@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.user_type != 1:
        return jsonify({"code": 403, "msg": "仅家长可创建订单"}), 403

    parent = Parent.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    demand_id = data.get('demand_id')
    tutor_id = data.get('tutor_id')

    demand = Demand.query.get(demand_id)
    if not demand or demand.parent_id != parent.id:
        return jsonify({"code": 404, "msg": "需求不存在"}), 404

    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        return jsonify({"code": 404, "msg": "家教不存在"}), 404

    order = Order(
        demand_id=demand_id,
        parent_id=parent.id,
        tutor_id=tutor_id,
        total_amount=data.get('total_amount', 0),
        status=2,  # 进行中（跳过支付）
        remark=data.get('remark', ''),
    )
    db.session.add(order)
    demand.status = 3  # 已完成
    db.session.commit()

    return jsonify({
        "code": 200, "msg": "订单创建成功", "data": {"id": order.id}
    }), 200


@order_bp.route('/list', methods=['GET'])
@jwt_required()
def list_orders():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user.user_type == 1:
        parent = Parent.query.filter_by(user_id=user_id).first()
        orders = Order.query.filter_by(parent_id=parent.id).order_by(Order.create_time.desc()).all()
    elif user.user_type == 2:
        tutor = Tutor.query.filter_by(user_id=user_id).first()
        orders = Order.query.filter_by(tutor_id=tutor.id).order_by(Order.create_time.desc()).all()
    else:
        orders = Order.query.order_by(Order.create_time.desc()).all()

    result = [{
        'id': o.id, 'demand_id': o.demand_id, 'parent_id': o.parent_id,
        'tutor_id': o.tutor_id, 'total_amount': float(o.total_amount) if o.total_amount else 0,
        'status': o.status, 'remark': o.remark,
        'create_time': o.create_time.isoformat()
    } for o in orders]

    return jsonify({"code": 200, "data": result}), 200


@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def detail(order_id):
    o = Order.query.get(order_id)
    if not o:
        return jsonify({"code": 404, "msg": "订单不存在"}), 404

    tutor = Tutor.query.get(o.tutor_id)
    tutor_user = User.query.get(tutor.user_id) if tutor else None
    demand = Demand.query.get(o.demand_id)

    return jsonify({"code": 200, "data": {
        'id': o.id, 'demand_id': o.demand_id,
        'demand_title': demand.title if demand else '',
        'tutor_id': o.tutor_id,
        'tutor_name': tutor.real_name if tutor else '',
        'tutor_school': tutor.school if tutor else '',
        'tutor_phone': tutor_user.phone if tutor_user else '',
        'total_amount': float(o.total_amount) if o.total_amount else 0,
        'status': o.status, 'remark': o.remark,
        'create_time': o.create_time.isoformat()
    }}), 200


@order_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_status(order_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    o = Order.query.get(order_id)
    if not o:
        return jsonify({"code": 404, "msg": "订单不存在"}), 404

    data = request.get_json()
    new_status = data.get('status')

    valid_transitions = {2: [3, 4], 3: [4]}
    if new_status not in valid_transitions.get(o.status, []):
        return jsonify({"code": 400, "msg": "无效的状态变更"}), 400

    if new_status == 3 and user.user_type not in (1, 3):
        return jsonify({"code": 403, "msg": "仅家长或管理员可确认完成"}), 403

    o.status = new_status
    o.update_time = datetime.now()

    if new_status == 3:
        demand = Demand.query.get(o.demand_id)
        if demand:
            demand.status = 3

    db.session.commit()
    return jsonify({"code": 200, "msg": "状态更新成功"}), 200
