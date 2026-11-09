# hf_space — AI 家教匹配服务（HuggingFace Spaces 部署版）

这是「趣学喵（QuXueMiao）」家教供需匹配平台的 **独立 AI 匹配服务**，用于部署到 [HuggingFace Spaces](https://huggingface.co/spaces)，以 Gradio Web 应用 + HTTP API 的形式对外提供「家长需求 → 候选家教智能打分」能力。

主项目的 Flask 后端（部署于 Render）通过 `HF_MATCH_API_URL` 环境变量远程调用本服务，实现 AI 匹配的解耦与独立扩缩容。

---

## 功能说明

输入家长需求 + 候选家教列表，输出按总分排序的匹配结果：

- **规则初筛 + RAG 检索 + LLM 打分** 三段式匹配流程
- 基于 **学科知识点图谱**（`data/subjects.json`）与 **ChromaDB 向量库** 增强上下文
- 四维评分：学科匹配（40 分）、经验匹配（30 分）、地理与时间（15 分）、性价比（15 分）
- 输出结构化 JSON，含每位候选家教的推荐理由

---

## 目录结构

```
hf_space/
├── app.py                     # Gradio 入口，定义 Web 界面 + HTTP API
├── requirements.txt           # Python 依赖
├── README.md                  # 本文件
└── ai_module/                 # AI 匹配核心模块
    ├── __init__.py
    ├── config.yaml            # LLM / Embedding / RAG 配置
    ├── agent.py               # MatchAgent — 匹配决策 Agent（编排流程）
    ├── llm_client.py          # LLM 统一调用接口（DeepSeek）
    ├── embedding.py           # 本地向量编码（bge-small-zh-v1.5）
    ├── rag.py                 # ChromaDB 检索 + 知识库管理
    └── data/
        ├── subjects.json      # 学科知识点图谱（数/语/英/物/化）
        └── prompts/
            └── match_scoring.txt  # LLM 匹配打分 Prompt 模板
```

---

## 匹配流程

```
家长需求 + 候选家教
        │
        ▼
① RAG 检索 (ChromaDB)
   需求向量化 → 检索相关知识点，增强上下文
        │
        ▼
② 学科知识点注入
   从 subjects.json 读取对应学段知识点
        │
        ▼
③ 构造 Prompt → LLM 打分 (DeepSeek)
   输出 JSON 数组 [{tutor_id, total_score, ...}]
        │
        ▼
④ 取 Top-N 返回
   默认返回前 5 名（matching.top_n）
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 DeepSeek API Key

`ai_module/config.yaml` 中的 `llm.api_key` 为 `${DEEPSEEK_API_KEY}`，运行时从环境变量读取：

```bash
export DEEPSEEK_API_KEY=sk-xxx
```

### 3. 本地运行

```bash
python app.py
```

默认启动 Gradio 服务，访问浏览器打开 Web 界面，或通过 `/api/predict` 端点以 JSON 方式调用。

---

## 配置说明（`ai_module/config.yaml`）

| 配置路径 | 默认值 | 说明 |
|---|---|---|
| `llm.provider` | `deepseek` | LLM 提供商（openai / deepseek / qwen） |
| `llm.model` | `deepseek-v4-flash` | 模型名称 |
| `llm.base_url` | `https://api.deepseek.com` | API 端点地址 |
| `llm.temperature` | `0.3` | 生成温度 |
| `llm.max_tokens` | `2000` | 单次最大输出 token 数 |
| `embedding.model` | `BAAI/bge-small-zh-v1.5` | 本地 Embedding 模型，首次运行自动下载 |
| `embedding.device` | `cpu` | 推理设备（cpu / cuda） |
| `rag.collection_name` | `tutor_knowledge` | ChromaDB 集合名 |
| `rag.persist_dir` | `./ai_module/chroma_db` | 向量库持久化目录 |
| `rag.top_k` | `10` | RAG 检索返回文档数 |
| `matching.max_candidates` | `50` | 候选池上限 |
| `matching.top_n` | `5` | 最终返回的推荐家教数 |

---

## 接口说明

`app.py` 中的 `match_demand` 接收以下输入：

| 输入字段 | 类型 | 说明 |
|---|---|---|
| `subject` | string | 需求学科 |
| `grade` | string | 年级 |
| `location` | string | 所在地区 |
| `budget` | number | 预算（元/小时） |
| `description` | string | 需求描述 |
| `requirements` | string | 额外要求 |
| `candidates_json` | string | 候选家教列表（JSON 数组） |

**候选家教 JSON 字段**：`id`、`real_name`、`school`、`major`、`education`、`grade`、`skills`、`teaching_exp`、`location`、`available_time`、`hourly_rate`、`introduction`。

**输出**：JSON 数组，按总分降序，每项含：

```json
{
  "tutor_id": 整数,
  "total_score": 整数,
  "subject_match": 整数,
  "experience_match": 整数,
  "location_time_match": 整数,
  "value_match": 整数,
  "reason": "推荐理由"
}
```

---

## 部署到 HuggingFace Spaces

1. 将 `hf_space/` 目录内容上传为一个新的 Space（SDK 选择 **Gradio**）
2. 在 Space 的 Settings → Secrets 中添加 `DEEPSEEK_API_KEY`
3. Space 会自动读取 `requirements.txt` 安装依赖并启动 `app.py`

部署完成后，将 Space 的 API 地址（形如 `https://your-space.hf.space/api/predict`）填入主项目后端的 `HF_MATCH_API_URL` 环境变量，即可启用远程 AI 匹配。

---

## 相关链接

- 主项目：趣学喵（QuXueMiao）家教供需匹配平台
- 主项目 README：`../README.md`
- 后端 AI 匹配模块（本地直调版）：`../ai_module/`
