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
# AI Agent Instructions — 高中信息技术教学平台（精简版）

此文件面向 AI 开发/自动化代理，帮助快速在本仓库中安全、可审查地做出改动。

**架构概览**
- **前端**：`frontend/`（Vue3 + Vite）。路由按角色分组（`/student/*`, `/teacher/*`）；状态通过 Pinia（`frontend/src/stores/user.js`）；统一 API 封装在 `frontend/src/utils/api.js`。
- **后端**：`backend/`（FastAPI）。主要目录：`app/api/`（路由）、`app/services/`（业务）、`app/models/`（SQLAlchemy）、`app/schemas/`（Pydantic）、`app/utils/`（工具）。JWT 认证在 `app/services/auth.py`。
- **数据/问题集**：静态问题与内容位于 `data/problems/`（索引在 `data/problems/index.json`），后端 service 通过该目录加载题目。

**快速上手（Windows cmd 示例）**
- 启动后端（推荐）：
```
python scripts\start_backend.py
```
- 或直接运行后端入口：
```
python backend\start_server.py
```
- 启动前端（或使用仓库脚本）：
```
cd frontend
npm ci
npm run dev
```
- 一键启动（仓库脚本）：
```
python scripts\start_both.py
```

**测试与验证**
- 后端单测：`cd backend && pytest -q`。
- 变更后建议：后端改动 -> 更新/新增 Pydantic schema；前端改动 -> 确保 `frontend/src/utils/api.js` 的接口调用一致。

**关键文件（速查）**
- 后端路由：`backend/app/api/`（如 `auth/routes.py`, `problems/routes.py`）
- 认证与安全：`backend/app/services/auth.py`（JWT）
- 模型/模式：`backend/app/models/`, `backend/app/schemas/`
- 问题数据源：`data/problems/`, `data/change_data.py`
- 前端 API + 状态：`frontend/src/utils/api.js`, `frontend/src/stores/user.js`
- 默认账号：`docs/default_accounts.md`，本地 DB：`backend/app.db`

**项目约定与限制（AI 代理须遵守）**
- **不要**修改或提交任何包含凭证的文件（`.env`、私钥等）。
- **不要**在无人审批下安装外部二进制或自动从网络拉取可执行文件；如需新增依赖，先在变更说明中声明并请求人工确认，并在 `requirements.txt` 或 `frontend/package.json` 中列出。 
- 小幅改动（单文件、非安全相关）可直接生成 patch；重大改动（数据库迁移、API contract 变化、CI、引入运行沙箱）需要先生成“决策摘要”供人工复核。

**变更报告模板（每次自动化补丁必须包含）**
- `文件`：列出修改的文件路径
- `变更摘要`：一句话说明核心改动
- `测试命令`：最小复现/验证命令（例如 `cd backend && pytest -q`）
- `风险/注意`：可能影响点与回滚建议

如需我合并或进一步扩展某部分（例如添加 CI 步骤、对接评测沙箱建议），请指出优先项与接受的风险范围。