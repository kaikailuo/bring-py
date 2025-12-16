"""
安全相关的工具函数
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.user import User
from app.schemas.user import TokenData
from dotenv import load_dotenv
import os

# 读取 .env 配置文件
load_dotenv()

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 配置
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if SECRET_KEY == "dev-secret-key":
    print("[WARNING] Using development default secret key - DO NOT USE IN PRODUCTION!")
# HTTP Bearer认证
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    生成密码哈希
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    验证令牌并返回令牌数据
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        
        if username is None or user_id is None:
            raise credentials_exception
            
        token_data = TokenData(
            username=username,
            user_id=user_id,
            role=role
        )
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前用户
    """
    token = credentials.credentials
    token_data = verify_token(token)
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_role(required_role: str):
    """
    角色权限验证装饰器
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def require_admin(current_user: User = Depends(require_role("admin"))) -> User:
    """
    要求管理员权限
    """
    return current_user


def require_teacher(current_user: User = Depends(require_role("teacher"))) -> User:
    """
    要求教师权限
    """
    return current_user


def require_student(current_user: User = Depends(require_role("student"))) -> User:
    """
    要求学生权限
    """
    return current_user


def check_password_strength(password: str) -> dict:
    """
    检查密码强度
    """
    issues = []
    
    if len(password) < 6:
        issues.append("密码长度至少6位")
    if len(password) > 20:
        issues.append("密码长度不能超过20位")
    if not any(c.islower() for c in password):
        issues.append("密码应包含小写字母")
    if not any(c.isupper() for c in password):
        issues.append("密码应包含大写字母")
    if not any(c.isdigit() for c in password):
        issues.append("密码应包含数字")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        issues.append("密码应包含特殊字符")
    
    return {
        "is_strong": len(issues) == 0,
        "issues": issues,
        "strength": "weak" if len(issues) > 2 else "medium" if len(issues) > 0 else "strong"
    }
