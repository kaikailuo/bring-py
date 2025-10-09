"""
认证相关的业务逻辑
"""
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse
from app.utils.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        创建新用户
        """
        # 检查用户名是否已存在
        if self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 创建新用户
        try:
            db_user = User(
                username=user_data.username,
                password_hash=get_password_hash(user_data.password),
                role=user_data.role,
                name=user_data.name,
                email=user_data.email,
                is_active=True
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return db_user
            
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="创建用户失败，请检查输入信息"
            )
    
    def authenticate_user(self, username: str, password: str) -> User:
        """
        用户认证
        """
        user = self.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="账户已被禁用"
            )
        
        return user
    
    def login_user(self, login_data: UserLogin) -> LoginResponse:
        """
        用户登录
        """
        user = self.authenticate_user(login_data.username, login_data.password)
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "role": user.role.value
            },
            expires_delta=access_token_expires
        )
        
        return LoginResponse(
            token=access_token,
            user=UserResponse.from_orm(user)
        )
    
    def get_user_by_username(self, username: str) -> User:
        """
        根据用户名获取用户
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> User:
        """
        根据邮箱获取用户
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> User:
        """
        根据ID获取用户
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_info(self, user_id: int) -> UserResponse:
        """
        获取用户信息
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return UserResponse.from_orm(user)
    
    def update_user(self, user_id: int, update_data: dict) -> User:
        """
        更新用户信息
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新用户信息
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                if field == "password":
                    setattr(user, "password_hash", get_password_hash(value))
                else:
                    setattr(user, field, value)
        
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="更新用户信息失败"
            )
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        停用用户
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        user.is_active = False
        self.db.commit()
        return True
    
    def activate_user(self, user_id: int) -> bool:
        """
        激活用户
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        user.is_active = True
        self.db.commit()
        return True
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        修改密码
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="原密码错误"
            )
        
        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        return True
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        获取所有用户列表（分页）
        """
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_users_by_role(self, role: str, skip: int = 0, limit: int = 100) -> list[User]:
        """
        根据角色获取用户列表
        """
        return self.db.query(User).filter(
            User.role == role,
            User.is_active == True
        ).offset(skip).limit(limit).all()
