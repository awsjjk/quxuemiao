# 趣学喵平台部署设计文档

**日期**: 2026-05-10
**状态**: 设计已确认，待实现

## 概述

将趣学喵平台部署到 Vercel（前端）+ Render（后端）+ HuggingFace Spaces（AI 匹配服务）。

## 架构

```
Vercel (Vue 3 SPA)
  → Render (Flask + Gunicorn + PostgreSQL)
    → HuggingFace Spaces (Gradio: AI Matching / RAG / Embedding)
```

---

## 模块 1：项目结构调整

### 新增文件

| 文件 | 用途 |
|------|------|
| `vercel.json` | Vercel 前端部署配置 |
| `render.yaml` | Render 后端服务配置 |
| `backend/wsgi.py` | Gunicorn WSGI 入口 |
| `backend/runtime.txt` | 指定 Python 3.11 |
| `hf_space/app.py` | HuggingFace Gradio 应用 |
| `hf_space/requirements.txt` | HuggingFace 依赖 |
| `hf_space/ai_module/` | AI 模块拷贝 |
| `.env.example` | 环境变量模板（不含真实密钥） |

### 修改文件

| 文件 | 改动 |
|------|------|
| `backend/config.py` | 支持 `DATABASE_URL` + PostgreSQL |
| `backend/requirements.txt` | 添加 gunicorn, psycopg2-binary, requests |
| `backend/app.py` | 修复 ai_module 导入路径 |
| `frontend/src/api/index.js` | 根据环境切换 baseURL |
| `frontend/vite.config.js` | 移除 dev proxy，构建时由 VERCEL 处理 |
| `ai_module/agent.py` | 移除 sys.path.insert |
| `ai_module/rag.py` | 移除 sys.path.insert |

---

## 模块 2：数据库迁移

- MySQL → PostgreSQL（Render 原生支持）
- 配置改用 `DATABASE_URL` 环境变量
- 添加 `psycopg2-binary` 依赖
- JSON 字段 PostgreSQL 原生兼容，模型无需改动
- 本地开发可用 SQLite 回退

---

## 模块 3：环境变量

| 变量 | 用途 | 配置位置 |
|------|------|---------|
| `DATABASE_URL` | PostgreSQL 连接串 | Render Env Vars |
| `JWT_SECRET_KEY` | JWT 签名密钥 | Render Env Vars |
| `DEEPSEEK_API_KEY` | DeepSeek LLM API Key | Render Env Vars |
| `HF_MATCH_API_URL` | AI 匹配服务地址 | Render Env Vars |
| `VITE_API_BASE_URL` | 前端 API 地址 | Vercel Env Vars |

---

## 模块 4：Git 敏感信息清理

- 使用 `git filter-branch` 清除历史中 DeepSeek API Key
- 所有可能暴露的密钥移至环境变量
- Force push 更新远程仓库

---

## 模块 5：HuggingFace Spaces AI 服务

- 目录 `hf_space/`
- `app.py`：Gradio 接口，暴露 `match(demand, candidates)` 函数
- 依赖：sentence-transformers, chromadb, openai, pyyaml, numpy<2.0
- Render 后端通过 `HF_MATCH_API_URL` 调用

---

## 模块 6：前端 Vercel 部署

- `vercel.json`：sourceDirectory `frontend`，buildCommand `npm run build`，outputDirectory `dist`
- Axios baseURL：开发 `/api`（Vite proxy），生产 `${VITE_API_BASE_URL}/api`
- SPA 路由 fallback 由 Vercel 自动处理

---

## 模块 7：Render 后端部署

- `wsgi.py` 作为入口
- Gunicorn 启动：`gunicorn wsgi:app`
- Build command：`pip install -r requirements.txt`
- `runtime.txt` 指定 Python 版本

---

## 自我审查

- 无 TBD/TODO
- 三平台接口定义清晰（Rest API / Gradio）
- 与现有代码兼容，改动最小化
- 敏感信息全部通过环境变量管理
