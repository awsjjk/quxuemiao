# 趣学喵 (QuXueMiao) — 家教供需匹配平台

连接家长与优质大学生家教的在线平台，聚焦天津市中小学家庭用户，实现"需求发布 → AI 智能匹配 → 订单管理 → 服务评价"完整闭环。

---

## 技术栈

| 层 | 技术 | 说明 |
|---|---|---|
| 前端 | Vue 3 + Vite + Vue Router 4 + Pinia + Axios | SPA 单页应用，Tailwind CSS (CDN) |
| 后端 | Flask 3.0 + Flask-JWT-Extended + Flask-SQLAlchemy | RESTful API，JWT 认证 |
| 数据库 | MySQL 8.0 (生产) / SQLite (开发) | 通过 `DATABASE_URL` 环境变量切换 |
| AI Embedding | sentence-transformers + BAAI/bge-small-zh-v1.5 | 本地 CPU 推理 |
| AI 向量库 | ChromaDB | 持久化向量存储，cosine 距离 |
| AI LLM | DeepSeek API (deepseek-v4-flash) | 云端大模型 |
| 部署-后端 | Render + Gunicorn | Python 3.11 |
| 部署-前端 | Vercel | 静态 SPA |
| 部署-AI | HuggingFace Spaces (Gradio) | 独立 AI 匹配服务 |

---

## 项目架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户浏览器                           │
│               Vue 3 SPA (Vercel 托管)                    │
└────────────┬───────────────────────────────┬────────────┘
             │ /api/*                        │ 页面路由
             ▼                               ▼
┌────────────────────────┐    ┌──────────────────────────┐
│   Flask REST API       │    │   Vercel 静态托管         │
│   (Render 托管)         │    │   (SPA fallback)          │
│                        │    │                          │
│  ┌──────────────────┐  │    └──────────────────────────┘
│  │ JWT 认证中间件    │  │
│  ├──────────────────┤  │
│  │ 蓝图路由模块      │  │
│  │ auth / demand    │  │
│  │ match / order    │  │
│  │ rating / course  │  │
│  │ message / payment│  │
│  │ resource / tutor │  │
│  │ ai_assistant     │  │
│  ├──────────────────┤  │
│  │ SQLAlchemy ORM   │  │
│  └────────┬─────────┘  │
└───────────┼────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
┌─────────┐   ┌─────────────────────┐
│ MySQL   │   │  AI 匹配服务         │
│ (Render │   │  (HuggingFace Spaces)│
│  PG)    │   │                     │
└─────────┘   │ ┌─────────────────┐ │
              │ │ MatchAgent      │ │
              │ │ RAG + LLM 打分   │ │
              │ └─────────────────┘ │
              │                     │
              │ ┌─────────────────┐ │
              │ │ 本地 Embedding   │ │
              │ │ bge-small-zh    │ │
              │ └─────────────────┘ │
              └─────────────────────┘
```

---

## 目录结构

```
quxuemiao/
├── backend/                       # Flask REST API 后端
│   ├── app.py                     # 应用入口，蓝图注册
│   ├── config.py                  # 数据库/JWT 配置
│   ├── models.py                  # 10 张数据表 ORM 模型
│   ├── requirements.txt           # Python 依赖
│   ├── wsgi.py                    # Gunicorn 入口
│   ├── seed_test_data.py          # 测试数据填充脚本
│   ├── seed_kb.py                 # 学科知识库向量化脚本
│   ├── routes/                    # API 路由模块
│   │   ├── auth.py                # 登录/注册/个人信息
│   │   ├── demand.py              # 需求 CRUD
│   │   ├── match.py               # AI 匹配触发与结果轮询
│   │   ├── order.py               # 订单管理
│   │   ├── rating.py              # 服务评价
│   │   ├── course.py              # 课程记录
│   │   ├── message.py             # 即时消息
│   │   ├── payment.py             # 支付记录
│   │   ├── resource.py            # 教学资源
│   │   ├── tutor_search.py        # 家教搜索筛选
│   │   └── ai_assistant.py        # AI 助手 FAQ + LLM 兜底
│   └── utils/
│       └── decorators.py          # 角色权限装饰器
│
├── ai_module/                     # 独立 AI 模块包
│   ├── config.yaml                # LLM/Embedding/RAG 配置
│   ├── llm_client.py              # DeepSeek API 调用封装
│   ├── embedding.py               # sentence-transformers 编码器
│   ├── rag.py                     # ChromaDB 向量检索 + 知识库
│   ├── agent.py                   # 匹配决策 Agent
│   └── data/
│       ├── subjects.json          # 学科知识点图谱
│       └── prompts/
│           └── match_scoring.txt  # LLM 匹配打分 Prompt
│
├── frontend/                      # Vue 3 + Vite SPA 前端
│   ├── vite.config.js             # Vite 配置 + API 代理
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── main.js                # 应用入口
│       ├── App.vue                # 根组件
│       ├── api/index.js           # Axios 实例 + 拦截器
│       ├── router/index.js        # 路由表 + 导航守卫
│       ├── stores/
│       │   ├── auth.js            # 用户认证状态
│       │   └── demand.js          # 需求与匹配状态
│       ├── views/                 # 页面组件 (14 个)
│       │   ├── LoginPage.vue
│       │   ├── RegisterPage.vue
│       │   ├── DashboardPage.vue
│       │   ├── DemandDetailPage.vue
│       │   ├── MatchResultPage.vue
│       │   ├── SelectDemandPage.vue
│       │   ├── OrderDetailPage.vue
│       │   ├── ProfilePage.vue
│       │   ├── MessagePage.vue
│       │   ├── ResourcePage.vue
│       │   ├── PaymentPage.vue
│       │   └── AIAssistantPage.vue
│       └── components/            # 公共组件 (11 个)
│           ├── DemandForm.vue
│           ├── DemandCard.vue
│           ├── TutorCard.vue
│           ├── TutorSearch.vue
│           ├── OrderCard.vue
│           ├── RatingForm.vue
│           ├── MatchModeChoice.vue
│           ├── MatchLoading.vue
│           ├── ProfileBase.vue
│           ├── ParentProfile.vue
│           ├── TutorProfile.vue
│           └── AIAssistantFAB.vue
│
├── ai_assistant_data/
│   └── faq.json                   # AI 助手 FAQ 数据 (13 条)
│
├── hf_space/                      # HuggingFace Spaces 部署
│   └── requirements.txt
│
├── docs/                          # 设计文档
├── render.yaml                    # Render 部署配置
├── vercel.json                    # Vercel 部署配置
└── runtime.txt                    # Python 版本声明
```

---

## 数据库设计

### ER 图（核心表关系）

```
┌──────────────┐     ┌──────────────┐
│   user_info  │     │  user_info   │
│  (家长用户)   │     │  (家教用户)   │
└──────┬───────┘     └──────┬───────┘
       │ 1:1                │ 1:1
       ▼                    ▼
┌──────────────┐     ┌──────────────┐
│ parent_info  │     │  tutor_info  │
└──────┬───────┘     └──────┬───────┘
       │ 1:N                │ 1:N
       ▼                    ▼
┌──────────────┐     ┌──────────────┐
│ demand_info  │     │  order_info  │
│ (需求)        │────▶│  (订单)       │
└──────────────┘     └──────┬───────┘
                            │ 1:N
                  ┌─────────┼─────────┐
                  ▼         ▼         ▼
          ┌──────────┐ ┌──────────┐ ┌──────────┐
          │ course   │ │ rating   │ │ payment  │
          │ record   │ │ info     │ │ record   │
          └──────────┘ └──────────┘ └──────────┘

辅助表（独立）:
  message_info     — 聊天消息 (N:N, sender ↔ receiver)
  teaching_resource — 教学资源库
```

### 表说明

#### 用户与身份 (3 张)

| 表 | 说明 | 关键字段 |
|---|---|---|
| `user_info` | 基础用户表，家长和家教共用 | username, password, phone, email, user_type (1=家长, 2=家教, 3=管理员) |
| `parent_info` | 家长档案，1:1 关联 user | real_name, address, location, children_info (JSON), preference (JSON) |
| `tutor_info` | 家教档案，1:1 关联 user | school, major, education, skills (JSON), teaching_exp, hourly_rate, certificates (JSON), verification_status |

#### 核心业务 (4 张)

| 表 | 说明 | 关键字段 |
|---|---|---|
| `demand_info` | 家教需求，由家长发布 | subject, grade, budget, time_slots (JSON), match_result (JSON), match_status, status (1=招募中/2=已匹配/3=已完成/4=已取消) |
| `order_info` | 订单，关联需求与家教 | demand_id, parent_id, tutor_id, total_amount, status (1=待支付/2=进行中/3=已完成/4=已取消/5=退款中/6=已退款) |
| `course_record` | 课程记录，属于订单 | order_id, course_date, content, homework, knowledge_points (JSON), student_performance |
| `rating_info` | 服务评价，属于订单 | order_id, teaching_score, attitude_score, punctuality_score, overall_score, comment |

#### 辅助功能 (3 张)

| 表 | 说明 |
|---|---|
| `message_info` | 聊天消息，支持文本/图片/语音 |
| `payment_record` | 模拟支付记录 |
| `teaching_resource` | 教学资源（课件/题库/教案） |

---

## API 设计

所有 API 前缀为 `/api`，JWT 令牌通过 `Authorization: Bearer <token>` 请求头传递，有效期 24 小时。

### 认证 `/api/auth`

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| POST | `/api/auth/login` | 否 | 用户名+密码登录，返回 JWT 令牌与用户信息 |
| POST | `/api/auth/register` | 否 | 注册（选择家长/家教身份），自动创建角色档案 |
| GET | `/api/auth/user_info` | JWT | 获取当前登录用户信息（含角色详情） |
| PUT | `/api/auth/update_profile` | JWT | 更新个人资料（含角色特有字段如技能、可用时间等） |

### 需求 `/api/demand`

| 方法 | 路径 | 认证 | 角色 | 说明 |
|---|---|---|---|---|
| POST | `/api/demand/create` | JWT | 家长 | 发布家教需求 |
| GET | `/api/demand/list` | JWT | — | 查看我的需求列表 |
| GET | `/api/demand/<id>` | JWT | — | 需求详情 |
| PUT | `/api/demand/<id>` | JWT | 家长 | 修改或取消需求 |

### AI 匹配 `/api/match`

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| POST | `/api/match/run` | JWT | 触发异步 AI 匹配，后台线程执行，返回确认 |
| GET | `/api/match/result/<demand_id>` | JWT | 轮询匹配状态 (pending → processing → done/failed) 与结果 |

### 订单 `/api/order`

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| POST | `/api/order/create` | JWT | 家长基于匹配结果创建订单 |
| GET | `/api/order/list` | JWT | 我的订单列表（家长/家教双视角自动切换） |
| GET | `/api/order/<id>` | JWT | 订单详情（含家教信息） |
| PUT | `/api/order/<id>/status` | JWT | 更新订单状态 |

### 评价 `/api/rating`

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| POST | `/api/rating/submit` | JWT | 提交评价（教学/态度/守时/综合四维打分 + 文字评论） |
| GET | `/api/rating/tutor/<tutor_id>` | 否 | 查看家教的历史评价与平均分 |

### 其他模块

| 模块 | 前缀 | 说明 |
|---|---|---|
| 课程记录 | `/api/course` | 创建/查询/更新课程记录，关联订单 |
| 即时消息 | `/api/message` | 发送消息、搜索用户、会话列表、聊天记录轮询 |
| 家教搜索 | `/api/tutor` | 多条件筛选（学科/学校/学历/区域/时薪/经验） |
| AI 助手 | `/api/ai_assistant` | FAQ 向量匹配 + LLM 兜底问答 |
| 教学资源 | `/api/resource` | 资源列表/上传/详情（支持学科/年级/类型筛选） |
| 支付记录 | `/api/payment` | 模拟支付记录创建与查询 |

---

## AI 匹配模块设计

### 整体架构

```
家长触发匹配
     │
     ▼
POST /api/match/run
     │
     ▼
后台线程启动
     │
     ├──▶ 步骤1: 规则初筛 (MySQL SQL)
     │    按学科 + 年级 + 区域 + 预算过滤 → 候选池 (≤50人)
     │
     ├──▶ 步骤2: RAG 知识检索 (ChromaDB)
     │    需求向量化 → 检索学科知识点 + 家教资质 → 增强上下文
     │
     ├──▶ 步骤3: LLM 智能打分 (DeepSeek)
     │    构造 Prompt (需求 + 候选人 + RAG上下文 + 学科知识点)
     │    → JSON 结构化输出 [{tutor_id, score, reason}]
     │
     └──▶ 步骤4: 结果持久化
         写入 demand_info.match_result (JSON)
         更新 match_status = 'done'
     │
     ▼
前端轮询 GET /api/match/result/<demand_id>
  每 3 秒查询，最多 15 次 (45 秒超时)
```

### 匹配评分维度

| 维度 | 说明 | 权重参考 |
|---|---|---|
| 学科匹配 | 家教技能标签与需求学科的吻合度 | 高 |
| 经验匹配 | 教学经验年限与需求的匹配程度 | 高 |
| 区域时间匹配 | 地理位置相近 + 可用时间覆盖 | 中 |
| 性价比匹配 | 时薪与预算的契合度 | 中 |

### AI 核心组件

```
ai_module/
├── config.yaml        # DeepSeek API 配置、Embedding 模型、RAG top_k
├── llm_client.py      # 统一 LLM 调用，支持 JSON 格式响应
├── embedding.py       # BAAI/bge-small-zh-v1.5 单例编码器，Lazy 加载
├── rag.py             # ChromaDB 封装：RAGRetriever (搜索) + KnowledgeBase (增删)
└── agent.py           # MatchAgent — 编排匹配流程，组合 RAG + LLM
```

### 部署模式

支持两种 AI 调用模式：

1. **本地直调** — 开发环境，`MatchAgent` 直接 import 使用，模型本地推理
2. **远程代理** — 生产环境，通过 HuggingFace Spaces Gradio API 调用，`HF_MATCH_API_URL` 环境变量配置

---

## 前端架构

### 路由表

| 路径 | 页面 | 认证 | 说明 |
|---|---|---|---|
| `/login` | LoginPage | 否 | 分屏登录页（左品牌/右表单） |
| `/register` | RegisterPage | 否 | 注册页，身份选择 |
| `/dashboard` | DashboardPage | 是 | 主工作台，家长/家教双视图 |
| `/demand/:id` | DemandDetailPage | 是 | 需求详情 + 匹配触发入口 |
| `/match/:demand_id` | MatchResultPage | 是 | 匹配结果（轮询加载） |
| `/select-demand` | SelectDemandPage | 是 | 选择需求 → 确认下单 |
| `/order/:id` | OrderDetailPage | 是 | 订单详情/列表，含课程与评价 |
| `/profile` | ProfilePage | 是 | 个人资料编辑 |
| `/messages` `/messages/:partner_id` | MessagePage | 是 | 会话列表 + 聊天 |
| `/resources` | ResourcePage | 是 | 教学资源浏览与上传 |
| `/payments` | PaymentPage | 是 | 支付记录 |
| `/ai-assistant` | AIAssistantPage | 是 | AI 助手问答 |

### 状态管理 (Pinia)

- **auth store** — 用户信息、JWT 令牌、登录状态，提供 login / register / fetchUser / logout 操作
- **demand store** — 需求列表、当前需求、匹配结果、匹配状态，提供 list / detail / create / runMatch / pollResult 操作

### 导航守卫

`router.beforeEach` 检查 `meta.auth` 标记，未登录用户重定向至 `/login`。

### 核心用户流程

```
家长: 注册 → 完善资料 → 发布需求 → AI匹配/手动搜索 → 选择家教 → 创建订单 → 课程记录 → 完成评价
家教: 注册 → 完善资料(技能/时间/证书) → 被匹配/被搜索 → 接单 → 课程记录 → 获得评价
```

---

## 部署架构

```
                    ┌──────────────────┐
                    │   Vercel (CDN)    │
                    │   Vue 3 SPA       │
                    │   frontend/dist   │
                    └────────┬─────────┘
                             │ /api/*
                             ▼
                    ┌──────────────────┐
                    │   Render (Web)    │
                    │   Flask + Gunicorn│
                    │   Oregon Region   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              │
    ┌─────────────┐  ┌───────────┐         │
    │ Render PG   │  │ HuggingFace│         │
    │ (PostgreSQL)│  │ Spaces    │         │
    └─────────────┘  │ AI 匹配    │         │
                     │ Gradio API│         │
                     └───────────┘         │
                                           │
                     ┌─────────────────────┘
                     ▼
              ┌─────────────┐
              │ DeepSeek API│
              │ (云端 LLM)   │
              └─────────────┘
```

环境变量（Render 侧）：

| 变量 | 说明 |
|---|---|
| `DATABASE_URL` | Render PostgreSQL 连接串 |
| `JWT_SECRET_KEY` | JWT 签名密钥 |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `HF_MATCH_API_URL` | HuggingFace Spaces 匹配 API 地址 |

---

## 本地开发

### 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0 (或使用 SQLite，无需额外安装)

### 后端

```bash
cd backend
pip install -r requirements.txt

# 配置环境变量（可选，默认使用本地 MySQL）
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password

# 启动服务 (端口 5000)
python app.py
```

### 前端

```bash
cd frontend
npm install
npm run dev        # 端口 5173，API 代理到 localhost:5000
```

### 初始化数据

```bash
# 插入测试用户（10位家长 + 10位家教）
cd backend
python seed_test_data.py

# 构建学科知识向量库（ChromaDB）
python seed_kb.py
```

### AI 模块（可选）

```bash
# 需要设置 DeepSeek API Key
export DEEPSEEK_API_KEY=your_key

# 在 Python 中直接调用
from ai_module.agent import MatchAgent
agent = MatchAgent()
results = agent.match(demand, candidates)
```

---

## 设计决策记录

1. **前后端分离 SPA** — Vue 3 独立部署于 Vercel，Flask 纯 API 部署于 Render，职责清晰，独立扩缩容
2. **JWT 无状态认证** — 避免服务端 Session，适配多实例部署，令牌有效期 24 小时
3. **AI 匹配异步执行** — 匹配耗时较长 (LLM 调用)，通过后台线程异步执行 + 前端轮询，避免 HTTP 超时
4. **规则初筛 + AI 精排** — 先用 MySQL SQL 按硬约束过滤候选池，再交给 LLM 做语义匹配打分，兼顾效率与质量
5. **本地 Embedding + 云端 LLM** — 向量检索用本地模型 (BAAI/bge-small-zh-v1.5)，避免 API 延迟；LLM 推理用云端 DeepSeek，降低运维成本
6. **AI 助手混合策略** — FAQ 向量匹配优先 (相似度 ≥0.75 直接返回)，LLM 生成兜底，在用户体验与成本间取平衡
7. **多环境数据库兼容** — 通过 `DATABASE_URL` 环境变量自动切换 PostgreSQL (生产) / MySQL (本地)，SQLAlchemy 屏蔽差异
