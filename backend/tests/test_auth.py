"""
认证模块的单元测试
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.utils.database import get_db, Base
from app.models.user import User, UserRole
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserLogin

# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建测试数据库表
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAuthAPI:
    """认证API测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        # 清空测试数据库
        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()
    
    def test_register_success(self):
        """测试用户注册成功"""
        user_data = {
            "username": "testuser",
            "password": "password123",
            "role": "student",
            "name": "测试用户",
            "email": "test@example.com"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "注册成功"
        assert data["data"]["user"]["username"] == "testuser"
        assert data["data"]["user"]["role"] == "student"
    
    def test_register_duplicate_username(self):
        """测试注册重复用户名"""
        user_data = {
            "username": "testuser",
            "password": "password123",
            "role": "student",
            "name": "测试用户",
            "email": "test@example.com"
        }
        
        # 第一次注册
        client.post("/api/auth/register", json=user_data)
        
        # 第二次注册相同用户名
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 400
        assert "用户名已存在" in data["message"]
    
    def test_register_invalid_data(self):
        """测试注册无效数据"""
        user_data = {
            "username": "ab",  # 太短
            "password": "123",  # 太短
            "role": "student",
            "name": "测试用户",
            "email": "invalid-email"  # 无效邮箱
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 422  # 验证错误
    
    def test_login_success(self):
        """测试登录成功"""
        # 先注册用户
        user_data = {
            "username": "testuser",
            "password": "password123",
            "role": "student",
            "name": "测试用户",
            "email": "test@example.com"
        }
        client.post("/api/auth/register", json=user_data)
        
        # 登录
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "登录成功"
        assert "token" in data["data"]
        assert data["data"]["user"]["username"] == "testuser"
    
    def test_login_invalid_credentials(self):
        """测试登录无效凭据"""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 401
        assert "用户名或密码错误" in data["message"]
    
    def test_get_current_user(self):
        """测试获取当前用户信息"""
        # 先注册并登录用户
        user_data = {
            "username": "testuser",
            "password": "password123",
            "role": "student",
            "name": "测试用户",
            "email": "test@example.com"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["data"]["token"]
        
        # 获取当前用户信息
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "获取用户信息成功"
        assert data["data"]["user"]["username"] == "testuser"
    
    def test_get_current_user_without_token(self):
        """测试无令牌获取用户信息"""
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # 未授权
    
    def test_logout(self):
        """测试登出"""
        # 先注册并登录用户
        user_data = {
            "username": "testuser",
            "password": "password123",
            "role": "student",
            "name": "测试用户",
            "email": "test@example.com"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["data"]["token"]
        
        # 登出
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/auth/logout", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "登出成功"


class TestAuthService:
    """认证服务测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        self.db = TestingSessionLocal()
        self.auth_service = AuthService(self.db)
        # 清空测试数据库
        self.db.query(User).delete()
        self.db.commit()
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        self.db.close()
    
    def test_create_user(self):
        """测试创建用户"""
        user_data = UserCreate(
            username="testuser",
            password="password123",
            role=UserRole.STUDENT,
            name="测试用户",
            email="test@example.com"
        )
        
        user = self.auth_service.create_user(user_data)
        assert user.username == "testuser"
        assert user.role == UserRole.STUDENT
        assert user.name == "测试用户"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.password_hash is not None
    
    def test_authenticate_user(self):
        """测试用户认证"""
        # 先创建用户
        user_data = UserCreate(
            username="testuser",
            password="password123",
            role=UserRole.STUDENT,
            name="测试用户",
            email="test@example.com"
        )
        self.auth_service.create_user(user_data)
        
        # 认证成功
        user = self.auth_service.authenticate_user("testuser", "password123")
        assert user.username == "testuser"
        
        # 认证失败 - 错误密码
        with pytest.raises(Exception):
            self.auth_service.authenticate_user("testuser", "wrongpassword")
        
        # 认证失败 - 不存在用户
        with pytest.raises(Exception):
            self.auth_service.authenticate_user("nonexistent", "password123")
    
    def test_get_user_by_username(self):
        """测试根据用户名获取用户"""
        # 先创建用户
        user_data = UserCreate(
            username="testuser",
            password="password123",
            role=UserRole.STUDENT,
            name="测试用户",
            email="test@example.com"
        )
        self.auth_service.create_user(user_data)
        
        # 获取用户
        user = self.auth_service.get_user_by_username("testuser")
        assert user.username == "testuser"
        
        # 获取不存在的用户
        user = self.auth_service.get_user_by_username("nonexistent")
        assert user is None
    
    def test_get_user_by_email(self):
        """测试根据邮箱获取用户"""
        # 先创建用户
        user_data = UserCreate(
            username="testuser",
            password="password123",
            role=UserRole.STUDENT,
            name="测试用户",
            email="test@example.com"
        )
        self.auth_service.create_user(user_data)
        
        # 获取用户
        user = self.auth_service.get_user_by_email("test@example.com")
        assert user.email == "test@example.com"
        
        # 获取不存在的用户
        user = self.auth_service.get_user_by_email("nonexistent@example.com")
        assert user is None


if __name__ == "__main__":
    pytest.main([__file__])
