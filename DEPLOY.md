# 趣学喵部署指南

## 1. Render 后端部署

1. Fork 或 clone 本项目到你的 GitHub
2. 在 [Render](https://render.com) 创建新账号
3. New Web Service → 连接 GitHub 仓库
4. Render 会自动检测 `render.yaml` 并配置
5. 手动设置以下环境变量：
   - `DEEPSEEK_API_KEY` — DeepSeek API Key
   - `HF_MATCH_API_URL` — HuggingFace Spaces 地址（部署完第3步后填入）
6. 等待部署完成（约5-10分钟）
7. 获取后端地址：`https://quxuemiao-api.onrender.com`

## 2. Vercel 前端部署

1. 安装 Vercel CLI：`npm i -g vercel`
2. 在项目根目录运行：`vercel --prod`
3. 设置环境变量：`VITE_API_BASE_URL` = 后端地址
4. 获取前端地址：`https://quxuemiao.vercel.app`

## 3. HuggingFace Spaces AI 服务

1. 在 [HuggingFace](https://huggingface.co) 创建 Space，选 Gradio SDK
2. 上传 `hf_space/` 目录内容
3. 在 Space Settings → Secrets 设置 `DEEPSEEK_API_KEY`
4. 获取 API 地址：`https://your-space.hf.space/api/predict`
5. 将此地址填入 Render 的 `HF_MATCH_API_URL` 环境变量

## 4. 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
set MYSQL_USER=root
set MYSQL_PASSWORD=admin
python app.py

# 前端
cd frontend
npm install
npm run dev
```
