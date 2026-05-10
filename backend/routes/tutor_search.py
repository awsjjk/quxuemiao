from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Tutor

tutor_search_bp = Blueprint('tutor_search', __name__)


@tutor_search_bp.route('/search', methods=['GET'])
@jwt_required()
def search_tutors():
    query = Tutor.query.join(User, Tutor.user_id == User.id)

    subject = request.args.get('subject', '').strip()
    school = request.args.get('school', '').strip()
    education = request.args.get('education', '').strip()
    location = request.args.get('location', '').strip()
    min_rate = request.args.get('min_rate', type=float)
    max_rate = request.args.get('max_rate', type=float)
    min_exp = request.args.get('min_exp', type=int)
    verified_only = request.args.get('verified_only', '').strip()

    if subject:
        query = query.filter(Tutor.skills.contains(subject))
    if school:
        query = query.filter(Tutor.school.contains(school))
    if education:
        query = query.filter(Tutor.education == education)
    if location:
        query = query.filter(Tutor.location == location)
    if min_rate is not None:
        query = query.filter(Tutor.hourly_rate >= min_rate)
    if max_rate is not None:
        query = query.filter(Tutor.hourly_rate <= max_rate)
    if min_exp is not None:
        query = query.filter(Tutor.teaching_exp >= min_exp)
    if verified_only == '1':
        query = query.filter(Tutor.verification_status == 2)

    tutors = query.limit(50).all()
    result = []
    for t in tutors:
        user = User.query.get(t.user_id)
        result.append({
            "tutor_id": t.id,
            "user_id": t.user_id,
            "username": user.username if user else '',
            "real_name": t.real_name,
            "school": t.school,
            "major": t.major,
            "education": t.education,
            "grade": t.grade,
            "teaching_exp": t.teaching_exp,
            "hourly_rate": float(t.hourly_rate) if t.hourly_rate else None,
            "location": t.location,
            "skills": t.skills or [],
            "introduction": t.introduction,
            "available_time": t.available_time or [],
            "verification_status": t.verification_status,
        })
    return jsonify({"code": 200, "data": result}), 200
