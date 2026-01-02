# 快速测试指南

## 前置条件检查

### 1. 检查Python环境
```bash
python --version  # 需要 Python 3.11+
```

### 2. 检查Node.js环境
```bash
node --version  # 需要 Node.js 18+
npm --version
```

### 3. 检查PostgreSQL
```bash
psql --version
# 或使用Docker
docker ps | grep postgres
```

### 4. 检查Redis
```bash
redis-cli ping
# 或使用Docker
docker ps | grep redis
```

## 快速测试步骤

### 步骤1: 安装依赖

**后端:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**前端:**
```bash
cd frontend
npm install
```

### 步骤2: 配置环境变量

创建 `backend/.env` 文件（参考 `backend/.env.test`）：
```env
DATABASE_URL=postgresql://user:password@localhost:5432/interview_quote
REDIS_URL=redis://localhost:6379/0
LLM_API_KEY=your_api_key_here
# ... 其他配置
```

### 步骤3: 初始化数据库

```bash
cd backend
alembic upgrade head
```

### 步骤4: 启动服务

**终端1 - 后端API:**
```bash
cd backend
python run.py
```

**终端2 - Celery Worker:**
```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

**终端3 - 前端:**
```bash
cd frontend
npm run dev
```

### 步骤5: 运行测试脚本

```bash
python test_platform.py
```

### 步骤6: 手动测试前端

1. 打开浏览器: http://localhost:5173/simple
2. 填写案件名称
3. 上传测试逐字稿文件
4. 点击"开始处理并生成文件"
5. 等待处理完成
6. 下载生成的文件

## 测试检查清单

- [ ] 后端API健康检查通过
- [ ] 可以创建案件
- [ ] 可以上传文件
- [ ] 可以列出上传的文件
- [ ] 可以启动需求提取（需要LLM API Key）
- [ ] 提取完成后可以获取需求
- [ ] 可以生成报价方案
- [ ] 可以生成文档
- [ ] 前端界面可以访问
- [ ] 前端可以上传文件
- [ ] 前端可以下载文档

## 常见问题

### 问题1: 后端无法启动
- 检查端口8000是否被占用
- 检查数据库连接配置
- 检查Python依赖是否安装完整

### 问题2: Celery Worker无法启动
- 检查Redis是否运行
- 检查REDIS_URL配置

### 问题3: 前端无法连接后端
- 检查后端是否运行在8000端口
- 检查CORS配置
- 检查vite.config.ts中的proxy配置

### 问题4: 文件上传失败
- 检查storage目录权限
- 检查UPLOAD_PATH配置

### 问题5: 需求提取失败
- 检查LLM_API_KEY是否正确
- 检查LLM_BASE_URL配置
- 查看Celery Worker日志

## 测试数据

创建测试逐字稿文件 `test_transcript.txt`:
```
这是测试逐字稿内容
客户提到需要自动化生产线
工件重量范围：10-50kg
需要翻转工序
机器数量：2台
```

