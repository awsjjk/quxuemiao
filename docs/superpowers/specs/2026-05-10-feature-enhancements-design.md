# 趣学喵平台功能增强设计文档

**日期**: 2026-05-10
**分支**: main
**状态**: 设计已确认，待实现

---

## 概述

本文档涵盖四个功能增强：
1. 消息功能改造（用户名搜索替代ID输入）
2. 个人信息页面重新设计（分角色结构化表单）
3. 发布需求组件增强（AI匹配 + 手动筛选双路径）
4. AI助手模块（右下角浮动入口 + 独立页面）

技术栈保持不变：后端 Flask + SQLAlchemy + JWT，前端 Vue 3 + Vite + Pinia + Tailwind CSS。

---

## 模块1：消息功能改造

### 后端变更

**文件**: `backend/routes/message.py`

#### 新增接口：`GET /api/message/search_user`

```python
@message_bp.route('/search_user', methods=['GET'])
@jwt_required()
def search_user():
    username = request.args.get('username', '')
    current_user_id = int(get_jwt_identity())
    if not username:
        return jsonify({"code": 400, "msg": "请提供用户名"}), 400
    user = User.query.filter(
        User.username == username,
        User.id != current_user_id
    ).first()
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404
    return jsonify({"code": 200, "data": {
        "id": user.id,
        "username": user.username,
        "user_type": user.user_type,
        "role_text": {1: "家长", 2: "家教", 3: "管理员"}.get(user.user_type, "")
    }}), 200
```

#### 修改接口：`POST /api/message/send`

- `receiver_id` 改为 `receiver_username`
- 后端根据 username 查找用户，找不到返回 `{"code": 404, "msg": "用户不存在"}`
- 若 `receiver.id == sender.id` 返回 `{"code": 400, "msg": "不能给自己发消息"}`

### 前端变更

**文件**: `frontend/src/views/MessagePage.vue`

- 新会话输入区：`<input type="number">` → `<input type="text" placeholder="输入对方用户名">`
- 点击"开始聊天"调用 `searchUser` 校验用户名存在性
- 对方用户名旁显示角色标签（家长/家教）
- 错误提示：
  - 输入自己用户名 → "不能给自己发消息"
  - 用户不存在 → "用户不存在"

**文件**: `frontend/src/api/index.js` — 新增 `messageAPI.searchUser(username)`

### 数据流

```
用户输入用户名 → 点击"开始聊天"
  → messageAPI.searchUser(username)
  → 200: 找到用户，打开聊天
  → 404: 显示"用户不存在"
  → 400: username为空时自己用户名，显示"不能给自己发消息"
```

---

## 模块2：个人信息页重新设计

### 组件拆分

```
ProfilePage.vue
├── ProfileBase.vue      # 账号信息（双方共用）
├── ParentProfile.vue    # 家长专属表单
└── TutorProfile.vue     # 家教专属表单
```

### 账号信息区块（ProfileBase.vue，双方共用）

| 字段 | 类型 | 可编辑 | 备注 |
|------|------|--------|------|
| username | 文本 | 否（只读） | 灰色禁用 |
| user_type | 文本 | 否（只读） | 显示"家长"/"家教" |
| phone | 文本 | 是 | |
| email | 文本 | 是 | |
| avatar | 文本 | 是 | URL输入 |
| sex | 下拉 | 是 | 未设置/男/女 |
| birthday | 日期 | 是 | date picker |
| qq_openid | 按钮 | 部分 | "🔗 绑定QQ"，点击→"该功能暂不可用" |
| wechat_openid | 按钮 | 部分 | "🔗 绑定微信"，点击→"该功能暂不可用" |

### 家长信息区块（ParentProfile.vue）

| 字段 | 类型 | 说明 |
|------|------|------|
| real_name | 文本 | 真实姓名 |
| location | 下拉 | 所在区域 |
| address | 文本 | 家庭地址 |
| children_info (JSON) | **结构化列表** | 可添加/删除孩子，每项含姓名、年级、年龄 |
| preference (JSON) | **标签选择器** | 学科偏好（多选标签：数学/英语/语文/物理/化学/生物/政治/历史/地理/其他外语），时间偏好（多选标签） |

### 家教信息区块（TutorProfile.vue）

| 字段 | 类型 | 说明 |
|------|------|------|
| real_name | 文本 | 真实姓名 |
| id_card | 密码型文本 | 使用 type="password" 输入 |
| school | 文本 | 学校名称 |
| major | 文本 | 专业 |
| grade | 文本 | 年级 |
| education | 下拉 | 本科/硕士/博士 |
| teaching_exp | 数字 | 教学经验（年） |
| hourly_rate | 数字 | 时薪（元/h） |
| location | 下拉 | 所在区域 |
| verification_status | **状态 + 按钮** | 未认证显示"📝 申请认证"按钮；审核中显示进度；已认证显示绿色徽章 |
| skills (JSON) | **标签选择器** | 预设学科标签 + "+ 自定义"输入 |
| certificates (JSON) | **动态列表** | 可添加/删除，每项含证书名称 |
| available_time (JSON) | **7天×3时段网格** | 上午/下午/晚上 × 周一到周日，点击勾选 |
| introduction | 多行文本 | 个人简介 |

### 后端变更

**文件**: `backend/routes/auth.py`

- `GET /api/auth/user_info` 需返回所有 User + Parent/Tutor 字段
- `PUT /api/auth/update_profile` 需支持所有新增字段的更新

---

## 模块3：发布需求组件增强

### 组件拆分

```
DemandForm.vue          # 增强：新增加学科选项 + 双路径选择
├── MatchModeChoice.vue # 二选一卡片：AI匹配 / 手动筛选
├── TutorSearch.vue     # 手动筛选面板 + 搜索结果
└── TutorCard.vue       # B型卡片组件（可复用）
```

### 工作流程

1. 家长填写需求表单（标题、学科、年级、描述、区域、预算、时长、频率、要求）
2. 学科下拉增加：生物、政治、历史、地理、其他外语
3. 表单下方显示二选一卡片：
   - 🤖 **AI智能匹配**：调用现有 `ai_module/agent.py` 的 `MatchAgent.match()`
   - 🔍 **手动筛选搜索**：打开筛选面板

### AI智能匹配路径

- 复用现有流程：`MatchAgent.match(demand, candidates)` → 返回 top 5
- 匹配中显示 MatchLoading 组件
- 结果展示在 MatchResultPage（已有）

### 手动筛选路径

**筛选条件**：
- 学科/技能（标签多选）
- 学校（文本输入）
- 学历（下拉）
- 所在区域（下拉）
- 时薪范围（最低-最高）
- 教学经验（下拉：1年+/2年+/3年+/5年+）
- 仅显示已认证家教（复选框）

**搜索结果**：B型卡片列表，每张卡片含：
- 头像 + 姓名 + 认证徽章
- 学校/专业/教龄
- 右侧突出价格
- 个人简介摘要
- 信息标签（学校、区域、时间）
- "💬 发起沟通"按钮 → 跳转到 `/messages` 并预填对方用户名
- "👀 详情"按钮

**后端接口（新增）**：
`GET /api/tutor/search?subject=数学&school=南开&education=本科&location=南开区&min_rate=80&max_rate=200&min_exp=2&verified_only=1`

---

## 模块4：AI助手模块

### 组件结构

```
App.vue                    # 添加浮动按钮
└── AIAssistantFAB.vue     # 右下角浮动按钮（全局）
views/AIAssistantPage.vue  # 独立路由页面
```

### 浮动按钮（所有页面右下角）

- 位置：fixed, bottom: 24px, right: 24px, z-index: 50
- 样式：52px 圆形渐变紫色按钮 + 阴影，显示 🤖 图标
- 旁边显示"💬 需要帮助吗？"气泡
- 点击跳转到 `/ai-assistant` 路由

### AI助手页面（/ai-assistant）

#### 初始状态
- 居中机器人头像 + "趣学喵AI助手"标题
- 问候语："我是您的专属助手，可以帮您了解平台、解答疑问"
- 12个预设FAQ标签（可点击），覆盖四类：

| 分类 | FAQ条目 |
|------|---------|
| 平台介绍 | 趣学喵是什么平台？、如何注册账号？、平台收费吗？ |
| 操作指南 | 如何发布家教需求？、如何联系家教？、如何查看订单？、忘记密码怎么办？ |
| 家教相关 | 家教资质如何审核？、如何选择家教？、不满意可以换家教吗？ |
| 费用相关 | 课时费怎么计算？、如何退款？、支付方式有哪些？ |

#### 三种回复路径

**路径A：点击FAQ标签**
- 前端预设映射表 `faq_map: { question_text → fixed_answer }`
- 直接显示对应固定回复，无网络请求

**路径B：用户输入文本 → 向量语义匹配**
- 后端调用 `ai_module/embedding.py` 计算用户输入向量
- 与 FAQ 库计算 cosine 相似度
- 超过阈值（0.75）→ 返回匹配FAQ的固定回复
- 未超过阈值 → 进入路径C

**路径C：LLM兜底回复**
- 调用 LLM，使用 `ai_assistant_config.yaml` 的严格配置
- system_prompt 严格限定角色：
  > "你是趣学喵家教平台的AI客服助手。你只回答与平台使用、家教服务、学习辅导相关的问 题。如果用户询问无关话题（如编程、娱乐、政治等），请礼貌回复：'抱歉，我只擅长解答 平台使用和家教相关的问题，您可以尝试其他问题。' 回复使用中文，不超过200字，不使用 Markdown格式和代码块。"

### 配置分离

**新建文件**: `ai_assistant_config.yaml`（与 `ai_module/` 同级）

```yaml
llm:
  provider: "deepseek"
  model: "deepseek-v4-flash"
  base_url: "https://api.deepseek.com"
  api_key: "sk-xxx"
  temperature: 0.1
  max_tokens: 300
  top_p: 0.9

embedding:
  model: "BAAI/bge-small-zh-v1.5"
  device: "cpu"

faq:
  faq_data_path: "ai_assistant_data/faq.json"
  similarity_threshold: 0.75
```

**新建文件**: `ai_assistant_data/faq.json` — FAQ问答对数据

```json
[
  {
    "id": "faq_001",
    "question": "趣学喵是什么平台？",
    "answer": "趣学喵是一个连接家长与优质家教的在线教育平台...",
    "keywords": ["介绍", "平台", "是什么", "趣学喵"],
    "category": "平台介绍"
  },
  ...
]
```

**后端新增**: `backend/routes/ai_assistant.py` + `ai_assistant/__init__.py`

- `POST /api/ai_assistant/chat` — 接收 user_message，执行向量匹配或LLM调用
- `GET /api/ai_assistant/faq_list` — 返回FAQ列表

### 与 ai_module 的关系

| 维度 | ai_module | ai_assistant |
|------|-----------|-------------|
| 配置 | ai_module/config.yaml | ai_assistant_config.yaml |
| temperature | 0.3 | 0.1 |
| max_tokens | 2000 | 300 |
| system_prompt | 家教匹配专家 | 平台客服助手（严格限定） |
| embedding | 知识库检索 | FAQ语义匹配 |
| 用途 | 家教匹配评分 | 用户问答对话 |

---

## 新文件清单

### 前端

| 文件 | 类型 |
|------|------|
| `frontend/src/views/AIAssistantPage.vue` | 新增 |
| `frontend/src/components/AIAssistantFAB.vue` | 新增 |
| `frontend/src/components/ProfileBase.vue` | 新增 |
| `frontend/src/components/ParentProfile.vue` | 新增 |
| `frontend/src/components/TutorProfile.vue` | 新增 |
| `frontend/src/components/TutorSearch.vue` | 新增 |
| `frontend/src/components/TutorCard.vue` | 新增 |
| `frontend/src/components/MatchModeChoice.vue` | 新增 |

### 后端

| 文件 | 类型 |
|------|------|
| `backend/routes/ai_assistant.py` | 新增 |
| `backend/routes/tutor_search.py` | 新增 |
| `ai_assistant_config.yaml` | 新增 |
| `ai_assistant_data/faq.json` | 新增 |
| `ai_assistant_data/__init__.py` | 新增 |

### 修改文件

| 文件 | 改动 |
|------|------|
| `backend/routes/message.py` | 新增 search_user，修改 send |
| `backend/routes/auth.py` | 扩展 user_info 和 update_profile |
| `backend/app.py` | 注册新蓝图 |
| `frontend/src/App.vue` | 添加 AIAssistantFAB |
| `frontend/src/router/index.js` | 新增 /ai-assistant 路由 |
| `frontend/src/api/index.js` | 新增搜索/筛选/AI助手API |
| `frontend/src/views/ProfilePage.vue` | 重构为组合组件 |
| `frontend/src/views/MessagePage.vue` | 改造用户名搜索 |
| `frontend/src/components/DemandForm.vue` | 新增学科选项 + 模式选择 |
| `frontend/src/views/DashboardPage.vue` | 新加手动筛选入口 |

---

## 自我审查

- 无 TBD/TODO 占位符
- 前后端接口对齐，无矛盾
- 与现有技术栈一致，无架构冲突
- 四个模块相互独立，可分别实现和测试
- FAQ内容、system_prompt 等文本内容在实现阶段可根据需要微调
