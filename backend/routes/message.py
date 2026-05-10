from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Parent, Tutor, Message

message_bp = Blueprint('message', __name__)


@message_bp.route('/send', methods=['POST'])
@jwt_required()
def send():
    sender_id = int(get_jwt_identity())
    data = request.get_json()
    receiver_username = data.get('receiver_username', '').strip()
    if not receiver_username:
        return jsonify({"code": 400, "msg": "请提供接收者用户名"}), 400

    receiver = User.query.filter_by(username=receiver_username).first()
    if not receiver:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404
    if receiver.id == sender_id:
        return jsonify({"code": 400, "msg": "不能给自己发消息"}), 400

    msg = Message(
        sender_id=sender_id,
        receiver_id=receiver.id,
        content=data.get('content', ''),
        msg_type=data.get('msg_type', 1),
        resource_url=data.get('resource_url', ''),
        is_read=False
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"code": 200, "msg": "发送成功", "data": {"id": msg.id}}), 200


@message_bp.route('/search_user', methods=['GET'])
@jwt_required()
def search_user():
    username = request.args.get('username', '').strip()
    current_user_id = int(get_jwt_identity())
    if not username:
        return jsonify({"code": 400, "msg": "请提供用户名"}), 400
    user = User.query.filter(
        User.username == username,
        User.id != current_user_id
    ).first()
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404
    role_id = None
    real_name = None
    if user.user_type == 1:
        p = Parent.query.filter_by(user_id=user.id).first()
        if p:
            real_name = p.real_name
            role_id = p.id
    elif user.user_type == 2:
        t = Tutor.query.filter_by(user_id=user.id).first()
        if t:
            real_name = t.real_name
            role_id = t.id

    return jsonify({"code": 200, "data": {
        "id": user.id,
        "username": user.username,
        "user_type": user.user_type,
        "real_name": real_name or user.username,
        "role_id": role_id,
        "role_text": {1: "家长", 2: "家教", 3: "管理员"}.get(user.user_type, "")
    }}), 200


@message_bp.route('/conversations', methods=['GET'])
@jwt_required()
def conversations():
    user_id = int(get_jwt_identity())
    sent = db.session.query(Message.receiver_id).filter(Message.sender_id == user_id).distinct().all()
    received = db.session.query(Message.sender_id).filter(Message.receiver_id == user_id).distinct().all()
    partner_ids = set(r[0] for r in sent) | set(r[0] for r in received)
    result = []
    for pid in partner_ids:
        partner = User.query.get(pid)
        last_msg = Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == pid)) |
            ((Message.sender_id == pid) & (Message.receiver_id == user_id))
        ).order_by(Message.create_time.desc()).first()
        unread = Message.query.filter_by(sender_id=pid, receiver_id=user_id, is_read=False).count()
        result.append({
            'partner_id': pid,
            'partner_name': partner.username if partner else '未知',
            'partner_role': {1: '家长', 2: '家教', 3: '管理员'}.get(partner.user_type, '') if partner else '',
            'last_message': last_msg.content[:50] if last_msg else '',
            'last_time': last_msg.create_time.isoformat() if last_msg else None,
            'unread': unread
        })
    result.sort(key=lambda x: x['last_time'] or '', reverse=True)
    return jsonify({"code": 200, "data": result}), 200


@message_bp.route('/chat/<int:partner_id>', methods=['GET'])
@jwt_required()
def chat(partner_id):
    user_id = int(get_jwt_identity())
    msgs = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == partner_id)) |
        ((Message.sender_id == partner_id) & (Message.receiver_id == user_id))
    ).order_by(Message.create_time.asc()).limit(100).all()

    Message.query.filter_by(sender_id=partner_id, receiver_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()

    result = [{
        'id': m.id, 'sender_id': m.sender_id, 'receiver_id': m.receiver_id,
        'content': m.content, 'msg_type': m.msg_type, 'resource_url': m.resource_url,
        'is_read': m.is_read, 'create_time': m.create_time.isoformat()
    } for m in msgs]
    return jsonify({"code": 200, "data": result}), 200
