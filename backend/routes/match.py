import json
import threading
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Demand, Tutor, Parent

match_bp = Blueprint('match', __name__)

_task_status = {}


def _run_match(demand_id, app):
    """后台执行匹配任务"""
    try:
        with app.app_context():
            _task_status[demand_id] = 'processing'

            demand = Demand.query.get(demand_id)
            if not demand:
                _task_status[demand_id] = 'failed'
                return

            demand.match_status = 'processing'
            db.session.commit()

            # 1. 规则初筛
            candidates_query = Tutor.query.filter(
                Tutor.verification_status >= 1
            )
            if demand.location:
                candidates_query = candidates_query.filter(Tutor.location == demand.location)
            if demand.budget:
                candidates_query = candidates_query.filter(Tutor.hourly_rate <= float(demand.budget) * 1.5)
            candidates = candidates_query.limit(50).all()

            if not candidates:
                demand.match_result = []
                demand.match_status = 'done'
                demand.match_time = datetime.now()
                db.session.commit()
                _task_status[demand_id] = 'done'
                return

            # 2. 构造候选数据
            candidate_dicts = []
            for t in candidates:
                candidate_dicts.append({
                    'id': t.id, 'real_name': t.real_name or '', 'school': t.school or '',
                    'major': t.major or '', 'skills': t.skills or [], 'teaching_exp': t.teaching_exp or 0,
                    'introduction': t.introduction or '', 'location': t.location or '',
                    'available_time': t.available_time or [], 'hourly_rate': float(t.hourly_rate or 0),
                    'education': t.education or '', 'grade': t.grade or '',
                    'verification_status': t.verification_status
                })

            # 3. AI 匹配
            demand_dict = {
                'subject': demand.subject or '', 'grade': demand.grade or '',
                'location': demand.location or '', 'budget': float(demand.budget) if demand.budget else 0,
                'time_slots': demand.time_slots or [], 'description': demand.description or '',
                'requirements': demand.requirements or '', 'tags': demand.tags or []
            }

            from ai_module.agent import MatchAgent
            agent = MatchAgent()
            results = agent.match(demand_dict, candidate_dicts)

            # 4. 写入结果
            demand.match_result = results
            demand.match_status = 'done'
            demand.match_time = datetime.now()
            db.session.commit()
            _task_status[demand_id] = 'done'

    except Exception as e:
        print(f"Match error for demand {demand_id}: {e}")
        try:
            with app.app_context():
                demand = Demand.query.get(demand_id)
                if demand:
                    demand.match_status = 'failed'
                    db.session.commit()
        except:
            pass
        _task_status[demand_id] = 'failed'


@match_bp.route('/run', methods=['POST'])
@jwt_required()
def run_match():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.user_type != 1:
        return jsonify({"code": 403, "msg": "仅家长可触发匹配"}), 403

    parent = Parent.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    demand_id = data.get('demand_id')

    demand = Demand.query.get(demand_id)
    if not demand or demand.parent_id != parent.id:
        return jsonify({"code": 404, "msg": "需求不存在或无权操作"}), 404

    # Get the Flask app instance for thread context
    from flask import current_app
    app = current_app._get_current_object()

    demand.match_status = 'pending'
    db.session.commit()

    thread = threading.Thread(target=_run_match, args=(demand_id, app), daemon=True)
    thread.start()

    return jsonify({
        "code": 200,
        "msg": "匹配已启动",
        "data": {"demand_id": demand_id, "status": "pending"}
    }), 200


@match_bp.route('/result/<int:demand_id>', methods=['GET'])
@jwt_required()
def get_result(demand_id):
    demand = Demand.query.get(demand_id)
    if not demand:
        return jsonify({"code": 404, "msg": "需求不存在"}), 404

    return jsonify({
        "code": 200,
        "data": {
            "demand_id": demand.id,
            "status": demand.match_status,
            "result": demand.match_result,
            "match_time": demand.match_time.isoformat() if demand.match_time else None
        }
    }), 200
