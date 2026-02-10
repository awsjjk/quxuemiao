from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------------------------------------------------
# 1. 用户与身份 (User, Parent, Tutor)
# ---------------------------------------------------------

class User(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    avatar = db.Column(db.String(255))
    user_type = db.Column(db.SmallInteger, default=1)
    sex = db.Column(db.SmallInteger, default=0)
    birthday = db.Column(db.Date)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime)
    qq_openid = db.Column(db.String(128), unique=True)
    wechat_openid = db.Column(db.String(128), unique=True)
    linked_account_id = db.Column(db.Integer)

class Parent(db.Model):
    __tablename__ = 'parent_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    real_name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    location = db.Column(db.String(100))
    children_info = db.Column(db.JSON)
    preference = db.Column(db.JSON)

class Tutor(db.Model):
    __tablename__ = 'tutor_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    real_name = db.Column(db.String(50))
    id_card = db.Column(db.String(128))
    school = db.Column(db.String(100))
    major = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    education = db.Column(db.String(50))
    skills = db.Column(db.JSON)
    teaching_exp = db.Column(db.Integer)
    introduction = db.Column(db.Text)
    certificates = db.Column(db.JSON)
    location = db.Column(db.String(100))
    available_time = db.Column(db.JSON)
    hourly_rate = db.Column(db.Numeric(10, 2))
    verification_status = db.Column(db.SmallInteger, default=0) # 0:未认证, 1:审核中, 2:已认证

# ---------------------------------------------------------
# 2. 核心业务 (Demand, Order, Course, Rating)
# ---------------------------------------------------------

class Demand(db.Model):
    __tablename__ = 'demand_info'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_info.id'), nullable=False)
    title = db.Column(db.String(100))
    subject = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    location = db.Column(db.String(100))
    time_slots = db.Column(db.JSON)
    duration = db.Column(db.Integer)
    frequency = db.Column(db.String(50))
    budget = db.Column(db.Numeric(10, 2))
    requirements = db.Column(db.Text)
    status = db.Column(db.Integer, default=1) # 1:招募中, 2:已匹配, 3:已完成, 4:已取消
    create_time = db.Column(db.DateTime, default=datetime.now)
    tags = db.Column(db.JSON)
    is_urgent = db.Column(db.Boolean, default=False)
    auction_enabled = db.Column(db.Boolean, default=False)

class Order(db.Model):
    __tablename__ = 'order_info'
    id = db.Column(db.Integer, primary_key=True)
    demand_id = db.Column(db.Integer, db.ForeignKey('demand_info.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_info.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_info.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Integer, default=1) # 1:待支付, 2:进行中, 3:已完成, 4:已取消, 5:退款中, 6:已退款
    payment_status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    remark = db.Column(db.String(255))

class Course(db.Model):
    __tablename__ = 'course_record'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_info.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_info.id'))
    course_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    actual_duration = db.Column(db.Integer)
    content = db.Column(db.Text)
    homework = db.Column(db.Text)
    knowledge_points = db.Column(db.JSON)
    student_performance = db.Column(db.Text)
    tutor_feedback = db.Column(db.Text)
    parent_feedback = db.Column(db.Text)
    status = db.Column(db.Integer, default=1) # 1:待确认, 2:已确认
    create_time = db.Column(db.DateTime, default=datetime.now)

class Rating(db.Model):
    __tablename__ = 'rating_info'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_info.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_info.id'))
    teaching_score = db.Column(db.Integer)
    attitude_score = db.Column(db.Integer)
    punctuality_score = db.Column(db.Integer)
    overall_score = db.Column(db.Integer)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

# ---------------------------------------------------------
# 3. 辅助功能 (Message, Payment, TeachingResource)
# ---------------------------------------------------------

class Message(db.Model):
    __tablename__ = 'message_info'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    content = db.Column(db.Text)
    msg_type = db.Column(db.Integer, default=1) # 1:文本, 2:图片, 3:语音
    resource_url = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class Payment(db.Model):
    __tablename__ = 'payment_record'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2))
    payment_method = db.Column(db.String(50)) # 微信, 支付宝等
    transaction_id = db.Column(db.String(128), unique=True)
    status = db.Column(db.Integer, default=1) # 1:待支付, 2:成功, 3:失败, 4:已退款
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)

class TeachingResource(db.Model):
    __tablename__ = 'teaching_resource'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    subject = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    resource_type = db.Column(db.Integer) # 1:课件, 2:题库, 3:教案
    file_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    upload_user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    download_count = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=1) # 0:待审核, 1:已上线, 2:已下线