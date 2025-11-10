# AI Agent Instructions for 高中信息技术教学平台

本文档旨在帮助 AI 代理快速理解并参与项目开发。以下是关键开发指南。

## 🏗️ 项目架构

### 前端 (`/frontend`)
- Vue3 + Vite 构建的 SPA 应用
- 路由结构按用户角色分离：`/student/*`, `/teacher/*`
- 使用 Pinia 状态管理 (`stores/user.js`)
- API 请求封装在 `utils/api.js`

示例：新增功能时的路由和视图集成
```js
// 在 router/index.js 中添加路由
{
  path: '/student/practice',
  component: () => import('../views/student/Practice.vue')
}
```

### 后端 (`/backend`)
- FastAPI 应用，采用模块化组织
- 标准目录结构：
  - `app/api/` - 路由和控制器
  - `app/models/` - SQLAlchemy 数据模型
  - `app/schemas/` - Pydantic 模型
  - `app/services/` - 业务逻辑层
  - `app/utils/` - 通用工具
- 认证基于 JWT，实现在 `app/services/auth.py`

## 🔑 关键开发流程

### 本地开发环境
1. 后端启动：使用 `scripts/start_backend.py`
2. 前端启动：使用 `scripts/start_frontend.py`
3. 同时启动：使用 `scripts/start_both.py`

### 测试
- 后端单元测试位于 `backend/tests/`
- 使用 pytest 运行测试：在 backend 目录下执行 `pytest`
- 关键测试示例见 `backend/tests/test_auth.py`

### 数据库
- SQLite 数据库文件：`backend/app.db`
- 默认账号信息见 `docs/default_accounts.md`

## 📋 开发规范

### API 设计
- RESTful 端点统一放在 `app/api/` 下对应模块中
- 每个端点必须使用 Pydantic 模型定义请求/响应结构
- API 文档位于 `docs/api/backend_api.md`

示例：添加新的 API 端点
```python
from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate, current_user = Depends(get_current_user)):
    # 实现用户创建逻辑
```

### 前端组件
- 按角色（student/teacher）组织视图组件
- 共用组件放在 components/ 目录
- 使用 SCSS 变量（`styles/variables.scss`）维护主题

### 状态管理
- 用户状态统一通过 Pinia store 管理
- API 调用使用统一的 axios 实例（`utils/api.js`）

## 🤝 协作指南

### 分支管理
- 功能分支命名：`feature-{feature-name}`
- 修复分支命名：`fix-{issue-number}`

### 代码审查重点
- API 端点是否有完整的请求/响应模型定义
- 前端组件是否遵循既有的目录结构
- 状态管理是否通过 Pinia store 实现
- 是否包含相应的测试用例