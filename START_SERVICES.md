# 启动服务指南

## 快速启动

我已经为您创建了配置文件并启动了服务。请按照以下步骤操作：

## 已完成的配置

✅ 创建了 `backend/.env` 配置文件
✅ 创建了存储目录
✅ 配置了SQLite数据库（无需PostgreSQL）
✅ 启动了后端服务（端口8000）
✅ 启动了前端服务（端口5173）

## 访问地址

- **前端界面**: http://localhost:5173/simple
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 如果服务未启动

### 手动启动后端

打开新的PowerShell终端：

```powershell
cd backend
python run.py
```

### 手动启动前端

打开另一个PowerShell终端：

```powershell
cd frontend
npm install  # 如果还没安装依赖
npm run dev
```

## 注意事项

1. **数据库**: 当前使用SQLite，数据文件在 `backend/test.db`
2. **Redis**: 如果未安装Redis，Celery任务可能无法运行，但基本功能可用
3. **LLM API**: 需要配置真实的API Key才能使用需求提取功能

## 测试功能

1. 打开浏览器访问: http://localhost:5173/simple
2. 填写案件名称
3. 上传逐字稿文件
4. 点击"开始处理并生成文件"

## 停止服务

按 `Ctrl+C` 停止服务

