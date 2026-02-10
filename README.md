# quxuemiao
A tutor platform with Flask backend and HTML5 frontend

Quxuemiao是一个高效、可靠的家教资源匹配平台。采用 Python Flask 框架开发，实现了基于 JWT 的身份验证、导师/学生信息管理及课程预约功能。
?? 技术栈
* 核心框架: Flask 3.0+
* 数据库: SQLite (开发环境) / MySQL (生产环境)
* ORM: Flask-SQLAlchemy
* 身份验证: Flask-JWT-Extended
* 跨域处理: Flask-CORS

??? 快速上手
1. 环境准备
确保你已安装 Python 3.8 或更高版本。
Bash
# 克隆项目
git clone https://github.com/awsjjk/quxuemiao.git
cd tutor-backend

# 创建并激活虚拟环境
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
2. 环境配置
在根目录创建 .env 文件，并参考以下内容进行配置：
Plaintext
JWT_SECRET_KEY=你的加密密钥
DATABASE_URL=sqlite:///dev_database.db
FLASK_DEBUG=True
3. 运行项目
Bash
python app.py
项目默认运行在：http://127.0.0.1:5000

?? 目录结构
Plaintext
├── app.py              # 应用入口
├── models.py           # 数据库模型 (User, Tutor, Order等)
├── routes/             # 路由模块
│   └── auth.py         # 登录注册相关接口
├── instance/           # 本地数据库实例
└── requirements.txt    # 项目依赖清单

?? API 接口概览 (示例)
方法路径说明权限POST/api/auth/register用户注册公开POST/api/auth/login用户登录 (返回 JWT)公开
?? 协作规范
1. 分支管理: 请从 main 分支拉取新分支进行开发：feature/功能名。
2. 提交格式: 建议使用 feat: 新增功能 或 fix: 修复问题 作为 Commit 信息。
3. Pull Request: 代码完成后请提交 PR，并由至少一人审核。

?? 小贴士
* 数据库迁移：如果你修改了 models.py，请联系管理员运行迁移命令。
* 接口测试：建议使用 Postman 或 Apifox 导入 API 文档进行测试。

