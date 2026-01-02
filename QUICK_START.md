# 快速启动指南

## ✅ 已完成的配置

我已经为您：
1. ✅ 创建了配置文件（backend/.env）
2. ✅ 配置了SQLite数据库（无需PostgreSQL）
3. ✅ 创建了存储目录
4. ✅ 启动了后端服务（端口8000）
5. ✅ 启动了前端服务（端口5173）

## 🌐 访问地址

**前端界面（简体上传）**: http://localhost:5173/simple

**完整功能界面**: http://localhost:5173

**后端API**: http://localhost:8000

**API文档**: http://localhost:8000/docs

## 📝 使用步骤

1. 打开浏览器访问: **http://localhost:5173/simple**

2. 填写信息：
   - 案件名称（例如：测试案件）
   - 上传会议逐字稿（.txt文件）
   - （可选）上传工厂机器照片

3. 点击"开始处理并生成文件"

4. 等待处理完成

5. 在下方下载生成的文件

## ⚠️ 注意事项

### 如果服务未启动

**手动启动后端**（新PowerShell窗口）:
```powershell
cd backend
python run.py
```

**手动启动前端**（新PowerShell窗口）:
```powershell
cd frontend
npm install  # 如果还没安装
npm run dev
```

### 数据库

- 当前使用SQLite，数据文件在 `backend/test.db`
- 无需安装PostgreSQL

### LLM功能

- 需求提取功能需要配置真实的LLM API Key
- 在 `backend/.env` 中设置 `LLM_API_KEY=your_real_key`
- 如果没有API Key，可以测试其他功能（上传、查看界面等）

### Redis（可选）

- Celery任务需要Redis
- 如果没有Redis，基本功能仍可使用
- 需求提取和文档生成可能需要等待或使用同步模式

## 🔧 故障排除

### 端口被占用

如果8000或5173端口被占用：
- 后端：修改 `backend/run.py` 中的端口
- 前端：修改 `frontend/vite.config.ts` 中的端口

### 前端无法连接后端

检查：
1. 后端是否运行在8000端口
2. 浏览器控制台是否有错误
3. CORS配置是否正确

### 文件上传失败

检查：
1. `backend/storage` 目录是否存在
2. 目录权限是否正确

## 📞 需要帮助？

查看详细文档：
- `TESTING_GUIDE.md` - 详细测试指南
- `SETUP.md` - 完整设置说明
- `README.md` - 项目说明

