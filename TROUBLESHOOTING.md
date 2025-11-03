# 🔧 故障排除指南

## 常见问题及解决方案

### 1. "fail to fetch" 错误

**问题描述**：前端无法连接到后端API，显示"fail to fetch"错误。

**可能原因**：
- 前端和后端端口配置不匹配
- 后端服务未正常启动
- CORS配置问题
- 网络连接问题

**解决步骤**：

#### 步骤1：检查服务状态
```bash
# 运行诊断脚本
python scripts/check_services.py
```

#### 步骤2：确认端口配置
- 前端端口：5173
- 后端端口：8000
- 确保两个服务都在运行

#### 步骤3：手动检查服务
```bash
# 检查后端
curl http://localhost:8000/health
# 或访问 http://localhost:8000/docs

# 检查前端
# 访问 http://localhost:5173
```

#### 步骤4：查看浏览器控制台
1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签页的错误信息
3. 查看 Network 标签页的请求状态

### 2. 端口被占用

**解决方案**：
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# 杀死占用端口的进程
taskkill /PID <进程ID> /F

# macOS/Linux
lsof -i :8000
lsof -i :5173
kill -9 <进程ID>
```

### 3. 依赖安装问题

**后端依赖**：
```bash
cd backend
pip install -r requirements.txt
```

**前端依赖**：
```bash
cd frontend
npm install
```

### 4. 数据库问题

**重新初始化数据库**：
```bash
# 删除现有数据库文件
rm backend/app.db  # Linux/macOS
del backend\app.db  # Windows

# 重新启动后端，会自动创建新数据库
python scripts/start_backend.py
```

### 5. CORS错误

**检查CORS配置**：
- 后端已配置允许 `http://localhost:5173` 和 `http://localhost:3000`
- 如果仍有问题，检查浏览器是否缓存了旧配置

## 🚀 快速修复

### 一键重启
```bash
# 停止所有服务（Ctrl+C）
# 然后重新启动
python scripts/start_both.py
```

### 分步启动
```bash
# 1. 启动后端
python scripts/start_backend.py

# 2. 等待几秒后启动前端
python scripts/start_frontend.py
```

## 📞 获取帮助

如果问题仍然存在，请提供以下信息：
1. 操作系统版本
2. Python版本：`python --version`
3. Node.js版本：`node --version`
4. 错误截图或控制台输出
5. 诊断脚本的输出结果

## 🔍 调试技巧

### 后端调试
```bash
# 查看后端日志
cd backend
python start_server.py
# 观察控制台输出
```

### 前端调试
```bash
# 查看前端日志
cd frontend
npm run dev
# 观察控制台输出
```

### 网络调试
1. 打开浏览器开发者工具
2. 切换到 Network 标签
3. 刷新页面
4. 查看失败的请求详情

