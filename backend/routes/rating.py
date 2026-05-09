from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Rating, Order, Parent, Tutor

rating_bp = Blueprint('rating', __name__)


@rating_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.user_type != 1:
        return jsonify({"code": 403, "msg": "仅家长可提交评价"}), 403

    parent = Parent.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    order_id = data.get('order_id')

    order = Order.query.get(order_id)
    if not order or order.parent_id != parent.id:
        return jsonify({"code": 404, "msg": "订单不存在或无权评价"}), 404

    existing = Rating.query.filter_by(order_id=order_id).first()
    if existing:
        return jsonify({"code": 400, "msg": "该订单已评价"}), 400

    teaching = data.get('teaching_score', 5)
    attitude = data.get('attitude_score', 5)
    punctuality = data.get('punctuality_score', 5)
    overall = data.get('overall_score') or (teaching + attitude + punctuality) // 3

    rating = Rating(
        order_id=order_id,
        parent_id=parent.id,
        tutor_id=order.tutor_id,
        teaching_score=teaching,
        attitude_score=attitude,
        punctuality_score=punctuality,
        overall_score=overall,
        comment=data.get('comment', ''),
    )
    db.session.add(rating)
    db.session.commit()

    return jsonify({"code": 200, "msg": "评价提交成功", "data": {"id": rating.id}}), 200


@rating_bp.route('/tutor/<int:tutor_id>', methods=['GET'])
def tutor_ratings(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        return jsonify({"code": 404, "msg": "家教不存在"}), 404

    ratings = Rating.query.filter_by(tutor_id=tutor_id)\
        .order_by(Rating.create_time.desc()).limit(20).all()

    result = []
    for r in ratings:
        parent = Parent.query.get(r.parent_id)
        parent_user = User.query.get(parent.user_id) if parent else None
        result.append({
            'id': r.id, 'teaching_score': r.teaching_score,
            'attitude_score': r.attitude_score, 'punctuality_score': r.punctuality_score,
            'overall_score': r.overall_score, 'comment': r.comment,
            'parent_name': parent_user.username if parent_user else '匿名',
            'create_time': r.create_time.isoformat()
        })

    avg = db.session.query(db.func.avg(Rating.overall_score))\
        .filter(Rating.tutor_id == tutor_id).scalar()
    avg_score = round(float(avg), 1) if avg else 0

    return jsonify({
        "code": 200,
        "data": {
            "tutor_id": tutor_id,
            "average_score": avg_score,
            "total_count": Rating.query.filter_by(tutor_id=tutor_id).count(),
            "ratings": result
        }
    }), 200
