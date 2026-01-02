# 平台测试指南

## 快速开始测试

我已经为您创建了测试脚本和文档。以下是测试步骤：

## 📋 测试前准备

### 1. 检查环境

```bash
# 检查Python版本（需要3.11+）
python --version

# 检查Node.js版本（需要18+）
node --version
npm --version
```

### 2. 安装依赖

**后端:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**前端:**
```bash
cd frontend
npm install
```

### 3. 配置环境变量

创建 `backend/.env` 文件（至少需要以下配置）:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/interview_quote
REDIS_URL=redis://localhost:6379/0
LLM_API_KEY=your_api_key_here
SECRET_KEY=your-secret-key
STORAGE_PATH=./storage
UPLOAD_PATH=./storage/uploads
DOCUMENT_PATH=./storage/documents
CORS_ORIGINS=http://localhost:5173
```

## 🧪 测试方法

### 方法1: 基础代码测试（推荐先运行）

这个测试不需要启动服务，只测试代码结构：

```bash
python test_basic.py
```

**预期输出:**
- ✓ 所有模块导入成功
- ✓ 配置加载正常
- ✓ 数据模型定义正确
- ✓ 服务类初始化成功

### 方法2: 完整API测试

需要先启动服务，然后运行：

```bash
python test_platform.py
```

### 方法3: 手动前端测试

1. **启动服务**（需要3个终端）:

   **终端1 - 后端API:**
   ```bash
   cd backend
   python run.py
   ```
   应该看到: `Uvicorn running on http://0.0.0.0:8000`

   **终端2 - Celery Worker:**
   ```bash
   cd backend
   celery -A app.celery_app worker --loglevel=info
   ```
   应该看到: `celery@... ready`

   **终端3 - 前端:**
   ```bash
   cd frontend
   npm run dev
   ```
   应该看到: `Local: http://localhost:5173/`

2. **访问前端界面:**
   - 打开浏览器: http://localhost:5173/simple
   - 或完整功能: http://localhost:5173

3. **测试流程:**
   - 填写案件名称
   - 上传逐字稿文件（.txt格式）
   - （可选）上传图片
   - 点击"开始处理并生成文件"
   - 等待处理完成
   - 下载生成的文件

## 📝 测试检查清单

### 基础检查
- [ ] Python环境正常
- [ ] Node.js环境正常
- [ ] 后端依赖安装完成
- [ ] 前端依赖安装完成

### 配置检查
- [ ] `.env` 文件已创建
- [ ] 数据库URL配置正确
- [ ] Redis URL配置正确
- [ ] 存储路径配置正确

### 服务检查
- [ ] PostgreSQL数据库运行中
- [ ] Redis服务运行中
- [ ] 后端API可以访问 (http://localhost:8000/health)
- [ ] 前端可以访问 (http://localhost:5173)

### 功能检查
- [ ] 可以创建案件
- [ ] 可以上传文件
- [ ] 可以启动提取（需要LLM API Key）
- [ ] 可以生成方案
- [ ] 可以生成文档
- [ ] 可以下载文档

## 🔍 故障排除

### 问题1: 后端无法启动

**检查:**
- 端口8000是否被占用
- 数据库连接是否正常
- `.env` 文件是否存在

**解决:**
```bash
# 检查端口
netstat -ano | findstr :8000

# 检查数据库连接
psql -h localhost -U user -d interview_quote
```

### 问题2: Celery Worker无法启动

**检查:**
- Redis是否运行
- REDIS_URL配置是否正确

**解决:**
```bash
# 检查Redis
redis-cli ping
# 应该返回: PONG
```

### 问题3: 前端无法连接后端

**检查:**
- 后端是否运行
- CORS配置是否正确
- vite.config.ts中的proxy配置

**解决:**
- 检查后端日志
- 检查浏览器控制台错误
- 确认后端URL: http://localhost:8000

### 问题4: 文件上传失败

**检查:**
- storage目录是否存在
- 目录权限是否正确

**解决:**
```bash
# 创建目录
mkdir -p storage/uploads storage/documents
```

### 问题5: 需求提取失败

**检查:**
- LLM_API_KEY是否正确
- Celery Worker是否运行
- 查看Celery Worker日志

## 📊 测试结果示例

### 成功情况

```
==================================================
开始基础测试
==================================================
✓ config模块导入成功
✓ database模块导入成功
✓ models模块导入成功
✓ services模块导入成功
✓ API路由导入成功

总计: 5/5 测试通过
✓ 所有基础测试通过！代码结构正常。
```

### 失败情况

如果看到错误，请：
1. 检查错误信息
2. 确认依赖已安装
3. 检查Python路径配置
4. 查看详细错误堆栈

## 🎯 下一步

测试通过后，您可以：
1. 配置真实的LLM API Key进行完整测试
2. 上传真实的逐字稿文件测试
3. 检查生成的文档质量
4. 根据需要进行功能调整

## 📞 需要帮助？

如果遇到问题：
1. 查看错误日志
2. 检查配置文件
3. 确认服务状态
4. 参考 `SETUP.md` 和 `README.md`

