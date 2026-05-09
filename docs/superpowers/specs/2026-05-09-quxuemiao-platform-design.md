# 趣学苗 — 家教供需匹配平台 设计文档

## Context

基于现有 Flask + SQLite 原型，升级为 **Python Flask + Vue 3 + MySQL + AI (RAG + Agent)** 的全栈平台。核心覆盖天津市内高校大学生与中小学家庭用户，实现"需求发布 → AI 匹配 → 订单管理 → 服务评价"闭环。暂不涉及支付结算、跨区域服务等第三方集成。

## 技术选型

| 层 | 选型 | 说明 |
|---|---|---|
| 前端 | Vue 3 (Composition API) + Vite + Vue Router 4 + Pinia + Axios | SPA 单页应用，前后端分离 |
| 后端 | Flask 3.0 + Flask-JWT-Extended + Flask-CORS + Flask-SQLAlchemy | RESTful API |
| 数据库 | MySQL 8.0 | 关系型数据，10 张表（复用现有 models.py） |
| AI - 向量存储 | ChromaDB | 家教资质 + 学科知识点向量检索 |
| AI - Embedding | 本地模型 | sentence-transformers |
| AI - LLM | 云端 API | config.yaml 可配置（api_key / model / endpoint） |
| AI - 匹配策略 | 规则初筛 + RAG 检索 + LLM 打分 | 异步执行 |

## 目录结构

```
quxuemiao/
├── backend/                    # Flask REST API
│   ├── app.py                  # 应用入口 + 配置
│   ├── config.py               # MySQL / JWT / LLM 配置
│   ├── requirements.txt        # Python 依赖
│   ├── models.py               # 10 张表 (复用 + 适配 MySQL)
│   ├── routes/
│   │   ├── auth.py             # 登录 / 注册 / 个人信息
│   │   ├── demand.py           # 需求 CRUD
│   │   ├── match.py            # AI 匹配触发 + 结果查询
│   │   ├── order.py            # 订单管理
│   │   └── rating.py           # 服务评价
│   └── utils/
│       └── decorators.py       # 角色权限装饰器
├── ai_module/                   # 独立 AI 模块
│   ├── config.yaml              # api_key / model / endpoint
│   ├── __init__.py
│   ├── llm_client.py            # 统一 LLM 调用接口
│   ├── embedding.py             # 本地嵌入模型 (sentence-transformers)
│   ├── rag.py                   # ChromaDB 向量检索 + 知识库管理
│   ├── agent.py                 # 匹配决策 Agent
│   └── data/
│       ├── subjects.json        # 学科知识图谱
│       └── prompts/
│           └── match_scoring.txt
├── frontend/                    # Vue 3 + Vite SPA
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/index.js      # 路由 + 守卫 + 角色权限
│       ├── views/               # 7 个页面组件
│       ├── components/          # 6 个公共组件
│       ├── stores/              # Pinia (auth + demand)
│       └── api/index.js         # Axios 实例 + 拦截器
└── .claude/
```

## API 端点设计 (15 个端点，5 组)

### Auth — `/api/auth`
| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | /api/auth/login | 登录，返回 JWT | 否 |
| POST | /api/auth/register | 注册 (家长/家教)，自动创建角色表 | 否 |
| GET | /api/auth/user_info | 当前用户信息 | JWT |
| PUT | /api/auth/update_profile | 更新个人信息 + 角色详情 | JWT |

### Demand — `/api/demand`
| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | /api/demand/create | 发布需求 | JWT |
| GET | /api/demand/list | 我的需求列表 | JWT |
| GET | /api/demand/:id | 需求详情 | JWT |
| PUT | /api/demand/:id | 修改/取消需求 | JWT |

### Match — `/api/match`
| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | /api/match/run | 触发异步匹配，返回 task_id | JWT |
| GET | /api/match/result/:demand_id | 查询匹配状态+结果 | JWT |

### Order — `/api/order`
| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | /api/order/create | 创建订单 (家长选家教) | JWT |
| GET | /api/order/list | 我的订单列表 (双视角) | JWT |
| GET | /api/order/:id | 订单详情 | JWT |
| PUT | /api/order/:id/status | 更新订单状态 | JWT |

### Rating — `/api/rating`
| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | /api/rating/submit | 提交评价 (星级+文字) | JWT |
| GET | /api/rating/tutor/:tutor_id | 查看家教评价历史 | JWT |

## AI 匹配模块设计

### 匹配流程 (异步)

```
POST /api/match/run
  → Flask 启动后台线程
  → 1. 规则引擎初筛 (MySQL SQL 查询)
      学科 + 年级 + 区域 + 时间 + 预算 → 候选池 (≤50人)
  → 2. RAG 检索 (ChromaDB)
      需求向量化 → 检索家教资质 + 学科知识点 → 构造 LLM 上下文
  → 3. LLM 打分
      Prompt = 需求 + 候选(RAG增强) + 学科知识点 → JSON 结构化输出
  → 4. 结果写入 demand_info 表的 match_result JSON 字段
  → 返回 task_id，前端轮询 GET /api/match/result/:id
```

### ai_module 内部接口

```python
# llm_client.py
class LLMClient:
    def chat(self, prompt: str) -> str: ...

# embedding.py
def embed(texts: list[str]) -> list[list[float]]: ...  # 本地 sentence-transformers

# rag.py
class RAGRetriever:
    def search(self, query: str, top_k: int = 10) -> list[dict]: ...
class KnowledgeBase:
    def add(self, doc: dict) -> None: ...
    def delete(self, doc_id: str) -> None: ...

# agent.py
class MatchAgent:
    def match(self, demand: dict, candidates: list[dict]) -> list[dict]:
        """返回 [{tutor_id, score, reason}, ...]"""
```

## 前端路由 & 组件

### 路由（7 个页面）
| 路径 | 页面 | 认证 |
|---|---|---|
| /login | LoginPage | 否 |
| /register | RegisterPage | 否 |
| /dashboard | DashboardPage (角色分支) | JWT |
| /demand/:id | DemandDetailPage | JWT |
| /match/:demand_id | MatchResultPage | JWT |
| /order/:id | OrderDetailPage | JWT |
| /profile | ProfilePage | JWT |

### 组件（6 个公共组件）
- DemandForm — 需求发布表单
- DemandCard — 需求卡片
- TutorCard — 家教推荐卡片
- OrderCard — 订单卡片
- RatingForm — 评价表单 (星级 + 文字)
- MatchLoading — 异步匹配等待动画

### 状态 (2 个 Pinia store)
- auth — 用户信息 + JWT Token + 角色
- demand — 当前需求列表 + 匹配状态

### 核心流程
登录 → Dashboard → 发布需求 (DemandForm) → AI 匹配 (MatchLoading → TutorCard 列表) → 选择家教下单 → 订单管理 → 完成评价 (RatingForm)

## 数据库

复用现有 `models.py` 中的 10 张表，适配 MySQL (主要改动: 连接配置、JSON 字段使用 MySQL JSON 类型)：

- user_info / parent_info / tutor_info — 用户与身份
- demand_info — 家教需求
- order_info — 订单
- course_record — 课程记录
- rating_info — 评价
- message_info / payment_record / teaching_resource — 辅助表（首期不启用）

首期核心表：user_info → parent_info → demand_info → order_info → rating_info（5 张表）
伴生关联表：tutor_info（家教信息，参与匹配）

## 首期范围

**明确做**：注册/登录 → 需求发布 → AI 匹配 → 订单管理 → 服务评价
**明确不做**：支付结算、即时通讯、教学资源库、竞拍、第三方登录

## 验证计划

1. 后端：`pytest` 测试 API 端点，重点验证 auth 流程 + match 异步调用 + order 状态流转
2. 前端：Playwright 端到端测试家长完整流程（注册 → 发布需求 → AI 匹配 → 下单 → 评价）
3. AI 模块：单元测试 rag.retrieve() 检索质量 + agent.match() 输出格式
4. 手动验收：家长注册 → 家教注册 → 发布需求 → 触发匹配 → 查看推荐 → 创建订单 → 完成评价
