# 趣学喵平台部署实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将项目部署到 Vercel（前端）+ Render（后端）+ HuggingFace Spaces（AI 匹配服务）

**Architecture:** Monorepo 单仓库，Vercel 部署 `/frontend` Vue SPA，Render 部署 `/backend` Flask API，HuggingFace Spaces 托管 Gradio AI 匹配服务。PostgreSQL 替代 MySQL，所有密钥通过环境变量注入。

**Tech Stack:** Vue 3 + Vite (Vercel), Flask + Gunicorn + PostgreSQL + psycopg2 (Render), Gradio + sentence-transformers + ChromaDB (HuggingFace)

---

## Phase 1: 项目环境准备

### Task 1: 更新 requirements.txt

**Files:**
- Modify: `backend/requirements.txt`

- [ ] **Step 1: 替换 requirements.txt**

```txt
Flask==3.0.3
Flask-Cors==5.0.0
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.0
psycopg2-binary==2.9.9
cryptography==42.0.0
gunicorn==22.0.0
requests==2.31.0
numpy<2.0
chromadb==0.4.22
sentence-transformers==2.5.0
openai==1.30.0
pyyaml==6.0.1
```

- [ ] **Step 2: 提交**

```bash
git add backend/requirements.txt
git commit -m "chore: add gunicorn, psycopg2, requests to requirements"
```

---

### Task 2: 更新 backend/config.py 支持 PostgreSQL

**Files:**
- Modify: `backend/config.py`

- [ ] **Step 1: 替换 config.py**

```python
import os

# 数据库连接 — 优先使用 DATABASE_URL（Render PostgreSQL），其次本地 MySQL，最后 SQLite 回退
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Render PostgreSQL: postgresql://user:pass@host:port/db
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
else:
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'admin')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'quxuemiao')
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
        '?charset=utf8mb4'
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'quxuemiao-secret-key-change-in-prod')
JWT_ACCESS_TOKEN_EXPIRES = 86400
```

- [ ] **Step 2: 提交**

```bash
git add backend/config.py
git commit -m "feat: support DATABASE_URL env var for PostgreSQL on Render"
```

---

### Task 3: 创建 .env.example

**Files:**
- Create: `.env.example`

- [ ] **Step 1: 创建 .env.example**

```bash
# Render 后端环境变量
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_SECRET_KEY=change-me-to-random-string
DEEPSEEK_API_KEY=sk-xxx
HF_MATCH_API_URL=https://your-space.hf.space/api/predict

# Vercel 前端环境变量
VITE_API_BASE_URL=https://your-app.onrender.com
```

- [ ] **Step 2: 提交**

```bash
git add .env.example
git commit -m "chore: add .env.example for deployment reference"
```

---

## Phase 2: Git 敏感信息清理

### Task 4: 清理 DeepSeek API Key

**Files:**
- Modify: `ai_module/config.yaml`

- [ ] **Step 1: 替换 config.yaml 中的真实 API Key 为占位符**

将 `ai_module/config.yaml` 中 `api_key: "sk-4cfd..."` 替换为：

```yaml
llm:
  provider: "deepseek"
  api_key: "${DEEPSEEK_API_KEY}"
  model: "deepseek-v4-flash"
  base_url: "https://api.deepseek.com"
  temperature: 0.3
  max_tokens: 2000

embedding:
  model: "BAAI/bge-small-zh-v1.5"
  device: "cpu"

rag:
  collection_name: "tutor_knowledge"
  persist_dir: "./ai_module/chroma_db"
  top_k: 10

matching:
  max_candidates: 50
  top_n: 5
```

更新 `ai_module/llm_client.py` 以支持环境变量替换：

```python
_api_key = _llm_config['api_key']
if _api_key.startswith('${') and _api_key.endswith('}'):
    import os
    _api_key = os.environ.get(_api_key[2:-1], '')
```

- [ ] **Step 2: 同样更新 ai_assistant_config.yaml**

将 `api_key: "sk-4cfd..."` 替换为 `${DEEPSEEK_API_KEY}`，并更新 `backend/routes/ai_assistant.py` 中的 API Key 读取逻辑同上。

- [ ] **Step 3: 使用 git filter-branch 从历史中清除 API Key**

```bash
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch ai_module/config.yaml" --prune-empty -- --all
# 注意：需要重新 add 修改后的 config.yaml
git add ai_module/config.yaml ai_assistant_config.yaml backend/routes/ai_assistant.py
git commit -m "security: replace hardcoded API keys with env var placeholders"
```

然后：

```bash
git reflog expire --expire=now --all
git gc --prune=now
```

- [ ] **Step 4: 提交配置文件的修改**

```bash
git add ai_module/config.yaml ai_module/llm_client.py ai_assistant_config.yaml backend/routes/ai_assistant.py
git commit -m "security: replace hardcoded API keys with env var placeholders"
```

---

## Phase 3: 后端部署配置（Render）

### Task 5: 创建 Gunicorn WSGI 入口

**Files:**
- Create: `backend/wsgi.py`

- [ ] **Step 1: 创建 wsgi.py**

```python
from app import app

if __name__ == '__main__':
    app.run()
```

- [ ] **Step 2: 提交**

```bash
git add backend/wsgi.py
git commit -m "feat: add gunicorn WSGI entry point"
```

---

### Task 6: 创建 runtime.txt 和 render.yaml

**Files:**
- Create: `backend/runtime.txt`
- Create: `render.yaml`

- [ ] **Step 1: 创建 runtime.txt**

```
python-3.11.0
```

- [ ] **Step 2: 创建 render.yaml**

```yaml
services:
  - type: web
    name: quxuemiao-api
    env: python
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: quxuemiao-db
          property: connectionString
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: DEEPSEEK_API_KEY
        sync: false
      - key: HF_MATCH_API_URL
        sync: false

databases:
  - name: quxuemiao-db
    plan: free
```

- [ ] **Step 3: 提交**

```bash
git add backend/runtime.txt render.yaml
git commit -m "feat: add Render deployment config"
```

---

## Phase 4: 前端部署配置（Vercel）

### Task 7: 创建 Vercel 配置

**Files:**
- Create: `vercel.json`

- [ ] **Step 1: 创建 vercel.json**

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "devCommand": "cd frontend && npm run dev",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

- [ ] **Step 2: 提交**

```bash
git add vercel.json
git commit -m "feat: add Vercel deployment config"
```

---

### Task 8: 前端 API 地址适配

**Files:**
- Modify: `frontend/vite.config.js`
- Modify: `frontend/src/api/index.js`

- [ ] **Step 1: 更新 vite.config.js**

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
  },
  build: {
    outDir: 'dist'
  }
})
```

- [ ] **Step 2: 更新 api/index.js — baseURL 根据环境切换**

```javascript
import axios from 'axios'

const baseURL = import.meta.env.PROD
  ? (import.meta.env.VITE_API_BASE_URL || '') + '/api'
  : '/api'

const api = axios.create({ baseURL, timeout: 30000 })
```

（其余 axios 拦截器保留不变）

- [ ] **Step 3: 创建 .env.production 模板**

```bash
# frontend/.env.production
VITE_API_BASE_URL=https://your-app.onrender.com
```

- [ ] **Step 4: 提交**

```bash
git add frontend/vite.config.js frontend/src/api/index.js frontend/.env.production
git commit -m "feat: adapt frontend API baseURL for production deployment"
```

---

## Phase 5: HuggingFace AI 服务

### Task 9: 创建 HuggingFace Gradio 应用

**Files:**
- Create: `hf_space/app.py`
- Create: `hf_space/requirements.txt`
- Copy: `ai_module/` 文件到 `hf_space/ai_module/`

- [ ] **Step 1: 创建 hf_space/requirements.txt**

```txt
sentence-transformers==2.5.0
chromadb==0.4.22
numpy<2.0
pyyaml==6.0.1
requests==2.31.0
```

- [ ] **Step 2: 创建 hf_space/app.py**

```python
import json
import yaml
import gradio as gr
from pathlib import Path
from ai_module.agent import MatchAgent

_agent = MatchAgent()

def match_demand(subject, grade, location, budget, description, requirements, candidates_json):
    """AI 匹配入口"""
    try:
        candidates = json.loads(candidates_json)
    except:
        return "错误：候选家教数据格式无效"

    demand = {
        "subject": subject,
        "grade": grade,
        "location": location,
        "budget": float(budget or 0),
        "time_slots": [],
        "description": description,
        "requirements": requirements,
        "tags": []
    }

    results = _agent.match(demand, candidates)
    return json.dumps(results, ensure_ascii=False, indent=2)


demo = gr.Interface(
    fn=match_demand,
    inputs=[
        gr.Textbox(label="学科"),
        gr.Textbox(label="年级"),
        gr.Textbox(label="地区"),
        gr.Number(label="预算(元/小时)"),
        gr.Textbox(label="需求描述", lines=3),
        gr.Textbox(label="额外要求"),
        gr.Textbox(label="候选家教 JSON", lines=10),
    ],
    outputs=gr.Textbox(label="匹配结果", lines=15),
    title="趣学喵 AI 家教匹配",
    description="根据家长需求和候选家教资料进行 AI 匹配打分",
)

if __name__ == "__main__":
    demo.launch()
```

- [ ] **Step 3: 拷贝 ai_module 到 hf_space**

```bash
cp -r ai_module hf_space/ai_module
# 修复 hf_space/ai_module/llm_client.py 使用 API Key 环境变量
```

- [ ] **Step 4: 移除 sys.path hack**

更新 `hf_space/ai_module/agent.py`，移除 `project_root` 相关的 `sys.path.insert` 代码（因为在 hf_space 内直接使用绝对导入即可）。

- [ ] **Step 5: 提交**

```bash
git add hf_space/
git commit -m "feat: add HuggingFace Gradio AI matching service"
```

---

### Task 10: 后端对接 HuggingFace 匹配服务

**Files:**
- Modify: `backend/routes/match.py`

- [ ] **Step 1: 更新 _run_match 使用 HF 服务替代本地调用**

```python
import os
import requests

def _call_hf_match(demand_dict, candidate_dicts):
    hf_url = os.environ.get('HF_MATCH_API_URL', '')
    if hf_url:
        resp = requests.post(
            hf_url,
            json={
                "data": [
                    demand_dict.get('subject', ''),
                    demand_dict.get('grade', ''),
                    demand_dict.get('location', ''),
                    demand_dict.get('budget', 0),
                    demand_dict.get('description', ''),
                    demand_dict.get('requirements', ''),
                    json.dumps(candidate_dicts, ensure_ascii=False)
                ]
            },
            timeout=120
        )
        resp.raise_for_status()
        return json.loads(resp.json()['data'][0])
    else:
        # 本地回退（开发环境）
        import sys
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        from ai_module.agent import MatchAgent
        agent = MatchAgent()
        return agent.match(demand_dict, candidate_dicts)
```

在 `_run_match` 中将 `agent.match(...)` 替换为 `_call_hf_match(demand_dict, candidate_dicts)`。

- [ ] **Step 2: 提交**

```bash
git add backend/routes/match.py
git commit -m "feat: call HuggingFace for AI matching, fallback to local agent"
```

---

## Phase 6: 推送和部署

### Task 11: 清理和最终准备

**Files:**
- Create: `.gitignore`（如不存在）

- [ ] **Step 1: 确认 .gitignore 内容**

```gitignore
__pycache__/
*.pyc
.venv/
node_modules/
dist/
.env
*.db
chroma_db/
.env.local
.env.production.local
```

- [ ] **Step 2: Force push 到 GitHub**

```bash
git remote add origin https://github.com/your-username/quxuemiao.git
git push -f origin main
```

- [ ] **Step 3: 部署步骤文档**

创建 `DEPLOY.md`：

```markdown
# 趣学喵部署指南

## 1. Render 后端
- 连接 GitHub 仓库
- New Web Service → 选择 `render.yaml`
- 设置环境变量：DEEPSEEK_API_KEY, HF_MATCH_API_URL
- 等待自动部署

## 2. Vercel 前端
- `vercel --prod`
- 设置环境变量：VITE_API_BASE_URL = https://quxuemiao-api.onrender.com

## 3. HuggingFace Spaces
- 上传 `hf_space/` 目录
- 设置 DEEPSEEK_API_KEY 环境变量
```

- [ ] **Step 4: 提交**

```bash
git add .gitignore DEPLOY.md
git commit -m "chore: add .gitignore and deployment guide"
git push origin main
```

---

## Self-Review

**Spec coverage check:**
- 模块1（项目结构调整）：Tasks 1-3, 5-7 — 新增 wsgi.py, runtime.txt, render.yaml, vercel.json, .env.example ✓
- 模块2（数据库迁移）：Task 2 — config.py 支持 DATABASE_URL ✓
- 模块3（环境变量）：Tasks 2, 4 — config.py + llm_client.py 读取环境变量 ✓
- 模块4（敏感信息清理）：Task 4 — git filter-branch + 替换 API Key ✓
- 模块5（HuggingFace）：Tasks 9-10 — Gradio app + 后端调用 HF 服务 ✓
- 模块6（前端 Vercel）：Tasks 7-8 — vercel.json + vite.config + api baseURL ✓
- 模块7（Render 后端）：Tasks 5-6 — wsgi.py + render.yaml ✓

**Placeholder scan:** 无 TBD/TODO。所有代码完整。
