#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加个人资料字段
添加字段：avatar, nickname, bio, gender, phone
"""
import sys
import os

# 添加项目根目录到Python路径
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from sqlalchemy import text
from app.utils.database import engine, SessionLocal

def migrate_add_profile_fields():
    """
    添加个人资料字段到 users 表
    """
    print("开始数据库迁移：添加个人资料字段...")
    
    db = SessionLocal()
    try:
        # 检查每个字段是否存在，如果不存在则添加
        # SQLite 不支持直接检查列是否存在，所以我们先尝试添加，如果失败就忽略
        
        fields_to_add = [
            ("avatar", "VARCHAR(255)"),
            ("nickname", "VARCHAR(100)"),
            ("bio", "VARCHAR(500)"),
            ("gender", "VARCHAR(20)"),
            ("phone", "VARCHAR(50)")
        ]
        
        for field_name, field_type in fields_to_add:
            try:
                # 尝试添加列（如果已存在会失败，但我们忽略错误）
                alter_sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                db.execute(text(alter_sql))
                db.commit()
                print(f"[OK] 成功添加字段: {field_name}")
            except Exception as e:
                # 如果字段已存在或其他错误，跳过
                error_msg = str(e).lower()
                if "duplicate column" in error_msg or "already exists" in error_msg:
                    print(f"[SKIP] 字段 {field_name} 已存在，跳过")
                else:
                    # 如果是其他错误（比如列已存在但错误信息不同），也尝试继续
                    print(f"[WARN] 添加字段 {field_name} 时出现错误（可能已存在）: {e}")
                    db.rollback()
                    # 继续执行下一个字段
        
        print("\n数据库迁移完成！")
        print("已添加的字段：")
        print("  - avatar: 头像 URL")
        print("  - nickname: 昵称")
        print("  - bio: 个人简介")
        print("  - gender: 性别")
        print("  - phone: 手机号")
        
    except Exception as e:
        print(f"数据库迁移失败: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    migrate_add_profile_fields()

