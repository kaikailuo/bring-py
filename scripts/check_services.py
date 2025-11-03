#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务状态检查脚本
"""
import requests
import subprocess
import sys
import time
import socket

def check_port(host, port):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_backend():
    """检查后端服务"""
    print("🔍 检查后端服务...")
    
    # 检查端口
    if check_port('localhost', 8000):
        print("✅ 后端端口8000已开放")
        
        # 检查API健康状态
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ 后端API响应正常")
                return True
            else:
                print(f"❌ 后端API响应异常: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 后端API连接失败: {e}")
            return False
    else:
        print("❌ 后端端口8000未开放")
        return False

def check_frontend():
    """检查前端服务"""
    print("\n🔍 检查前端服务...")
    
    # 检查端口
    if check_port('localhost', 5173):
        print("✅ 前端端口5173已开放")
        
        # 检查前端页面
        try:
            response = requests.get('http://localhost:5173', timeout=5)
            if response.status_code == 200:
                print("✅ 前端页面响应正常")
                return True
            else:
                print(f"❌ 前端页面响应异常: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 前端页面连接失败: {e}")
            return False
    else:
        print("❌ 前端端口5173未开放")
        return False

def check_cors():
    """检查CORS配置"""
    print("\n🔍 检查CORS配置...")
    
    try:
        # 模拟前端请求
        headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json'
        }
        response = requests.get('http://localhost:8000/api/auth/me', headers=headers, timeout=5)
        
        # 检查CORS头
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]
        
        for header in cors_headers:
            if header in response.headers:
                print(f"✅ CORS头 {header} 存在")
            else:
                print(f"❌ CORS头 {header} 缺失")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ CORS检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 高中信息技术教学平台 - 服务诊断")
    print("=" * 50)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    if backend_ok and frontend_ok:
        check_cors()
        print("\n✅ 所有服务运行正常！")
        print("🌐 前端地址: http://localhost:5173")
        print("📖 后端API文档: http://localhost:8000/docs")
    else:
        print("\n❌ 服务检查发现问题！")
        print("\n🔧 解决方案：")
        if not backend_ok:
            print("1. 启动后端服务: python scripts/start_backend.py")
        if not frontend_ok:
            print("2. 启动前端服务: python scripts/start_frontend.py")
        print("3. 或者使用一键启动: python scripts/start_both.py")

if __name__ == "__main__":
    main()

