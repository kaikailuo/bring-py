#!/usr/bin/env python
"""
快速迁移脚本：为现有 SQLite 数据库添加 is_muted 列
用途：在不使用 Alembic 的情况下快速更新数据库结构
执行方式：python add_is_muted_to_db.py
"""
import sqlite3
import os
import sys

def migrate_add_is_muted():
    """为 users 表添加 is_muted 列"""
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查列是否已存在
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'is_muted' in column_names:
            print("✅ 列 'is_muted' 已存在，无需添加")
            conn.close()
            return True
        
        # 添加 is_muted 列
        cursor.execute("ALTER TABLE users ADD COLUMN is_muted BOOLEAN DEFAULT 0")
        conn.commit()
        
        print("✅ 成功添加列 'is_muted' 到 users 表")
        print("📋 列信息:")
        
        # 查看添加后的列信息
        cursor.execute("PRAGMA table_info(users)")
        for col in cursor.fetchall():
            print(f"   - {col[1]}: {col[2]}")
        
        conn.close()
        return True
    
    except sqlite3.Error as e:
        print(f"❌ 数据库错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未预期的错误: {e}")
        return False

if __name__ == '__main__':
    print("🔄 开始数据库迁移...")
    success = migrate_add_is_muted()
    sys.exit(0 if success else 1)
