# 🧭 Git 团队协作开发流程指南

## 🌱 一、分支模型说明

    main（稳定可发布）
    ↑
    │
    │ 🔁 Pull Request 合并（测试通过）
    │
    dev（集成开发分支）
    ↑
    │
    │ 🔀 本地合并功能分支
    │
    feature/功能-开发者（个人开发分支）

### 分支命名规范

| 类型 | 命名格式 | 示例 |
|------|-----------|------|
| 功能分支 | `feature/<功能>-<开发者>` | `feature/login-kaikai` |
| 修复分支 | `fix/<问题>-<开发者>` | `fix/token-expire-lu` |
| 实验分支 | `exp/<尝试>-<开发者>` | `exp/ui-redesign-kaikai` |

---

## 🧩 二、完整协作流程

### 1️⃣ 更新本地 main 与 dev
在开始新功能前，务必先同步远程最新代码：
```bash
git checkout main
git pull origin main

git checkout dev
git pull origin dev
```
### 2️⃣ 从 dev 创建 feature 分支
```bash

git checkout dev
git pull origin dev
git checkout -b feature/<功能>-<开发者>

✅ 所有功能分支都基于 dev 创建，而不是 main。(git branch 可查看当前分支)
```
### 3️⃣ 开发与提交代码
```bash
git add .
git commit -m "提交信息"
Commit 信息规范：

类型    	    前缀	         示例
新功能	    feat:	     feat: 新增注册功能
修复		    fix:         fix: 修复 token 过期问题
优化/重构	refactor:    refactor: 优化数据库连接
文档    	    docs:	     docs: 更新接口说明文档
```
### 4️⃣ 上传 feature 分支到远程
```bash
git push origin feature/<功能>-<开发者>
📌 上传远程是为了备份与让团队可见。
不要直接 push 到 main 或 dev！
```
### 5️⃣ 合并到 dev（本地测试后）
```bash
git checkout dev
git pull origin dev
git merge feature/<功能>-<开发者>
若有冲突：


# 手动解决后
git add .
git commit
然后推送：


git push origin dev
```
### 6️⃣ 提交 Pull Request 给 main
```base
在 GitHub 上：

base: main

compare: dev

标题示例：feat: 登录功能测试完成（by Kaikai）

由团队负责人审核、测试后合并。
```
### 7️⃣ 清理无用分支
开发完成后可清理：
```bash

git branch -d feature/<功能>-<开发者>             # 删除本地
git push origin --delete feature/<功能>-<开发者>   # 删除远程
```
## 🧠 三、团队操作建议
| 操作           | 建议                         |
| ------------ | -------------------------- |
| 每次开发前        | `git pull origin dev` 保持最新 |
| 功能分支完成       | 合并到 dev 后删除分支              |
| Pull Request | 至少一人审核后再合并                 |
| 提交前          | 运行测试、lint、格式化代码            |
| main 分支      | 打开 GitHub 保护，不允许直接 push    |

## 🧰 四、常用命令速查表
| 目标       | 命令                                  |
| -------- | ----------------------------------- |
| 克隆仓库     | `git clone <repo-url>`              |
| 查看分支     | `git branch -a`                     |
| 切换分支     | `git checkout <branch>`             |
| 新建分支     | `git checkout -b <branch>`          |
| 删除分支     | `git branch -d <branch>`            |
| 删除远程分支   | `git push origin --delete <branch>` |
| 查看合并情况   | `git branch --merged`               |
| 撤销最近一次提交 | `git reset --soft HEAD~1`           |


## 🧭 五、整体流程图
        +-------------------+
        |     main（稳定）  |
        +-------------------+

                  ↑
                  │ Pull Request（测试通过）
                  │
        +-------------------+
        |      dev（集成）  |
        +-------------------+
                  ↑
                  │ 本地合并 & 测试
                  │
        +-----------------------------+
        | feature/login-kaikai（功能开发） |
        +-----------------------------+
## ✨ 六、总结一句话
🗣️ 「每个功能独立分支 → 合并到 dev 测试 → 通过后 PR 给 main」

🚫 不直接 push main，🚀 保持 main 稳定干净！