-- 迁移脚本：为 users 表添加 is_muted 列
-- 用途：支持教师/管理员禁言功能
-- 执行方式：在 SQLite 客户端运行此脚本

-- 添加 is_muted 列（如果不存在）
-- SQLite 的 ALTER TABLE 不支持 IF NOT EXISTS，所以这里直接添加
-- 如果列已存在，会报错；手动删除该行即可
ALTER TABLE users ADD COLUMN is_muted BOOLEAN DEFAULT 0;

-- 验证（运行后查看是否看到 is_muted 列）
PRAGMA table_info(users);
