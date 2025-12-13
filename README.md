# 高中信息技术教学平台

一个专为高中生设计的Python编程学习平台，集成AI智能辅导、实时代码评测、学情分析等功能。前后端分离，支持多角色（学生/教师），提供完整的编程教学体验。

## 🌟 项目特色

### 核心功能模块

#### 1. 编程练习中心 ✅
- **题目管理**：按课程分类的练习题（支持多课程动态加载）
- **代码编辑器**：集成 Monaco Editor，支持语法高亮、代码补全
- **实时运行**：Python 代码在线执行，即时反馈结果
- **自动测评**：多组测试用例验证，通过率统计
- **学习进度追踪**：记录题目完成状态，展示通过情况

#### 2. AI编程助手系统 ✅
- **智能代码反馈**：提交代码后，AI 自动生成改进建议
- **问题解答**：学生可提问，AI 提供友好的调试指导
- **对话记录**：保留每次交互的上下文
- **教师级学情分析**：AI 生成面向教师的学生学习分析报告（含改进建议与可执行方案）

#### 3. 互动交流平台 ✅
- **问答论坛**：学生发帖、评论、点赞、收藏
- **问题监控**：教师实时查看学生的提问与讨论
- **代码分享**：展示优秀解答、经验分享
- **学生活动**：记录学生的学习行为，展示最近活动

#### 4. 教学资源管理 ✅
- **资源中心**：支持上传和浏览教学资源
- **分类组织**：按课程对资源分类
- **权限控制**：仅授权学生可见

#### 5. 学情分析仪表盘 ✅
- **学生自查**：学生查看自己的学习统计、课程进度
- **班级分析**：教师查看班级整体表现、学生排名
- **数据可视化**：通过图表展示学习趋势

### 用户角色支持

#### 学生端特色功能 ✅
- **Dashboard**：学习概览、课程进度、活动时间线
- **编程练习**：题目列表、代码编辑、运行测评、AI 助手
- **资源浏览**：查看和学习教学资源
- **论坛互动**：发帖、回帖、阅读讨论
- **个人资料**：学习统计、成就展示

#### 教师端特色功能 ✅
- **教学仪表盘**：快速统计（学生数、班级数、资源数、待答疑数量）
- **班级管理**：学生列表、班级分组、学生成绩追踪
- **问题监控**：实时查看学生提问、快速回答
- **资源管理**：上传、审核、分类教学资源
- **学情分析**：班级学习数据分析、AI 生成学生评估报告
- **作业布置**：（开发中）创建和管理作业
- **快捷操作**：一键跳转至常用功能，今日待办列表

## 🚀 技术栈

### 前端
- **框架**：Vue 3（Composition API）+ Vite
- **UI组件库**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **样式**：Sass/SCSS（教育主题设计系统）
- **代码编辑器**：Monaco Editor
- **图标库**：Element Plus Icons
- **Markdown 渲染**：markdown-it（用于题目描述渲染）

### 后端
- **框架**：FastAPI（异步 Python Web 框架）
- **数据库**：SQLite（本地开发）/ PostgreSQL（生产推荐）
- **ORM**：SQLAlchemy
- **数据验证**：Pydantic
- **认证**：JWT（JSON Web Tokens）
- **AI 集成**：OpenAI API（或兼容 LLM）
- **文件存储**：本地上传目录（`/backend/uploads`）
- **CORS**：FastAPI CORS Middleware

## 📁 项目结构

```
bring-py/
├── backend/                              # 🐍 后端服务（FastAPI）
│   ├── app/
│   │   ├── main.py                       # FastAPI 应用入口
│   │   ├── api/                          # 路由定义
│   │   │   ├── auth/                     # 认证路由（注册、登录、JWT）
│   │   │   ├── problems/                 # 题目路由（题目列表、运行代码、提交答案）
│   │   │   ├── resources/                # 资源管理路由
│   │   │   ├── post.py                   # 论坛帖子路由
│   │   │   ├── comment.py                # 评论路由
│   │   │   ├── favorite.py               # 收藏路由
│   │   │   ├── analytics.py              # 学情分析路由
│   │   │   └── ai/                       # AI 助手路由（问答、代码反馈、学情分析）
│   │   ├── models/                       # 数据库模型（SQLAlchemy）
│   │   │   ├── user.py                   # 用户、学生、教师模型
│   │   │   ├── post.py                   # 帖子、评论模型
│   │   │   ├── student_result.py         # 学生答题记录
│   │   │   ├── student_tests.py          # 学生测试结果
│   │   │   ├── resource.py               # 教学资源模型
│   │   │   ├── comment.py                # 评论模型
│   │   │   └── favorite.py               # 收藏模型
│   │   ├── schemas/                      # 请求/响应数据模型（Pydantic）
│   │   ├── services/                     # 业务逻辑
│   │   │   ├── auth.py                   # 认证、JWT、密码哈希
│   │   │   ├── problems_service.py       # 题目加载、代码运行、测评逻辑
│   │   │   ├── resource_service.py       # 资源管理
│   │   │   └── ai/                       # AI 服务
│   │   │       ├── client.py             # LLM API 调用（OpenAI 或兼容）
│   │   │       ├── prompts.py            # Prompt 管理（代码反馈、学情分析等）
│   │   │       └── tasks/                # AI 任务（异步任务处理）
│   │   └── utils/                        # 工具函数
│   │       ├── database.py               # 数据库连接、会话管理
│   │       └── security.py               # JWT、密码相关工具
│   ├── data/                             # 题目数据源
│   │   └── problems/
│   │       ├── index.json                # 题目索引（课程、题目元数据）
│   │       ├── courses.json              # 课程配置
│   │       ├── lesson_01/, lesson_02/... # 按课程分类的题目目录
│   │       │   └── problem_01/
│   │       │       ├── README.md         # 题目描述（Markdown）
│   │       │       ├── solution.py       # 参考解答
│   │       │       ├── tests.json        # 测试用例
│   │       │       └── assets/           # 题目附属资源（图片等）
│   ├── migrations/                       # 数据库迁移脚本
│   ├── tests/                            # 后端单元测试
│   ├── uploads/                          # 用户上传的文件目录
│   ├── requirements.txt                  # Python 依赖
│   ├── app.db                            # SQLite 数据库文件（本地开发）
│   └── start_server.py                   # 后端启动脚本
│
├── frontend/                             # 💻 前端（Vue 3 + Vite）
│   ├── index.html                        # HTML 入口
│   ├── vite.config.js                    # Vite 配置
│   ├── package.json                      # 前端依赖
│   ├── public/                           # 静态资源
│   └── src/
│       ├── App.vue                       # 根组件
│       ├── main.js                       # 前端启动入口
│       ├── router/
│       │   └── index.js                  # 路由配置（学生/教师/公共路由）
│       ├── stores/
│       │   └── user.js                   # Pinia 用户状态（登录、权限）
│       ├── utils/
│       │   ├── api.js                    # API 请求封装（通用接口调用）
│       │   └── markdown.js               # Markdown 渲染工具
│       ├── styles/
│       │   ├── variables.scss            # 主题颜色、间距变量
│       │   ├── index.scss                # 全局样式
│       │   └── markdown.scss             # Markdown 样式
│       ├── components/                   # 通用组件
│       │   ├── MonacoEditor.vue          # 代码编辑器包装
│       │   ├── PracticeAiChat.vue        # 练习页 AI 助手聊天
│       │   └── ...
│       └── views/
│           ├── Home.vue                  # 首页
│           ├── Login.vue                 # 登录页
│           ├── Profile.vue               # 个人资料
│           ├── AboutUs.vue, Contact.vue  # 关于、联系
│           ├── student/                  # 学生端
│           │   ├── Layout.vue            # 学生主布局
│           │   ├── Dashboard.vue         # 学生仪表盘
│           │   ├── Practice.vue          # 编程练习（题目选择、代码编辑、运行）
│           │   ├── CourseDetail.vue      # 课程详情
│           │   ├── Resources.vue         # 教学资源浏览
│           │   └── Forum.vue             # 论坛讨论
│           └── teacher/                  # 教师端
│               ├── Layout.vue            # 教师主布局（快捷操作、待办任务）
│               ├── Dashboard.vue         # 教师仪表盘
│               ├── ClassManagement.vue   # 班级管理
│               ├── ResourceManagement.vue# 资源管理
│               ├── Analytics.vue         # 学情分析
│               ├── QuestionMonitor.vue   # 问题监控
│               ├── AssignmentManager.vue # 作业管理
│               └── CreateAssignmentWizard.vue # 作业创建向导
│
├── docs/                                 # 📄 文档
│   ├── api/
│   │   └── backend_api.md                # 后端 API 文档
│   ├── default_accounts.md               # 默认账号说明
│   └── README/
│       └── backend_README.md             # 后端详细说明
│
├── scripts/                              # 🧰 启动脚本
│   ├── start_backend.py                  # 启动后端
│   ├── start_frontend.py                 # 启动前端
│   └── start_both.py                     # 同时启动前后端
│
├── .github/                              # CI/CD 配置
│   ├── copilot-instructions.md           # AI 开发指南
│   └── workflows/                        # GitHub Actions
│
├── README.md                             # 项目说明（本文件）
├── .gitignore                            # Git 忽略规则
└── git_work.md                           # Git 工作日志/开发记录
```

## 📚 API 文档

详细的 API 接口说明见 `docs/api/backend_api.md`。

主要模块：
- **认证 API**（`/api/auth/`）：注册、登录、刷新 token
- **题目 API**（`/api/problems/`）：获取题目、运行代码、提交答案、获取进度
- **资源 API**（`/api/resources/`）：上传、浏览、删除资源
- **论坛 API**（`/api/posts/`, `/api/comments/`）：发帖、评论、点赞
- **AI API**（`/api/ai/`）：代码反馈、问答、学情分析
- **分析 API**（`/api/analytics/`）：学生统计、班级数据

### 使用 Swagger 文档

启动后端后，访问：http://localhost:8000/docs

## 🔐 安全与认证

- 使用 JWT（JSON Web Tokens）进行用户认证
- 密码使用 bcrypt 加密存储
- 敏感接口需要有效 token
- CORS 配置限制跨域请求

## 🌐 部署与运行

### 本地开发

```bash
# 启动后端和前端
python scripts/start_both.py
```

### Docker 部署（可选）

```bash
# 使用 docker-compose 启动
docker-compose -f infra/docker-compose.yml up
```

### 生产构建

**前端：**
```bash
cd frontend
npm install
npm run build  # 构建到 dist/ 目录
```

**后端：**
```bash
cd backend
pip install -r requirements.txt
# 使用 gunicorn 或 uvicorn 启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📱 功能演示与截图

### 首页
- 现代化设计，介绍项目特色
- 用户角色说明，快速导航至登录
- 响应式布局适配多设备

### 登录系统
- 支持多角色登录（学生/教师）
- 表单验证、错误提示
- JWT 认证，安全会话管理

### 学生端功能

#### Dashboard（学生仪表盘）
- 学习统计概览（通过率、练习数、等级）
- 课程进度条
- 最近活动时间线

#### Practice（编程练习）
- **题目选择**：按课程筛选题目列表，显示难度和通过状态
- **代码编辑**：Monaco Editor 集成，支持语法高亮、代码补全
- **实时运行**：点击"运行代码"即时执行，展示输出结果
- **测试评估**：自动运行测试用例，显示通过/失败状态
- **AI 助手**：提交代码后，AI 自动生成改进建议；也支持手动提问
- **题目描述**：支持 Markdown 渲染，包含题目、输入/输出示例

#### Resources（教学资源）
- 浏览和下载教师上传的资源
- 按课程分类展示

#### Forum（论坛讨论）
- 发帖、回帖、点赞、收藏
- 查看讨论热度和评论

#### Profile（个人资料）
- 查看学习统计、成就
- 修改个人信息

### 教师端功能

#### Dashboard（教学仪表盘）
- 快速统计卡片（学生总数、班级数、资源数、待答疑数）
- 快捷操作按钮（资源管理、班级管理、答疑中心、布置作业）
- 今日待办列表，支持添加和删除任务
- 学生活动信息流
- 热门话题、系统公告

#### Class Management（班级管理）
- 学生列表、学习进度追踪
- 班级分组管理

#### Resource Management（资源管理）
- 上传和管理教学资源
- 审核和分类

#### Question Monitor（问题监控）
- 实时查看学生提问
- 快速回答和标记已解决

#### Analytics（学情分析）
- 班级学习数据分析
- AI 生成的学生学情分析报告（面向教师）
- 学生个体分析和建议

#### Assignment Manager（作业管理）
- 创建和布置作业
- 追踪学生完成情况

## 🔧 开发计划与状态

### 已完成功能 ✅
- ✅ 项目架构搭建（Vue 3 + FastAPI）
- ✅ 首页、登录、注册系统
- ✅ JWT 认证与用户管理
- ✅ 学生端编程练习（题目、编辑器、运行测评）
- ✅ 题目动态加载与题目索引管理
- ✅ 代码运行与测试用例验证
- ✅ AI 代码反馈与学情分析（集成 OpenAI API）
- ✅ 论坛系统（发帖、评论、点赞、收藏）
- ✅ 教学资源管理与浏览
- ✅ 教师端仪表盘、班级管理、问题监控
- ✅ 学情分析与数据可视化
- ✅ 响应式设计（桌面、平板、移动适配）
- ✅ 教师学生学情分析 prompt 优化

### 开发中功能 🔄
- 🔄 作业管理与提交功能完善
- 🔄 更多 AI 功能集成（知识点推荐、学习路径优化）
- 🔄 实时通知与消息推送

### 待开发功能 🔲
- 🔲 管理员后台（用户管理、系统配置、数据导出）
- 🔲 小组协作与项目式学习
- 🔲 考试模块与在线测试
- 🔲 高级数据分析与报表导出
- 🔲 第三方 LLM 支持（阿里通义、腾讯混元等）
- 🔲 Docker 容器化部署

### 优化计划 🎯
- 代码编辑器主题切换与格式化工具
- 题目难度自动推断算法优化
- 缓存策略优化（Redis 集成）
- 单元测试覆盖扩展
- E2E 测试自动化
- CI/CD Pipeline 完善

## 🎨 设计规范

### 色彩系统
- **主色调**：教育蓝 (#1890ff) - 用于主要操作按钮、链接
- **辅助色**：
  - 成功绿 (#52c41a) - 通过、成功状态
  - 警告橙 (#faad14) - 中等优先级、警告
  - 错误红 (#f5222d) - 失败、错误状态
  - 教育紫 (#9254de) - 特殊标签
- **中性色**：灰色系用于文本、边框、背景

### 响应式设计
- **桌面**（> 1200px）：三列布局（侧边栏 + 内容 + 右侧面板）
- **平板**（768px - 1200px）：流动布局，内容充分利用空间
- **移动**（< 768px）：单列，隐藏部分菜单，显示汉堡菜单

### 交互动效
- 页面切换：平滑淡入淡出
- 悬停效果：按钮缩放、背景色变化
- 加载动画：骨架屏、加载圈
- 过渡：CSS transition（0.3s）

## 🧪 测试

### 后端测试

```bash
cd backend
pytest -q  # 运行所有测试
pytest tests/test_auth.py -v  # 运行特定文件
```

### 前端测试（可选）

```bash
cd frontend
npm run test  # 需要配置 Jest/Vitest
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

- 项目维护者：高中信息技术教学平台团队
- 项目地址：[GitHub Repository](https://github.com/kaikailuo/bring-py)

---

**让Python编程学习更智能、更高效！** 🐍✨
