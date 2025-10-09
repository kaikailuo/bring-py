# 高中信息技术教学平台 - 后端API

## 项目简介

这是一个基于FastAPI的高中信息技术教学平台后端API系统，提供学生、教师和管理员的认证功能。

## 技术栈

- **框架**: FastAPI
- **数据库**: SQLite (开发环境)
- **ORM**: SQLAlchemy
- **认证**: JWT (JSON Web Tokens)
- **密码加密**: Bcrypt
- **数据验证**: Pydantic
- **测试**: pytest

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 应用程序入口
│   ├── api/                    # API路由
│   │   ├── __init__.py
│   │   └── auth/               # 认证相关API
│   │       ├── __init__.py
│   │       └── routes.py       # 认证路由
│   ├── models/                 # 数据模型
│   │   └── user.py            # 用户模型
│   ├── schemas/               # 数据验证模式
│   │   └── user.py            # 用户模式
│   ├── services/              # 业务逻辑
│   │   └── auth.py            # 认证服务
│   └── utils/                 # 工具函数
│       ├── database.py        # 数据库配置
│       └── security.py        # 安全工具
├── tests/                     # 测试文件
│   ├── __init__.py
│   └── test_auth.py          # 认证测试
├── requirements.txt          # 依赖包
├── init_db.py               # 数据库初始化脚本
├── env.example              # 环境变量示例
└── README.md                # 项目说明
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

### 3. 初始化数据库

```bash
python init_db.py
```

### 4. 启动服务

```bash
# 开发模式
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者直接运行
python app/main.py
```

### 5. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API接口

### 认证接口

#### 用户注册
- **POST** `/api/auth/register`
- **请求体**:
  ```json
  {
    "username": "string",
    "password": "string",
    "role": "student|teacher",
    "name": "string",
    "email": "string"
  }
  ```

#### 用户登录
- **POST** `/api/auth/login`
- **请求体**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

#### 用户登出
- **POST** `/api/auth/logout`
- **请求头**: `Authorization: Bearer <token>`

#### 获取当前用户信息
- **GET** `/api/auth/me`
- **请求头**: `Authorization: Bearer <token>`

#### 更新用户信息
- **PUT** `/api/auth/me`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:
  ```json
  {
    "name": "string",
    "email": "string"
  }
  ```

#### 修改密码
- **POST** `/api/auth/change-password`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:
  ```json
  {
    "old_password": "string",
    "new_password": "string"
  }
  ```

### 管理员接口

#### 获取用户列表
- **GET** `/api/auth/users`
- **请求头**: `Authorization: Bearer <admin_token>`
- **查询参数**: `skip`, `limit`, `role`

#### 激活用户
- **PUT** `/api/auth/users/{user_id}/activate`
- **请求头**: `Authorization: Bearer <admin_token>`

#### 停用用户
- **PUT** `/api/auth/users/{user_id}/deactivate`
- **请求头**: `Authorization: Bearer <admin_token>`

## 响应格式

所有API响应都遵循统一格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 默认账户

系统初始化时会创建默认管理员账户：
- **用户名**: admin
- **密码**: admin123
- **角色**: admin

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 运行测试并显示覆盖率
pytest --cov=app
```

## 开发说明

### 数据验证规则

- **用户名**: 3-20个字符，只能包含字母、数字、下划线和连字符
- **密码**: 6-20个字符
- **姓名**: 2-10个字符
- **邮箱**: 有效的邮箱格式

### 用户角色

- **student**: 学生
- **teacher**: 教师
- **admin**: 管理员

### JWT令牌

- **算法**: HS256
- **过期时间**: 30分钟
- **包含信息**: 用户名、用户ID、角色

## 部署说明

### 生产环境配置

1. 修改 `SECRET_KEY` 为安全的随机字符串
2. 使用PostgreSQL或MySQL替代SQLite
3. 配置HTTPS
4. 设置适当的CORS策略
5. 使用环境变量管理配置

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
