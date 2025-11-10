#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

# 添加项目根目录到Python路径
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# 导入数据库配置和模型
from app.utils.database import engine, Base, init_db as db_init_db
from app.models.user import User
from app.models.resource import Resource


def init_db():
    """
    初始化数据库 - 创建所有表并设置默认数据
    """
    print("正在初始化数据库...")
    
    try:
        # 创建所有表
        print("创建数据库表结构...")
        Base.metadata.create_all(bind=engine)
        print("表结构创建完成！")
        
        # 调用数据库模块中的初始化函数创建默认管理员账户
        print("创建默认管理员账户...")
        db_init_db()
        
        print("数据库初始化成功！")
        print("\n=== 默认账户信息 ===")
        print("用户名: admin")
        print("密码: admin123")
        print("角色: admin")
        print("===================")
        
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    init_db()
