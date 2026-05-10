"""向 parent_info 和 tutor_info 表各插入 10 条测试数据"""
from app import app
from models import db, User, Parent, Tutor

with app.app_context():
    # 清理旧测试数据（可选）
    User.query.filter(User.username.like('test_parent_%')).delete()
    User.query.filter(User.username.like('test_tutor_%')).delete()
    db.session.commit()

    parents = []
    tutors = []

    parent_data = [
        {"real_name": "张大明", "address": "南开区卫津路94号", "location": "南开区",
         "children_info": [{"name": "小明", "grade": "三年级", "age": 9}, {"name": "小红", "grade": "一年级", "age": 7}],
         "preference": {"subjects": ["数学", "英语"], "times": ["周末上午", "工作日晚上"]}},
        {"real_name": "李丽萍", "address": "和平区南京路128号", "location": "和平区",
         "children_info": [{"name": "小宇", "grade": "高一", "age": 15}],
         "preference": {"subjects": ["物理", "化学"], "times": ["周末下午"]}},
        {"real_name": "王建国", "address": "河西区友谊路16号", "location": "河西区",
         "children_info": [{"name": "小芳", "grade": "初二", "age": 13}, {"name": "小龙", "grade": "五年级", "age": 11}],
         "preference": {"subjects": ["语文", "英语", "历史"], "times": ["每天"]}},
        {"real_name": "赵秀英", "address": "河东区津塘路55号", "location": "河东区",
         "children_info": [{"name": "小雨", "grade": "高二", "age": 16}],
         "preference": {"subjects": ["数学", "生物"], "times": ["周末晚上", "周末上午"]}},
        {"real_name": "陈文华", "address": "河北区中山路88号", "location": "河北区",
         "children_info": [{"name": "小杰", "grade": "四年级", "age": 10}],
         "preference": {"subjects": ["英语", "其他外语"], "times": ["工作日晚上"]}},
        {"real_name": "刘美玲", "address": "红桥区丁字沽1号", "location": "红桥区",
         "children_info": [{"name": "小慧", "grade": "初三", "age": 14}, {"name": "小刚", "grade": "六年级", "age": 12}],
         "preference": {"subjects": ["化学", "物理", "数学"], "times": ["周末上午"]}},
        {"real_name": "孙志强", "address": "东丽区津塘公路100号", "location": "东丽区",
         "children_info": [{"name": "小伟", "grade": "高三", "age": 17}],
         "preference": {"subjects": ["政治", "历史", "地理"], "times": ["每天"]}},
        {"real_name": "周雪琴", "address": "西青区杨柳青镇12号", "location": "西青区",
         "children_info": [{"name": "小婷", "grade": "二年级", "age": 8}],
         "preference": {"subjects": ["语文", "数学"], "times": ["周末上午", "周末下午"]}},
        {"real_name": "吴建军", "address": "津南区咸水沽镇8号", "location": "津南区",
         "children_info": [{"name": "小豪", "grade": "初一", "age": 12}, {"name": "小琪", "grade": "三年级", "age": 9}],
         "preference": {"subjects": ["英语", "其他外语"], "times": ["周末晚上"]}},
        {"real_name": "郑桂芳", "address": "北辰区果园新村20号", "location": "北辰区",
         "children_info": [{"name": "小乐", "grade": "五年级", "age": 11}],
         "preference": {"subjects": ["生物", "地理", "化学"], "times": ["工作日晚上", "周末下午"]}},
    ]

    tutor_data = [
        {"real_name": "王老师", "id_card": "120101199001011234", "school": "南开大学", "major": "数学与应用数学",
         "grade": "研二", "education": "硕士", "skills": ["数学", "物理"], "teaching_exp": 3,
         "introduction": "南开大学数学专业研究生，有3年家教经验，擅长初高中数学物理辅导，教学耐心细致。", "certificates": ["教师资格证", "CET-6"],
         "location": "南开区", "available_time": ["一_晚上", "三_晚上", "六_上午", "六_下午", "日_上午", "日_下午"],
         "hourly_rate": 120, "verification_status": 2},
        {"real_name": "李老师", "id_card": "120102199503152345", "school": "天津大学", "major": "英语",
         "grade": "大三", "education": "本科", "skills": ["英语", "语文"], "teaching_exp": 2,
         "introduction": "天大英语专业在读，英语专八水平，口语流利，曾辅导多名学生通过英语等级考试。", "certificates": ["CET-6", "英语专八"],
         "location": "和平区", "available_time": ["二_晚上", "四_晚上", "六_上午", "日_下午", "日_晚上"],
         "hourly_rate": 100, "verification_status": 2},
        {"real_name": "张老师", "id_card": "120103198807083456", "school": "天津师范大学", "major": "化学教育",
         "grade": "已毕业", "education": "本科", "skills": ["化学", "生物"], "teaching_exp": 5,
         "introduction": "多年中学化学教学经验，熟悉初高中化学教材和考试重点，善于归纳总结解题方法。", "certificates": ["教师资格证"],
         "location": "河西区", "available_time": ["一_晚上", "三_晚上", "五_晚上", "六_上午", "六_下午", "日_上午"],
         "hourly_rate": 130, "verification_status": 2},
        {"real_name": "刘老师", "id_card": "120104199201014567", "school": "河北工业大学", "major": "物理学",
         "grade": "研一", "education": "硕士", "skills": ["物理", "数学"], "teaching_exp": 1,
         "introduction": "物理学研究生，基础扎实，对物理教学有独到见解，善于用通俗易懂的方式讲解复杂概念。", "certificates": ["CET-4"],
         "location": "河东区", "available_time": ["四_晚上", "五_晚上", "六_下午", "六_晚上", "日_下午"],
         "hourly_rate": 110, "verification_status": 1},
        {"real_name": "赵老师", "id_card": "120105199303025678", "school": "天津财经大学", "major": "英语翻译",
         "grade": "大一", "education": "本科", "skills": ["英语", "其他外语"], "teaching_exp": 0,
         "introduction": "大一在读，英语高考145分，口语流利，适合辅导小学生和初中生英语基础。", "certificates": [],
         "location": "河北区", "available_time": ["二_上午", "四_上午", "六_下午", "日_上午", "日_下午"],
         "hourly_rate": 80, "verification_status": 0},
        {"real_name": "陈老师", "id_card": "120106199508096789", "school": "天津科技大学", "major": "生物工程",
         "grade": "大三", "education": "本科", "skills": ["生物", "化学"], "teaching_exp": 1,
         "introduction": "擅长初高中生物化学辅导，教学风格轻松活泼，注重培养学生的学习兴趣和实验思维。", "certificates": ["CET-4"],
         "location": "红桥区", "available_time": ["一_晚上", "三_晚上", "六_上午", "日_晚上"],
         "hourly_rate": 90, "verification_status": 0},
        {"real_name": "孙老师", "id_card": "120107198512018901", "school": "天津理工大学", "major": "计算机科学",
         "grade": "已毕业", "education": "博士", "skills": ["数学", "物理", "化学"], "teaching_exp": 8,
         "introduction": "博士学历，8年一线教学经验，曾辅导多名学生考入重点大学，尤其擅长理科综合辅导。", "certificates": ["教师资格证", "CET-6"],
         "location": "东丽区", "available_time": ["六_上午", "六_下午", "六_晚上", "日_上午", "日_下午", "日_晚上"],
         "hourly_rate": 180, "verification_status": 2},
        {"real_name": "周老师", "id_card": "120108199708110123", "school": "天津外国语大学", "major": "日语",
         "grade": "大四", "education": "本科", "skills": ["其他外语", "语文"], "teaching_exp": 2,
         "introduction": "日语N1证书持有者，可辅导日语和语文，善于激发学生对语言学习的兴趣。", "certificates": ["日语N1"],
         "location": "西青区", "available_time": ["二_晚上", "五_晚上", "六_上午", "六_下午", "日_下午"],
         "hourly_rate": 100, "verification_status": 1},
        {"real_name": "吴老师", "id_card": "120109199004012345", "school": "天津音乐学院", "major": "音乐教育",
         "grade": "大二", "education": "本科", "skills": ["语文", "英语"], "teaching_exp": 0,
         "introduction": "文科成绩优异，擅长语文阅读理解辅导和英语基础教学，有耐心有亲和力。", "certificates": [],
         "location": "津南区", "available_time": ["三_晚上", "五_晚上", "六_上午", "日_上午", "日_下午"],
         "hourly_rate": 75, "verification_status": 0},
        {"real_name": "郑老师", "id_card": "120110199112116789", "school": "中国民航大学", "major": "交通运输",
         "grade": "大三", "education": "本科", "skills": ["地理", "政治", "历史"], "teaching_exp": 2,
         "introduction": "文科综合成绩优异，擅长文综辅导，对地理政治历史有自己的高效学习方法和解题技巧。", "certificates": ["CET-4"],
         "location": "北辰区", "available_time": ["一_晚上", "二_晚上", "四_晚上", "六_下午", "日_下午", "日_晚上"],
         "hourly_rate": 95, "verification_status": 1},
    ]

    for i, pd in enumerate(parent_data, 1):
        user = User(username=f"test_parent_{i}", password="123", phone=f"1380001000{i:02d}", sex=i % 2 + 1, user_type=1, status=1)
        db.session.add(user)
        db.session.flush()
        parent = Parent(user_id=user.id, **pd)
        db.session.add(parent)
        parents.append(parent)

    for i, td in enumerate(tutor_data, 1):
        user = User(username=f"test_tutor_{i:02d}", password="123", phone=f"1390002000{i:02d}", sex=i % 2 + 1, user_type=2, status=1)
        db.session.add(user)
        db.session.flush()
        parent = Tutor(user_id=user.id, **td)
        db.session.add(parent)
        tutors.append(parent)

    db.session.commit()
    print(f"OK — 插入 {len(parents)} 条家长和 {len(tutors)} 条家教测试数据")
    print(f"家长用户名: test_parent_1 ~ test_parent_{len(parents)}")
    print(f"家教用户名: test_tutor_01 ~ test_tutor_{len(tutors):02d}")
