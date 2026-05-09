# 趣学喵 — 家教供需匹配平台 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 Flask + SQLite 原型升级为 Python Flask + Vue 3 + MySQL + AI (RAG + Agent) 的全栈家教匹配平台，实现"需求发布 → AI 匹配 → 订单管理 → 服务评价"闭环。

**Architecture:** 前后端分离——Flask 提供 RESTful API（backend/），Vue 3 SPA 前端（frontend/），AI 模块独立 Python package（ai_module/），MySQL 8.0 关系型数据库。AI 匹配采用规则初筛 + ChromaDB RAG 检索 + 云端 LLM 打分，异步执行。

**Tech Stack:** Flask 3.0, SQLAlchemy, JWT, MySQL 8.0, ChromaDB, sentence-transformers (BAAI/bge-small-zh-v1.5), Vue 3 + Vite + Pinia + Vue Router 4 + Axios

---

### Task 1: 项目目录重构与 MySQL 配置

**Files:**
- Create: `backend/config.py`
- Create: `backend/requirements.txt`
- Create: `backend/app.py` (from existing `app.py`)
- Move: `models.py` → `backend/models.py`
- Move: `routes/auth.py` → `backend/routes/auth.py`
- Create: `backend/routes/__init__.py`
- Create: `backend/utils/__init__.py`
- Create: `backend/utils/decorators.py`
- Create: `ai_module/config.yaml`
- Create: `ai_module/__init__.py`

- [ ] **Step 1: 创建 backend/config.py**

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# MySQL 连接配置
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
MYSQL_DB = os.environ.get('MYSQL_DB', 'quxuemiao')

SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    '?charset=utf8mb4'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'quxuemiao-secret-key-change-in-prod')
JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 小时
```

- [ ] **Step 2: 创建 backend/requirements.txt**

```
Flask==3.0.3
Flask-Cors==5.0.0
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.0
cryptography==42.0.0
chromadb==0.4.22
sentence-transformers==2.5.0
openai==1.30.0
pyyaml==6.0.1
```

- [ ] **Step 3: 创建 backend/app.py**

```python
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

db.init_app(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

- [ ] **Step 4: 创建 backend/routes/__init__.py**

```python
```

- [ ] **Step 5: 创建 backend/utils/__init__.py**

```python
```

- [ ] **Step 6: 创建 backend/utils/decorators.py**

```python
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
```

- [ ] **Step 7: 创建 ai_module/config.yaml**

```yaml
llm:
  provider: "openai"          # openai / deepseek / qwen
  api_key: "your-api-key"
  model: "gpt-4o-mini"
  base_url: "https://api.openai.com/v1"
  temperature: 0.3
  max_tokens: 2000

embedding:
  model: "BAAI/bge-small-zh-v1.5"
  device: "cpu"               # cpu / cuda

rag:
  collection_name: "tutor_knowledge"
  persist_dir: "./ai_module/chroma_db"
  top_k: 10

matching:
  max_candidates: 50
  top_n: 5
```

- [ ] **Step 8: 创建 ai_module/__init__.py**

```python
```

- [ ] **Step 9: 移动文件并验证结构**

Run: `ls backend/ ai_module/`

- [ ] **Step 10: Commit**

```bash
git add backend/ ai_module/
git rm app.py models.py routes/ requirements.txt
git commit -m "feat: restructure project into backend/ + ai_module/ with MySQL config"
```

---

### Task 2: 适配 models.py 支持 MySQL

**Files:**
- Modify: `backend/models.py`

- [ ] **Step 1: 适配 models.py 为 MySQL 并新增 match_result 字段**

在 `backend/models.py` 中，保持现有所有模型不变，仅做以下改动：

1. 开头导入不变
2. 在 `Demand` 模型中新增 `match_result` 字段：

```python
# 在 Demand 类的 status 字段之后、create_time 之前添加：
match_result = db.Column(db.JSON, comment='AI匹配结果')
```

3. 在 `Demand` 模型中新增 `match_time` 字段和 `match_status` 字段用于异步匹配状态追踪：

```python
match_status = db.Column(db.String(20), default='pending', comment='匹配状态: pending/processing/done/failed')
match_time = db.Column(db.DateTime, comment='匹配完成时间')
```

- [ ] **Step 2: Commit**

```bash
git add backend/models.py
git commit -m "feat: add match_result/match_status fields to Demand model for MySQL"
```

---

### Task 3: 增强 Auth 路由

**Files:**
- Modify: `backend/routes/auth.py`

- [ ] **Step 1: 改写 auth.py 支持完善注册与信息更新**

`backend/routes/auth.py` 已存在，需要扩展 `update_profile` 支持更新家长/家教详情：

```python
# 在 update_profile 函数中，现有基础上增加角色详情更新：

@auth_bp.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404

    data = request.get_json()

    # 更新 User 基础字段
    for field in ['phone', 'email', 'avatar', 'sex', 'birthday']:
        if field in data:
            setattr(user, field, data[field])

    # 更新角色详情
    if user.user_type == 1:  # 家长
        parent = Parent.query.filter_by(user_id=user.id).first()
        if parent:
            for field in ['real_name', 'address', 'location', 'children_info', 'preference']:
                if field in data:
                    setattr(parent, field, data[field])
    elif user.user_type == 2:  # 家教
        tutor = Tutor.query.filter_by(user_id=user.id).first()
        if tutor:
            for field in ['real_name', 'school', 'major', 'grade', 'education',
                          'skills', 'teaching_exp', 'introduction', 'certificates',
                          'location', 'available_time', 'hourly_rate']:
                if field in data:
                    setattr(tutor, field, data[field])

    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "资料更新成功"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": f"更新失败: {str(e)}"}), 500
```

- [ ] **Step 2: Commit**

```bash
git add backend/routes/auth.py
git commit -m "feat: extend update_profile to support parent/tutor detail fields"
```

---

### Task 4: 实现 AI 模块 — embedding.py

**Files:**
- Create: `ai_module/embedding.py`

- [ ] **Step 1: 创建 ai_module/embedding.py**

```python
"""本地 embedding 模块 — 使用 BAAI/bge-small-zh-v1.5"""
import yaml
import os
from pathlib import Path

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_model_name = _config['embedding']['model']
_device = _config['embedding'].get('device', 'cpu')

_encoder = None

def _get_encoder():
    global _encoder
    if _encoder is None:
        from sentence_transformers import SentenceTransformer
        _encoder = SentenceTransformer(_model_name, device=_device)
    return _encoder

def embed(texts):
    """文本列表 → 向量列表
    Args:
        texts: str or list[str]
    Returns:
        list[list[float]]
    """
    if isinstance(texts, str):
        texts = [texts]
    encoder = _get_encoder()
    embeddings = encoder.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
```

- [ ] **Step 2: Commit**

```bash
git add ai_module/embedding.py
git commit -m "feat: add local embedding module with BAAI/bge-small-zh-v1.5"
```

---

### Task 5: 实现 AI 模块 — llm_client.py

**Files:**
- Create: `ai_module/llm_client.py`

- [ ] **Step 1: 创建 ai_module/llm_client.py**

```python
"""统一 LLM 调用接口 — 读取 config.yaml 配置"""
import yaml
import json
from pathlib import Path
from openai import OpenAI

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_llm_config = _config['llm']
_client = OpenAI(
    api_key=_llm_config['api_key'],
    base_url=_llm_config['base_url']
)
_model = _llm_config['model']
_temperature = _llm_config.get('temperature', 0.3)
_max_tokens = _llm_config.get('max_tokens', 2000)


class LLMClient:

    def chat(self, system_prompt, user_prompt, response_format=None):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        kwargs = dict(
            model=_model,
            messages=messages,
            temperature=_temperature,
            max_tokens=_max_tokens
        )
        if response_format == 'json':
            kwargs['response_format'] = {"type": "json_object"}

        response = _client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def chat_json(self, system_prompt, user_prompt):
        text = self.chat(system_prompt, user_prompt, response_format='json')
        return json.loads(text)
```

- [ ] **Step 2: Commit**

```bash
git add ai_module/llm_client.py
git commit -m "feat: add unified LLM client with OpenAI-compatible API"
```

---

### Task 6: 实现 AI 模块 — rag.py

**Files:**
- Create: `ai_module/rag.py`

- [ ] **Step 1: 创建 ai_module/rag.py**

```python
"""ChromaDB 向量检索 + 知识库管理"""
import yaml
import chromadb
from pathlib import Path
from embedding import embed

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_rag_config = _config['rag']
_persist_dir = Path(_config_path).parent / _rag_config['persist_dir']
_collection_name = _rag_config['collection_name']
_top_k = _rag_config.get('top_k', 10)

_client = chromadb.PersistentClient(path=str(_persist_dir))


class RAGRetriever:

    def __init__(self):
        self.collection = _client.get_or_create_collection(
            name=_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def search(self, query, top_k=None):
        """向量检索 — 返回最相关的 top_k 个文档
        Args:
            query: str — 查询文本
            top_k: int — 返回数量
        Returns:
            list[dict] — [{id, text, metadata, distance}, ...]
        """
        if top_k is None:
            top_k = _top_k
        query_vec = embed(query)
        results = self.collection.query(
            query_embeddings=query_vec,
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        docs = []
        ids = results.get('ids', [[]])[0]
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]
        for i in range(len(ids)):
            docs.append({
                'id': ids[i],
                'text': documents[i] if documents else '',
                'metadata': metadatas[i] if metadatas else {},
                'distance': distances[i] if distances else 0
            })
        return docs


class KnowledgeBase:

    def __init__(self):
        self.collection = _client.get_or_create_collection(
            name=_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, doc_id, text, metadata=None):
        vec = embed(text)
        self.collection.add(
            ids=[doc_id],
            embeddings=vec,
            documents=[text],
            metadatas=[metadata or {}]
        )

    def add_batch(self, items):
        """items: [(doc_id, text, metadata), ...]"""
        if not items:
            return
        ids = [it[0] for it in items]
        texts = [it[1] for it in items]
        vecs = embed(texts)
        metas = [it[2] if len(it) > 2 else {} for it in items]
        self.collection.add(
            ids=ids,
            embeddings=vecs,
            documents=texts,
            metadatas=metas
        )

    def delete(self, doc_id):
        self.collection.delete(ids=[doc_id])

    def count(self):
        return self.collection.count()
```

- [ ] **Step 2: Commit**

```bash
git add ai_module/rag.py
git commit -m "feat: add ChromaDB RAG retriever and knowledge base manager"
```

---

### Task 7: 实现 AI 模块 — agent.py

**Files:**
- Create: `ai_module/agent.py`
- Create: `ai_module/data/subjects.json`
- Create: `ai_module/data/prompts/match_scoring.txt`

- [ ] **Step 1: 创建学科知识点数据 `ai_module/data/subjects.json`**

```json
{
  "数学": {
    "小学": ["四则运算", "分数与小数", "几何初步", "应用题", "逻辑思维"],
    "初中": ["代数基础", "几何证明", "函数入门", "方程与不等式", "统计与概率"],
    "高中": ["函数与导数", "解析几何", "数列与极限", "概率统计", "向量与立体几何"]
  },
  "语文": {
    "小学": ["拼音与识字", "阅读理解", "作文基础", "古诗词", "成语故事"],
    "初中": ["文言文阅读", "现代文阅读", "议论文写作", "语法修辞", "名著导读"],
    "高中": ["文言文翻译", "论述文写作", "诗歌鉴赏", "文学常识", "语言文字运用"]
  },
  "英语": {
    "小学": ["字母与发音", "基础词汇", "简单对话", "自然拼读", "绘本阅读"],
    "初中": ["语法体系", "完形填空", "阅读理解", "书面表达", "听力训练"],
    "高中": ["高级语法", "长难句分析", "写作模板", "翻译技巧", "真题训练"]
  },
  "物理": {
    "初中": ["力学基础", "电学入门", "光学", "热学", "声现象"],
    "高中": ["牛顿力学", "电磁学", "热力学", "光学与原子物理", "实验专题"]
  },
  "化学": {
    "初中": ["物质构成", "化学方程式", "溶液", "酸碱盐", "金属活动性"],
    "高中": ["物质结构", "化学反应原理", "有机化学", "电化学", "化学实验"]
  }
}
```

- [ ] **Step 2: 创建 Prompt 模板 `ai_module/data/prompts/match_scoring.txt`**

```
你是一个专业的家教匹配评估专家。请根据以下信息，对候选家教进行综合打分排序。

## 家长需求
- 学科: {subject}
- 年级: {grade}
- 地区: {location}
- 预算: {budget} 元/小时
- 时间要求: {time_slots}
- 额外要求: {requirements}
- 需求描述: {description}

## 学科知识点参考
{knowledge_points}

## 候选家教列表
{candidates}

## 评估维度
1. 学科匹配度 (0-40分): 家教专业/技能是否与需求学科匹配
2. 经验匹配度 (0-30分): 教学经验、年级对口程度
3. 地理与时间 (0-15分): 位置接近度、时间可用性
4. 性价比 (0-15分): 收费标准与资质的匹配度

## 输出要求
请输出 JSON 数组，按总分从高到低排序：
[
  {
    "tutor_id": 整数,
    "total_score": 整数,
    "subject_match": 整数,
    "experience_match": 整数,
    "location_time_match": 整数,
    "value_match": 整数,
    "reason": "推荐理由，不超过50字"
  },
  ...
]
```

- [ ] **Step 3: 创建 ai_module/agent.py**

```python
"""匹配决策 Agent — 规则初筛 + RAG 检索 + LLM 打分"""
import yaml
import json
from pathlib import Path
from llm_client import LLMClient
from rag import RAGRetriever

_config_path = Path(__file__).parent / 'config.yaml'
with open(_config_path, 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)

_match_config = _config['matching']

_PROMPT_PATH = Path(__file__).parent / 'data' / 'prompts' / 'match_scoring.txt'
with open(_PROMPT_PATH, 'r', encoding='utf-8') as f:
    _MATCH_PROMPT_TEMPLATE = f.read()

_SUBJECTS_PATH = Path(__file__).parent / 'data' / 'subjects.json'
with open(_SUBJECTS_PATH, 'r', encoding='utf-8') as f:
    _SUBJECTS = json.load(f)


class MatchAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.rag = RAGRetriever()

    def match(self, demand, candidates):
        """执行 AI 匹配
        Args:
            demand: dict — 需求信息 (subject, grade, location, budget, time_slots, description, requirements, tags)
            candidates: list[dict] — 候选家教列表, 每个 dict 含 id, real_name, school, major, skills, teaching_exp,
                        introduction, location, available_time, hourly_rate, verification_status
        Returns:
            list[dict] — [{tutor_id, total_score, subject_match, experience_match, location_time_match, value_match, reason}, ...]
        """
        top_n = _match_config.get('top_n', 5)

        # 1. RAG 检索 — 获取学科知识点作为上下文
        subject = demand.get('subject', '')
        grade = demand.get('grade', '')
        query = f"{subject} {grade} 家教 辅导"
        rag_docs = self.rag.search(query, top_k=5)

        knowledge_points = []
        if subject in _SUBJECTS:
            for level, points in _SUBJECTS[subject].items():
                knowledge_points.append(f"- {level}: {', '.join(points)}")

        # 2. 构造候选家教文本
        candidates_text = []
        for i, t in enumerate(candidates):
            skills = ', '.join(t.get('skills', [])) if isinstance(t.get('skills'), list) else t.get('skills', '')
            available = t.get('available_time', '')
            if isinstance(available, list):
                available = '; '.join(available)
            candidates_text.append(
                f"[{t.get('id')}] {t.get('real_name', '未知')} | "
                f"学校: {t.get('school', '')} | 专业: {t.get('major', '')} | "
                f"学历: {t.get('education', '')} | 年级: {t.get('grade', '')} | "
                f"技能: {skills} | "
                f"教学经验: {t.get('teaching_exp', 0)}年 | "
                f"地区: {t.get('location', '')} | "
                f"可用时间: {available} | "
                f"时薪: {t.get('hourly_rate', 0)}元 | "
                f"简介: {t.get('introduction', '')}"
            )

        rag_context = '\n'.join(
            f"[RAG {d['distance']:.3f}] {d['text'][:200]}" for d in rag_docs
        )

        # 3. 构造 Prompt
        user_prompt = _MATCH_PROMPT_TEMPLATE.format(
            subject=subject,
            grade=grade,
            location=demand.get('location', ''),
            budget=demand.get('budget', 0),
            time_slots=json.dumps(demand.get('time_slots', []), ensure_ascii=False),
            requirements=demand.get('requirements', '无'),
            description=demand.get('description', ''),
            knowledge_points='\n'.join(knowledge_points),
            candidates='\n'.join(candidates_text)
        )

        system_prompt = f"你是一个家教匹配专家。结合以下 RAG 知识库参考信息辅助判断：\n{rag_context}"

        # 4. LLM 调用
        result = self.llm.chat_json(system_prompt, user_prompt)

        # 5. 取 top_n
        if isinstance(result, list):
            return result[:top_n]
        return []
```

- [ ] **Step 4: Commit**

```bash
git add ai_module/agent.py ai_module/data/
git commit -m "feat: add MatchAgent with rule-filter + RAG + LLM scoring pipeline"
```

---

### Task 8: 实现 Demand 路由

**Files:**
- Create: `backend/routes/demand.py`
- Modify: `backend/app.py` (register demand blueprint)

- [ ] **Step 1: 创建 backend/routes/demand.py**

```python
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
```

- [ ] **Step 2: 在 app.py 中注册 demand blueprint**

```python
# 在 app.py 中添加:
from routes.demand import demand_bp
app.register_blueprint(demand_bp, url_prefix='/api/demand')
```

- [ ] **Step 3: Commit**

```bash
git add backend/routes/demand.py backend/app.py
git commit -m "feat: add demand CRUD routes (create/list/detail/update)"
```

---

### Task 9: 实现 Match 路由（异步匹配）

**Files:**
- Create: `backend/routes/match.py`
- Modify: `backend/app.py` (register match blueprint)

- [ ] **Step 1: 创建 backend/routes/match.py**

```python
import json
import threading
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Demand, Tutor, Parent

match_bp = Blueprint('match', __name__)

_task_status = {}


def _run_match(demand_id):
    """后台执行匹配任务"""
    try:
        with match_bp.application.app_context():
            _task_status[demand_id] = 'processing'

            demand = Demand.query.get(demand_id)
            if not demand:
                _task_status[demand_id] = 'failed'
                return

            # 1. 规则初筛
            candidates = Tutor.query.filter(
                Tutor.verification_status >= 1
            )
            if demand.location:
                candidates = candidates.filter(Tutor.location == demand.location)
            if demand.budget:
                candidates = candidates.filter(Tutor.hourly_rate <= demand.budget * 1.5)
            candidates = candidates.limit(50).all()

            if not candidates:
                _task_status[demand_id] = 'done'
                demand.match_result = []
                demand.match_status = 'done'
                demand.match_time = datetime.now()
                db.session.commit()
                return

            # 2. 构造候选数据
            candidate_dicts = []
            for t in candidates:
                candidate_dicts.append({
                    'id': t.id, 'real_name': t.real_name, 'school': t.school,
                    'major': t.major, 'skills': t.skills, 'teaching_exp': t.teaching_exp or 0,
                    'introduction': t.introduction, 'location': t.location,
                    'available_time': t.available_time, 'hourly_rate': float(t.hourly_rate),
                    'education': t.education, 'grade': t.grade,
                    'verification_status': t.verification_status
                })

            # 3. AI 匹配
            demand_dict = {
                'subject': demand.subject, 'grade': demand.grade,
                'location': demand.location, 'budget': float(demand.budget) if demand.budget else 0,
                'time_slots': demand.time_slots, 'description': demand.description or '',
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
        with match_bp.application.app_context():
            demand = Demand.query.get(demand_id)
            if demand:
                demand.match_status = 'failed'
                db.session.commit()
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

    demand.match_status = 'pending'
    db.session.commit()

    thread = threading.Thread(target=_run_match, args=(demand_id,), daemon=True)
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
```

- [ ] **Step 2: 在 app.py 中注册 match blueprint**

```python
from routes.match import match_bp
app.register_blueprint(match_bp, url_prefix='/api/match')
```

- [ ] **Step 3: Commit**

```bash
git add backend/routes/match.py backend/app.py
git commit -m "feat: add async match routes with threading + AI agent integration"
```

---

### Task 10: 实现 Order 路由

**Files:**
- Create: `backend/routes/order.py`
- Modify: `backend/app.py` (register order blueprint)

- [ ] **Step 1: 创建 backend/routes/order.py**

```python
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
    demand.status = 2  # 已匹配
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

    valid_transitions = {2: [3, 4], 3: [4]}  # 2→3(完成), 2→4(取消), 3→4(取消)
    if new_status not in valid_transitions.get(o.status, []):
        return jsonify({"code": 400, "msg": "无效的状态变更"}), 400

    if new_status == 3 and user.user_type not in (1, 3):
        return jsonify({"code": 403, "msg": "仅家长或管理员可确认完成"}), 403

    o.status = new_status
    o.update_time = datetime.now()
    db.session.commit()

    # 如果订单完成，同步更新需求状态
    if new_status == 3:
        demand = Demand.query.get(o.demand_id)
        if demand:
            demand.status = 3

    db.session.commit()
    return jsonify({"code": 200, "msg": "状态更新成功"}), 200
```

- [ ] **Step 2: 在 app.py 中注册 order blueprint**

```python
from routes.order import order_bp
app.register_blueprint(order_bp, url_prefix='/api/order')
```

- [ ] **Step 3: Commit**

```bash
git add backend/routes/order.py backend/app.py
git commit -m "feat: add order routes (create/list/detail/status)"
```

---

### Task 11: 实现 Rating 路由

**Files:**
- Create: `backend/routes/rating.py`
- Modify: `backend/app.py` (register rating blueprint)

- [ ] **Step 1: 创建 backend/routes/rating.py**

```python
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
    overall = (teaching + attitude + punctuality) // 3 if not data.get('overall_score') else data.get('overall_score')

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

    ratings = Rating.query.filter_by(tutor_id=tutor_id).order_by(Rating.create_time.desc()).limit(20).all()

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

    avg = db.session.query(db.func.avg(Rating.overall_score)).filter(Rating.tutor_id == tutor_id).scalar()
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
```

- [ ] **Step 2: 在 app.py 中注册 rating blueprint**

```python
from routes.rating import rating_bp
app.register_blueprint(rating_bp, url_prefix='/api/rating')
```

- [ ] **Step 3: Commit**

```bash
git add backend/routes/rating.py backend/app.py
git commit -m "feat: add rating routes (submit/tutor history with average)"
```

---

### Task 12: 初始化 Vue 3 前端项目

**Files:**
- Create: `frontend/` (via Vite scaffolding)
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/api/index.js`
- Create: `frontend/src/stores/auth.js`
- Create: `frontend/src/stores/demand.js`

- [ ] **Step 1: 使用 Vite 创建 Vue 3 项目**

Run:
```bash
cd frontend && npm create vite@latest . -- --template vue
npm install vue-router@4 pinia axios
```

- [ ] **Step 2: 配置 vite.config.js (API 代理)**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: 创建 frontend/src/api/index.js**

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
export const authAPI = {
  login: data => api.post('/auth/login', data),
  register: data => api.post('/auth/register', data),
  getUserInfo: () => api.get('/auth/user_info'),
  updateProfile: data => api.put('/auth/update_profile', data)
}
export const demandAPI = {
  create: data => api.post('/demand/create', data),
  list: () => api.get('/demand/list'),
  detail: id => api.get(`/demand/${id}`),
  update: (id, data) => api.put(`/demand/${id}`, data)
}
export const matchAPI = {
  run: demandId => api.post('/match/run', { demand_id: demandId }),
  result: demandId => api.get(`/match/result/${demandId}`)
}
export const orderAPI = {
  create: data => api.post('/order/create', data),
  list: () => api.get('/order/list'),
  detail: id => api.get(`/order/${id}`),
  updateStatus: (id, status) => api.put(`/order/${id}/status`, { status })
}
export const ratingAPI = {
  submit: data => api.post('/rating/submit', data),
  tutorRatings: tutorId => api.get(`/rating/tutor/${tutorId}`)
}
```

- [ ] **Step 4: 创建 frontend/src/stores/auth.js**

```javascript
import { defineStore } from 'pinia'
import { authAPI } from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || '',
    isLoggedIn: !!localStorage.getItem('token')
  }),
  actions: {
    async login(username, password) {
      const res = await authAPI.login({ username, password })
      this.token = res.token
      this.isLoggedIn = true
      localStorage.setItem('token', res.token)
      await this.fetchUser()
    },
    async register(data) {
      await authAPI.register(data)
    },
    async fetchUser() {
      const res = await authAPI.getUserInfo()
      this.user = res.data
    },
    logout() {
      this.token = ''
      this.user = null
      this.isLoggedIn = false
      localStorage.removeItem('token')
    }
  }
})
```

- [ ] **Step 5: 创建 frontend/src/stores/demand.js**

```javascript
import { defineStore } from 'pinia'
import { demandAPI, matchAPI } from '../api'

export const useDemandStore = defineStore('demand', {
  state: () => ({
    demands: [],
    currentDemand: null,
    matchResult: null,
    matchStatus: null
  }),
  actions: {
    async fetchList() {
      const res = await demandAPI.list()
      this.demands = res.data
    },
    async fetchDetail(id) {
      const res = await demandAPI.detail(id)
      this.currentDemand = res.data
    },
    async create(data) {
      return await demandAPI.create(data)
    },
    async runMatch(demandId) {
      await matchAPI.run(demandId)
      this.matchStatus = 'pending'
    },
    async pollResult(demandId) {
      const res = await matchAPI.result(demandId)
      this.matchStatus = res.data.status
      if (res.data.status === 'done') {
        this.matchResult = res.data.result
      }
      return res.data
    }
  }
})
```

- [ ] **Step 6: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold Vue 3 + Vite project with router/stores/api"
```

---

### Task 13: 实现前端页面 — Login & Register

**Files:**
- Create: `frontend/src/views/LoginPage.vue`
- Create: `frontend/src/views/RegisterPage.vue`
- Modify: `frontend/src/router/index.js`

- [ ] **Step 1: 创建路由配置 frontend/src/router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginPage.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterPage.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardPage.vue'), meta: { auth: true } },
  { path: '/demand/:id', name: 'DemandDetail', component: () => import('../views/DemandDetailPage.vue'), meta: { auth: true } },
  { path: '/match/:demand_id', name: 'MatchResult', component: () => import('../views/MatchResultPage.vue'), meta: { auth: true } },
  { path: '/order/:id', name: 'OrderDetail', component: () => import('../views/OrderDetailPage.vue'), meta: { auth: true } },
  { path: '/profile', name: 'Profile', component: () => import('../views/ProfilePage.vue'), meta: { auth: true } },
  { path: '/', redirect: '/dashboard' },
  { path: '/:pathMatch(.*)', redirect: '/dashboard' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

- [ ] **Step 2: 创建 frontend/src/views/LoginPage.vue**

```vue
<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>趣学喵</h1>
      <p class="subtitle">天津市家教供需匹配平台</p>
      <form @submit.prevent="handleLogin">
        <input v-model="username" placeholder="用户名" required />
        <input v-model="password" type="password" placeholder="密码" required />
        <button :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p class="link">还没有账号？<router-link to="/register">立即注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.msg || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display:flex; align-items:center; justify-content:center; min-height:100vh; background:#f5f5f5; }
.auth-card { background:#fff; padding:40px; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,0.08); width:360px; text-align:center; }
.auth-card h1 { margin:0 0 4px; color:#2563eb; }
.subtitle { color:#6b7280; font-size:13px; margin-bottom:24px; }
input { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.error { color:#dc2626; font-size:13px; margin-top:8px; }
.link { margin-top:16px; font-size:13px; color:#6b7280; }
</style>
```

- [ ] **Step 3: 创建 RegisterPage.vue**

```vue
<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>注册账号</h1>
      <form @submit.prevent="handleRegister">
        <input v-model="form.username" placeholder="用户名" required />
        <input v-model="form.password" type="password" placeholder="密码" required />
        <input v-model="form.phone" placeholder="手机号" />
        <input v-model="form.email" placeholder="邮箱" />
        <select v-model.number="form.user_type" required>
          <option :value="1">我是家长</option>
          <option :value="2">我是家教</option>
        </select>
        <button :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
      <p class="link">已有账号？<router-link to="/login">去登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ username: '', password: '', phone: '', email: '', user_type: 1 })
const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  success.value = ''
  try {
    await auth.register({ ...form })
    success.value = '注册成功，请登录'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.msg || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display:flex; align-items:center; justify-content:center; min-height:100vh; background:#f5f5f5; }
.auth-card { background:#fff; padding:40px; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,0.08); width:360px; text-align:center; }
.auth-card h1 { margin:0 0 20px; color:#2563eb; }
input, select { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.error { color:#dc2626; font-size:13px; }
.success { color:#16a34a; font-size:13px; }
.link { margin-top:16px; font-size:13px; color:#6b7280; }
</style>
```

- [ ] **Step 4: 更新 App.vue 和 main.js**

```vue
<!-- App.vue -->
<template>
  <router-view />
</template>
```

```javascript
// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/ frontend/src/router/ frontend/src/App.vue frontend/src/main.js
git commit -m "feat: add login and register pages with role selection"
```

---

### Task 14: 实现 Dashboard + 需求发布 + AI 匹配页面

**Files:**
- Create: `frontend/src/views/DashboardPage.vue`
- Create: `frontend/src/views/DemandDetailPage.vue`
- Create: `frontend/src/views/MatchResultPage.vue`
- Create: `frontend/src/components/DemandForm.vue`
- Create: `frontend/src/components/DemandCard.vue`
- Create: `frontend/src/components/TutorCard.vue`
- Create: `frontend/src/components/MatchLoading.vue`

- [ ] **Step 1: 创建 DemandForm.vue**

```vue
<template>
  <div class="demand-form">
    <h3>发布家教需求</h3>
    <form @submit.prevent="submit">
      <div class="row">
        <input v-model="form.title" placeholder="标题（如：高一数学辅导）" required />
        <select v-model="form.subject" required>
          <option value="">选择学科</option>
          <option value="数学">数学</option><option value="语文">语文</option>
          <option value="英语">英语</option><option value="物理">物理</option>
          <option value="化学">化学</option>
        </select>
      </div>
      <div class="row">
        <select v-model="form.grade" required>
          <option value="">选择年级</option>
          <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
        </select>
        <input v-model="form.location" placeholder="所在区域（如：南开区）" />
      </div>
      <input v-model.number="form.budget" type="number" placeholder="预算（元/小时）" />
      <textarea v-model="form.description" placeholder="详细描述孩子的学习情况、薄弱环节..." rows="3"></textarea>
      <input v-model="form.requirements" placeholder="额外要求（如：有耐心、女老师优先）" />
      <div class="row">
        <input v-model.number="form.duration" type="number" placeholder="每次课时长(小时)" min="1" max="4" />
        <select v-model="form.frequency">
          <option value="">上课频率</option>
          <option value="每周1次">每周1次</option><option value="每周2次">每周2次</option>
          <option value="每周3次">每周3次</option><option value="每天">每天</option>
        </select>
      </div>
      <label class="urgent"><input type="checkbox" v-model="form.is_urgent" /> 紧急需求</label>
      <button :disabled="loading">{{ loading ? '发布中...' : '发布需求' }}</button>
    </form>
    <p v-if="msg" :class="msgType">{{ msg }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useDemandStore } from '../stores/demand'

const emit = defineEmits(['created'])
const store = useDemandStore()
const grades = ['小学一年级','小学二年级','小学三年级','小学四年级','小学五年级','小学六年级',
  '初一','初二','初三','高一','高二','高三']
const form = reactive({
  title: '', subject: '', grade: '', location: '', budget: null, description: '',
  requirements: '', duration: null, frequency: '', is_urgent: false
})
const loading = ref(false)
const msg = ref('')
const msgType = ref('')

async function submit() {
  loading.value = true
  msg.value = ''
  try {
    await store.create({ ...form, time_slots: [], tags: [] })
    msg.value = '发布成功'
    msgType.value = 'success'
    emit('created')
    Object.keys(form).forEach(k => form[k] = typeof form[k] === 'boolean' ? false : (typeof form[k] === 'number' ? null : ''))
  } catch (e) {
    msg.value = e.response?.data?.msg || '发布失败'
    msgType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.demand-form { background:#fff; padding:24px; border-radius:12px; box-shadow:0 1px 6px rgba(0,0,0,0.06); max-width:600px; margin:0 auto; }
h3 { margin:0 0 16px; color:#1f2937; }
.row { display:flex; gap:12px; }
.row > * { flex:1; }
input, select, textarea { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
.urgent { display:flex; align-items:center; gap:6px; font-size:13px; color:#6b7280; margin-bottom:12px; }
.urgent input { width:auto; margin:0; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.success { color:#16a34a; font-size:13px; margin-top:8px; }
.error { color:#dc2626; font-size:13px; margin-top:8px; }
</style>
```

- [ ] **Step 2: 创建 DemandCard.vue**

```vue
<template>
  <div class="card" @click="$emit('click')">
    <div class="header">
      <span class="title">{{ demand.title }}</span>
      <span class="tag" :class="statusClass">{{ statusText }}</span>
    </div>
    <div class="info">
      <span>{{ demand.subject }} · {{ demand.grade }}</span>
      <span v-if="demand.location">{{ demand.location }}</span>
      <span v-if="demand.budget">{{ demand.budget }}元/时</span>
    </div>
    <div class="actions" v-if="demand.status === 1" @click.stop>
      <button @click="$emit('match')" :disabled="matching">AI 智能匹配</button>
    </div>
    <div class="actions" v-if="demand.match_status === 'done' && demand.match_result" @click.stop>
      <button class="secondary" @click="$emit('viewMatch')">查看匹配结果</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ demand: Object, matching: Boolean })
defineEmits(['click', 'match', 'viewMatch'])

const statuses = { 1: '招募中', 2: '已匹配', 3: '已完成', 4: '已取消' }
const statusText = computed(() => statuses[props.demand.status] || '未知')
const statusClass = computed(() => props.demand.status === 1 ? 'active' : '')
</script>

<style scoped>
.card { background:#fff; padding:16px 20px; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,0.06); cursor:pointer; margin-bottom:10px; transition:box-shadow 0.15s; }
.card:hover { box-shadow:0 2px 10px rgba(0,0,0,0.1); }
.header { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.title { font-weight:600; color:#1f2937; }
.tag { font-size:12px; padding:2px 8px; border-radius:12px; background:#f3f4f6; color:#6b7280; }
.tag.active { background:#dbeafe; color:#2563eb; }
.info { display:flex; gap:12px; font-size:13px; color:#6b7280; flex-wrap:wrap; }
.actions { margin-top:12px; display:flex; gap:8px; }
button { padding:6px 16px; background:#2563eb; color:#fff; border:none; border-radius:6px; font-size:13px; cursor:pointer; }
button:disabled { opacity:0.6; }
button.secondary { background:#059669; }
</style>
```

- [ ] **Step 3: 创建 DashboardPage.vue**

```vue
<template>
  <div class="dashboard">
    <nav>
      <span class="logo">趣学喵</span>
      <div class="nav-right">
        <span class="user">{{ auth.user?.username }} ({{ roleText }})</span>
        <button @click="goProfile">个人信息</button>
        <button @click="goOrders">我的订单</button>
        <button class="logout" @click="handleLogout">退出</button>
      </div>
    </nav>

    <div class="container" v-if="auth.user?.user_type === 1">
      <h2>我的家教需求</h2>
      <button class="btn-create" @click="showForm = !showForm">
        {{ showForm ? '收起' : '+ 发布新需求' }}
      </button>
      <DemandForm v-if="showForm" @created="onCreated" />
      <div class="list" v-if="store.demands.length">
        <DemandCard v-for="d in store.demands" :key="d.id" :demand="d"
          :matching="matchingId === d.id"
          @click="$router.push(`/demand/${d.id}`)"
          @match="handleMatch(d.id)"
          @viewMatch="$router.push(`/match/${d.id}`)" />
      </div>
      <p v-else class="empty">还没有发布需求，点击上方按钮发布第一条</p>
    </div>

    <div class="container" v-else-if="auth.user?.user_type === 2">
      <h2>家教工作台</h2>
      <p class="empty">完善个人资料以接收匹配推荐</p>
      <button @click="goProfile">完善资料</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useDemandStore } from '../stores/demand'
import DemandForm from '../components/DemandForm.vue'
import DemandCard from '../components/DemandCard.vue'

const router = useRouter()
const auth = useAuthStore()
const store = useDemandStore()

const showForm = ref(false)
const matchingId = ref(null)

const roleText = computed(() => {
  const roles = { 1: '家长', 2: '家教', 3: '管理员' }
  return roles[auth.user?.user_type] || ''
})

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  if (auth.user?.user_type === 1) await store.fetchList()
})

function onCreated() {
  showForm.value = false
  store.fetchList()
}

async function handleMatch(demandId) {
  matchingId.value = demandId
  await store.runMatch(demandId)
  matchingId.value = null
  router.push(`/match/${demandId}`)
}

function handleLogout() { auth.logout(); router.push('/login') }
function goProfile() { router.push('/profile') }
function goOrders() { router.push('/order/0') }
</script>

<style scoped>
.dashboard { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
.nav-right { display:flex; align-items:center; gap:12px; }
.nav-right .user { font-size:14px; color:#374151; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
nav button.logout { background:#fee2e2; color:#dc2626; border-color:#fecaca; }
.container { max-width:700px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; }
.btn-create { margin:12px 0; padding:8px 20px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
.empty { color:#9ca3af; font-size:14px; margin-top:48px; text-align:center; }
.list { margin-top:16px; }
</style>
```

- [ ] **Step 4: 创建 TutorCard.vue**

```vue
<template>
  <div class="tutor-card">
    <div class="top">
      <span class="rank">#{{ rank }}</span>
      <span class="name">{{ tutor.real_name || '未填写姓名' }}</span>
      <span class="score">{{ tutor.total_score }}分</span>
    </div>
    <div class="meta">
      <span>{{ tutor.school }}</span>
      <span>{{ tutor.major }}</span>
      <span>{{ tutor.education }}</span>
      <span>{{ tutor.teaching_exp }}年经验</span>
    </div>
    <div class="scores">
      <span>学科匹配 {{ tutor.subject_match }}/40</span>
      <span>经验匹配 {{ tutor.experience_match }}/30</span>
      <span>区位匹配 {{ tutor.location_time_match }}/15</span>
      <span>性价比 {{ tutor.value_match }}/15</span>
    </div>
    <p class="reason">💡 {{ tutor.reason }}</p>
    <button v-if="!selected" @click="$emit('select', tutor.tutor_id)">选择此家教</button>
  </div>
</template>

<script setup>
defineProps({ tutor: Object, rank: Number, selected: Boolean })
defineEmits(['select'])
</script>

<style scoped>
.tutor-card { background:#fff; padding:20px; border-radius:10px; box-shadow:0 1px 6px rgba(0,0,0,0.06); margin-bottom:12px; }
.top { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.rank { background:#2563eb; color:#fff; width:28px; height:28px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; }
.name { font-weight:600; font-size:16px; color:#1f2937; }
.score { margin-left:auto; font-weight:700; color:#2563eb; font-size:18px; }
.meta { display:flex; gap:12px; font-size:13px; color:#6b7280; margin-bottom:8px; }
.scores { display:flex; gap:10px; font-size:12px; color:#9ca3af; margin-bottom:8px; }
.reason { font-size:13px; color:#374151; margin-bottom:12px; }
button { padding:8px 20px; background:#059669; color:#fff; border:none; border-radius:6px; font-size:13px; cursor:pointer; }
</style>
```

- [ ] **Step 5: 创建 MatchLoading.vue 和 MatchResultPage.vue**

```vue
<!-- MatchLoading.vue -->
<template>
  <div class="loading">
    <div class="spinner"></div>
    <p>AI 正在为您智能匹配家教...</p>
    <p class="hint">正在分析需求、检索知识库、评估候选家教</p>
  </div>
</template>
<style scoped>
.loading { text-align:center; padding:60px 0; }
.spinner { width:40px; height:40px; border:3px solid #e5e7eb; border-top-color:#2563eb; border-radius:50%; animation:spin 0.8s linear infinite; margin:0 auto 16px; }
@keyframes spin { to { transform:rotate(360deg); } }
p { color:#374151; font-size:15px; }
.hint { color:#9ca3af; font-size:13px; margin-top:4px; }
</style>
```

```vue
<!-- MatchResultPage.vue -->
<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.push('/dashboard')">返回</button></nav>
    <div class="container">
      <h2>AI 匹配结果</h2>
      <MatchLoading v-if="status === 'pending' || status === 'processing'" />
      <div v-else-if="status === 'done' && results.length">
        <TutorCard v-for="(t, i) in results" :key="t.tutor_id" :tutor="t" :rank="i+1"
          :selected="selectedTutor === t.tutor_id" @select="handleSelect" />
        <button v-if="selectedTutor" class="create-btn" @click="createOrder">创建订单</button>
      </div>
      <p v-else-if="status === 'done' && !results.length" class="empty">暂无匹配结果，请确认已完善需求信息</p>
      <p v-else-if="status === 'failed'" class="empty">匹配失败，请重试</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'
import { orderAPI } from '../api'
import MatchLoading from '../components/MatchLoading.vue'
import TutorCard from '../components/TutorCard.vue'

const route = useRoute()
const router = useRouter()
const store = useDemandStore()

const demandId = Number(route.params.demand_id)
const status = ref('pending')
const results = ref([])
const selectedTutor = ref(null)
let timer = null

onMounted(() => {
  poll()
  timer = setInterval(poll, 2000)
})

onUnmounted(() => clearInterval(timer))

async function poll() {
  const data = await store.pollResult(demandId)
  status.value = data.status
  if (data.status === 'done') {
    results.value = data.result || []
    clearInterval(timer)
  }
}

function handleSelect(tutorId) { selectedTutor.value = tutorId }

async function createOrder() {
  try {
    const res = await orderAPI.create({ demand_id: demandId, tutor_id: selectedTutor.value })
    router.push(`/order/${res.data.id}`)
  } catch (e) {
    alert(e.response?.data?.msg || '创建订单失败')
  }
}
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:600px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; margin-bottom:16px; }
.create-btn { width:100%; padding:12px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; margin-top:12px; }
.empty { text-align:center; color:#9ca3af; padding:48px 0; }
</style>
```

- [ ] **Step 6: Commit**

```bash
git add frontend/src/views/DashboardPage.vue frontend/src/views/MatchResultPage.vue frontend/src/components/
git commit -m "feat: add dashboard, demand form/card, tutor card, match result pages"
```

---

### Task 15: 实现 Order + Profile + Rating 页面

**Files:**
- Create: `frontend/src/views/OrderDetailPage.vue`
- Create: `frontend/src/views/ProfilePage.vue`
- Create: `frontend/src/components/OrderCard.vue`
- Create: `frontend/src/components/RatingForm.vue`
- Create: `frontend/src/views/DemandDetailPage.vue`

- [ ] **Step 1: 创建 OrderCard.vue**

```vue
<template>
  <div class="order-card" @click="$emit('click')">
    <div class="header">
      <span class="title">订单 #{{ order.id }}</span>
      <span class="status">{{ statusText }}</span>
    </div>
    <div class="info">
      <span v-if="order.demand_title">需求: {{ order.demand_title }}</span>
      <span>家教: {{ order.tutor_name || '--' }}</span>
      <span>金额: {{ order.total_amount }}元</span>
      <span>{{ order.create_time?.slice(0, 10) }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ order: Object })
defineEmits(['click'])
const statusText = computed(() => {
  const m = { 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }
  return m[props.order.status] || '未知'
})
</script>

<style scoped>
.order-card { background:#fff; padding:16px 20px; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,0.06); cursor:pointer; margin-bottom:10px; }
.header { display:flex; justify-content:space-between; margin-bottom:6px; }
.title { font-weight:600; color:#1f2937; }
.status { font-size:12px; padding:2px 8px; border-radius:12px; background:#f3f4f6; color:#6b7280; }
.info { display:flex; gap:12px; font-size:13px; color:#6b7280; flex-wrap:wrap; }
</style>
```

- [ ] **Step 2: 创建 RatingForm.vue**

```vue
<template>
  <div class="rating-form">
    <h3>服务评价</h3>
    <div class="stars">
      <div v-for="dim in dimensions" :key="dim.key" class="dim">
        <label>{{ dim.label }}</label>
        <div class="star-row">
          <span v-for="s in 5" :key="s" :class="starClass(dim.key, s)" @click="scores[dim.key] = s">★</span>
        </div>
      </div>
    </div>
    <div class="dim">
      <label>综合评价</label>
      <div class="star-row">
        <span v-for="s in 5" :key="s" :class="s <= overall ? 'star on' : 'star'" @click="overall = s">★</span>
      </div>
    </div>
    <textarea v-model="comment" placeholder="写下你的评价..." rows="3"></textarea>
    <button @click="submit" :disabled="loading">{{ loading ? '提交中...' : '提交评价' }}</button>
    <p v-if="msg">{{ msg }}</p>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { ratingAPI } from '../api'

const props = defineProps({ orderId: [Number, String] })
const emit = defineEmits(['submitted'])

const dimensions = [
  { key: 'teaching_score', label: '教学能力' },
  { key: 'attitude_score', label: '教学态度' },
  { key: 'punctuality_score', label: '守时情况' }
]
const scores = reactive({ teaching_score: 5, attitude_score: 5, punctuality_score: 5 })
const overall = ref(5)
const comment = ref('')
const loading = ref(false)
const msg = ref('')

function starClass(dim, s) {
  return s <= scores[dim] ? 'star on' : 'star'
}

async function submit() {
  loading.value = true
  try {
    await ratingAPI.submit({
      order_id: Number(props.orderId),
      ...scores,
      overall_score: overall.value,
      comment: comment.value
    })
    msg.value = '评价成功'
    emit('submitted')
  } catch (e) {
    msg.value = e.response?.data?.msg || '提交失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.rating-form { background:#fff; padding:20px; border-radius:10px; }
h3 { margin:0 0 16px; color:#1f2937; }
.dim { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.dim label { font-size:13px; color:#374151; }
.star-row { display:flex; gap:4px; }
.star { font-size:24px; color:#d1d5db; cursor:pointer; transition:color 0.1s; }
.star.on { color:#f59e0b; }
textarea { width:100%; margin:12px 0; padding:10px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { padding:8px 20px; background:#2563eb; color:#fff; border:none; border-radius:6px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
</style>
```

- [ ] **Step 3: 创建 OrderDetailPage.vue**

```vue
<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.back()">返回</button></nav>
    <div class="container">
      <div v-if="route.params.id === '0'">
        <h2>我的订单</h2>
        <p v-if="!orders.length" class="empty">暂无订单</p>
        <OrderCard v-for="o in orders" :key="o.id" :order="o" @click="$router.push(`/order/${o.id}`)" />
      </div>
      <div v-else-if="order">
        <h2>订单详情</h2>
        <div class="detail">
          <div class="row"><span class="label">订单状态</span><span>{{ statusText }}</span></div>
          <div class="row"><span class="label">需求标题</span><span>{{ order.demand_title }}</span></div>
          <div class="row"><span class="label">家教</span><span>{{ order.tutor_name }} · {{ order.tutor_school }}</span></div>
          <div class="row"><span class="label">联系电话</span><span>{{ order.tutor_phone || '--' }}</span></div>
          <div class="row"><span class="label">金额</span><span>{{ order.total_amount }}元</span></div>
          <div class="row"><span class="label">创建时间</span><span>{{ order.create_time?.slice(0, 10) }}</span></div>
        </div>
        <div class="actions" v-if="order.status === 2">
          <button @click="finishOrder" :disabled="loading">确认完成</button>
        </div>
        <RatingForm v-if="order.status === 3 && !rated" :order-id="order.id" @submitted="rated = true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderAPI } from '../api'
import OrderCard from '../components/OrderCard.vue'
import RatingForm from '../components/RatingForm.vue'

const route = useRoute()
const router = useRouter()
const orders = ref([])
const order = ref(null)
const loading = ref(false)
const rated = ref(false)

const statusText = computed(() => {
  const m = { 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }
  return m[order.value?.status] || '--'
})

onMounted(async () => {
  const id = route.params.id
  if (id === '0') {
    const res = await orderAPI.list()
    orders.value = res.data
  } else {
    const res = await orderAPI.detail(Number(id))
    order.value = res.data
  }
})

async function finishOrder() {
  loading.value = true
  try {
    await orderAPI.updateStatus(order.value.id, 3)
    order.value.status = 3
  } catch (e) {
    alert(e.response?.data?.msg || '操作失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:600px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; margin-bottom:16px; }
.empty { color:#9ca3af; text-align:center; padding:48px 0; }
.detail { background:#fff; padding:20px; border-radius:10px; margin-bottom:16px; }
.row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f3f4f6; font-size:14px; }
.row:last-child { border:none; }
.label { color:#6b7280; }
.actions { margin:16px 0; }
.actions button { padding:10px 24px; background:#059669; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
.actions button:disabled { opacity:0.6; }
</style>
```

- [ ] **Step 4: 创建 ProfilePage.vue**

```vue
<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.push('/dashboard')">返回工作台</button></nav>
    <div class="container">
      <h2>个人信息</h2>
      <form @submit.prevent="save">
        <input v-model="form.phone" placeholder="手机号" />
        <input v-model="form.email" placeholder="邮箱" />

        <div v-if="auth.user?.user_type === 1">
          <h3>家长信息</h3>
          <input v-model="form.real_name" placeholder="真实姓名" />
          <input v-model="form.address" placeholder="家庭地址" />
          <input v-model="form.location" placeholder="所在区域" />
        </div>

        <div v-if="auth.user?.user_type === 2">
          <h3>家教信息</h3>
          <input v-model="form.real_name" placeholder="真实姓名" />
          <input v-model="form.school" placeholder="学校" />
          <input v-model="form.major" placeholder="专业" />
          <input v-model="form.grade" placeholder="年级" />
          <input v-model="form.education" placeholder="学历" />
          <input v-model.number="form.teaching_exp" type="number" placeholder="教学经验(年)" />
          <input v-model.number="form.hourly_rate" type="number" placeholder="时薪(元/小时)" />
          <input v-model="form.location" placeholder="所在区域" />
          <textarea v-model="form.introduction" placeholder="个人简介" rows="3"></textarea>
        </div>

        <button :disabled="saving">{{ saving ? '保存中...' : '保存' }}</button>
      </form>
      <p v-if="msg" :class="msgType">{{ msg }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authAPI } from '../api'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({})
const saving = ref(false)
const msg = ref('')
const msgType = ref('')

onMounted(async () => {
  await auth.fetchUser()
  Object.assign(form, auth.user || {})
})

async function save() {
  saving.value = true
  try {
    await authAPI.updateProfile({ ...form })
    msg.value = '保存成功'
    msgType.value = 'success'
  } catch (e) {
    msg.value = e.response?.data?.msg || '保存失败'
    msgType.value = 'error'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:500px; margin:24px auto; padding:0 16px; }
h2 { color:#1f2937; margin-bottom:16px; }
h3 { color:#374151; margin:16px 0 8px; font-size:15px; }
input, textarea { width:100%; padding:10px; margin-bottom:12px; border:1px solid #d1d5db; border-radius:8px; font-size:14px; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
button:disabled { opacity:0.6; }
.success { color:#16a34a; font-size:13px; }
.error { color:#dc2626; font-size:13px; }
</style>
```

- [ ] **Step 5: 创建 DemandDetailPage.vue**

```vue
<template>
  <div class="page">
    <nav><span class="logo">趣学喵</span><button @click="$router.push('/dashboard')">返回</button></nav>
    <div class="container">
      <h2 v-if="demand">{{ demand.title }}</h2>
      <div v-if="demand" class="detail">
        <div class="row"><span class="label">学科</span><span>{{ demand.subject }} · {{ demand.grade }}</span></div>
        <div class="row"><span class="label">区域</span><span>{{ demand.location || '--' }}</span></div>
        <div class="row"><span class="label">预算</span><span>{{ demand.budget }}元/时</span></div>
        <div class="row"><span class="label">状态</span><span>{{ statusText }}</span></div>
        <div class="row"><span class="label">描述</span><span>{{ demand.description || '--' }}</span></div>
        <div class="row"><span class="label">要求</span><span>{{ demand.requirements || '--' }}</span></div>
      </div>
      <div v-if="demand && demand.status === 1" class="actions">
        <button @click="goMatch">AI 智能匹配</button>
      </div>
      <div v-if="demand && demand.match_status === 'done' && demand.match_result?.length" class="actions">
        <button class="secondary" @click="goMatch">查看匹配结果</button>
      </div>
      <p v-if="!demand" class="empty">需求不存在</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDemandStore } from '../stores/demand'

const route = useRoute()
const router = useRouter()
const store = useDemandStore()
const demand = ref(null)

const statusText = computed(() => {
  const m = { 1: '招募中', 2: '已匹配', 3: '已完成', 4: '已取消' }
  return m[demand.value?.status] || '--'
})

onMounted(async () => {
  await store.fetchDetail(Number(route.params.id))
  demand.value = store.currentDemand
})

function goMatch() { router.push(`/match/${demand.value.id}`) }
</script>

<style scoped>
.page { min-height:100vh; background:#f5f5f5; }
nav { display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; }
.logo { font-size:20px; font-weight:700; color:#2563eb; }
nav button { padding:6px 14px; border:1px solid #d1d5db; border-radius:6px; background:#fff; font-size:13px; cursor:pointer; }
.container { max-width:600px; margin:24px auto; padding:0 16px; }
.detail { background:#fff; padding:20px; border-radius:10px; }
.row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f3f4f6; font-size:14px; }
.row:last-child { border:none; }
.label { color:#6b7280; }
.actions { margin:16px 0; }
.actions button { padding:10px 24px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; margin-right:8px; }
.actions button.secondary { background:#059669; }
.empty { text-align:center; color:#9ca3af; padding:48px 0; }
h2 { margin-bottom:16px; }
</style>
```

- [ ] **Step 6: Commit**

```bash
git add frontend/src/views/OrderDetailPage.vue frontend/src/views/ProfilePage.vue frontend/src/views/DemandDetailPage.vue frontend/src/components/OrderCard.vue frontend/src/components/RatingForm.vue
git commit -m "feat: add order detail, profile edit, and rating pages"
```

---

### Task 16: 初始化知识库数据与端到端集成测试

**Files:**
- Create: `backend/seed_kb.py`

- [ ] **Step 1: 创建知识库种子脚本 backend/seed_kb.py**

```python
"""将现有 tutor_info 数据向量化写入 ChromaDB"""
import sys
sys.path.insert(0, '..')
from ai_module.rag import KnowledgeBase

kb = KnowledgeBase()

# 导入一些初始学科知识点文档
docs = [
    ("subj_math_primary", "小学数学知识点：四则运算、分数与小数、几何初步、应用题解题技巧、逻辑思维训练", {"subject": "数学", "grade": "小学"}),
    ("subj_math_junior", "初中数学知识点：代数基础、几何证明、函数入门、方程与不等式、统计与概率", {"subject": "数学", "grade": "初中"}),
    ("subj_math_senior", "高中数学知识点：函数与导数、解析几何、数列与极限、概率统计、向量与立体几何", {"subject": "数学", "grade": "高中"}),
    ("subj_eng_primary", "小学英语知识点：字母与发音、基础词汇、简单对话、自然拼读、绘本阅读", {"subject": "英语", "grade": "小学"}),
    ("subj_eng_junior", "初中英语知识点：语法体系、完形填空、阅读理解、书面表达、听力训练", {"subject": "英语", "grade": "初中"}),
    ("subj_eng_senior", "高中英语知识点：高级语法、长难句分析、写作模板、翻译技巧、真题训练", {"subject": "英语", "grade": "高中"}),
    ("subj_chn_primary", "小学语文知识点：拼音与识字、阅读理解、作文基础、古诗词背诵、成语故事", {"subject": "语文", "grade": "小学"}),
    ("subj_chn_junior", "初中语文知识点：文言文阅读、现代文阅读、议论文写作、语法修辞、名著导读", {"subject": "语文", "grade": "初中"}),
    ("subj_chn_senior", "高中语文知识点：文言文翻译、论述文写作、诗歌鉴赏、文学常识、语言文字运用", {"subject": "语文", "grade": "高中"}),
    ("subj_phy_junior", "初中物理知识点：力学基础、电学入门、光学、热学、声现象", {"subject": "物理", "grade": "初中"}),
    ("subj_phy_senior", "高中物理知识点：牛顿力学、电磁学、热力学、光学与原子物理、实验专题", {"subject": "物理", "grade": "高中"}),
    ("subj_chem_junior", "初中化学知识点：物质构成、化学方程式、溶液、酸碱盐、金属活动性", {"subject": "化学", "grade": "初中"}),
    ("subj_chem_senior", "高中化学知识点：物质结构、化学反应原理、有机化学、电化学、化学实验", {"subject": "化学", "grade": "高中"}),
]

kb.add_batch(docs)
print(f"知识库初始化完成，共 {kb.count()} 条记录")
```

- [ ] **Step 2: 端到端验证流程**

```bash
# 1. 确保 MySQL 运行 + 创建数据库
mysql -u root -e "CREATE DATABASE IF NOT EXISTS quxuemiao CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 启动 Flask 后端
cd backend && pip install -r requirements.txt && python app.py

# 3. 初始化知识库
python backend/seed_kb.py

# 4. 启动 Vue 前端
cd frontend && npm install && npm run dev

# 5. 手动测试流程:
#    - 浏览器打开 http://localhost:5173
#    - 注册家长账号 → 注册家教账号
#    - 家教完善资料（学校、专业、技能等）
#    - 家长发布需求 → 触发 AI 匹配 → 查看推荐列表
#    - 选择家教创建订单 → 确认完成 → 提交评价
```

- [ ] **Step 3: Commit**

```bash
git add backend/seed_kb.py
git commit -m "feat: add knowledge base seed script and integration test checklist"
```

---

## 验证清单

- [ ] MySQL 数据库 `quxuemiao` 创建且表自动生成
- [ ] `POST /api/auth/register` 家长/家教注册成功
- [ ] `POST /api/auth/login` 登录返回 JWT
- [ ] `POST /api/demand/create` 发布需求成功
- [ ] `POST /api/match/run` → `GET /api/match/result/:id` 异步匹配完成
- [ ] `POST /api/order/create` 下单成功
- [ ] `PUT /api/order/:id/status` 状态流转正确
- [ ] `POST /api/rating/submit` 评价提交成功
- [ ] `GET /api/rating/tutor/:id` 返回评分历史
- [ ] Vue 前端全部 7 个页面正常渲染
- [ ] 家长端完整闭环：注册 → 登录 → 发布需求 → AI 匹配 → 查看推荐 → 下单 → 评价
