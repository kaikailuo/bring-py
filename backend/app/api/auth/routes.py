""" 认证相关的API路由 """
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.database import get_db
from app.services.auth import AuthService
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    ApiResponse,
    LoginResponse,
    # 新增：个人资料更新模式
    UserProfileUpdate,
)
from app.utils.security import get_current_active_user
from app.models.user import User
from app.models.user import UserRole
from app.models.post import Post
from app.models.comment import Comment
from app.models.student_result import StudentResult

# 创建路由器
router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/register", response_model=ApiResponse, summary="用户注册")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """ 用户注册接口 """
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data)
        return ApiResponse.success(
            data={"user": UserResponse.model_validate(user).model_dump()},
            message="注册成功"
        )
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"注册失败: {str(e)}")


@router.post("/login", response_model=ApiResponse, summary="用户登录")
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """ 用户登录接口 """
    try:
        auth_service = AuthService(db)
        login_result = auth_service.login_user(login_data)
        return ApiResponse.success(
            data={"token": login_result.token, "user": login_result.user.model_dump()},
            message="登录成功"
        )
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"登录失败: {str(e)}")


@router.post("/logout", response_model=ApiResponse, summary="用户登出")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """ 用户登出接口 """
    return ApiResponse.success(
        data={"user_id": current_user.id, "username": current_user.username},
        message="登出成功"
    )


@router.get("/me", response_model=ApiResponse, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 获取当前用户信息接口 """
    try:
        user_data = UserResponse.model_validate(current_user).model_dump()

        # 统计帖子、评论和答题通过率
        posts_count = db.query(func.count(Post.id)).filter(Post.author_id == current_user.id).scalar() or 0
        comments_count = db.query(func.count(Comment.id)).filter(Comment.author_id == current_user.id).scalar() or 0
        total_submissions = db.query(func.count(StudentResult.id)).filter(StudentResult.student_id == current_user.id).scalar() or 0
        passed_submissions = db.query(func.count(StudentResult.id)).filter(StudentResult.student_id == current_user.id, StudentResult.passed == True).scalar() or 0
        pass_rate = 0
        if total_submissions > 0:
            pass_rate = round((passed_submissions / total_submissions) * 100, 2)

        # 拉取最新帖子与评论（最近5条）用于个人主页详情展示
        recent_posts = db.query(Post).filter(Post.author_id == current_user.id).order_by(Post.created_at.desc()).limit(5).all()
        recent_comments = db.query(Comment).filter(Comment.author_id == current_user.id, Comment.is_deleted == False).order_by(Comment.created_at.desc()).limit(5).all()

        user_data.update({
            "stats": {
                "posts_count": int(posts_count),
                "comments_count": int(comments_count),
                "total_submissions": int(total_submissions),
                "passed_submissions": int(passed_submissions),
                "pass_rate": pass_rate
            },
            "recent_posts": [p.to_dict() for p in recent_posts],
            "recent_comments": [c.to_dict() for c in recent_comments]
        })

        return ApiResponse.success(data={"user": user_data}, message="获取用户信息成功")
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取用户信息失败: {str(e)}")


@router.put("/me", response_model=ApiResponse, summary="更新当前用户信息")
async def update_current_user_info(
    user_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 更新当前用户信息接口 """
    try:
        auth_service = AuthService(db)
        updated_user = auth_service.update_user(current_user.id, user_data)
        return ApiResponse.success(
            data={"user": UserResponse.model_validate(updated_user).model_dump()},
            message="更新用户信息成功"
        )
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"更新用户信息失败: {str(e)}")


@router.post("/change-password", response_model=ApiResponse, summary="修改密码")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 修改密码接口 """
    try:
        auth_service = AuthService(db)
        auth_service.change_password(current_user.id, old_password, new_password)
        return ApiResponse.success(message="密码修改成功")
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"密码修改失败: {str(e)}")


# 管理员专用接口
@router.get("/users", response_model=ApiResponse, summary="获取用户列表（管理员）")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    role: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 获取用户列表接口（仅管理员可用） """
    if current_user.role != "admin":
        return ApiResponse.error(code=403, message="权限不足")
    try:
        auth_service = AuthService(db)
        if role:
            users = auth_service.get_users_by_role(role, skip, limit)
        else:
            users = auth_service.get_all_users(skip, limit)
        user_list = [UserResponse.model_validate(user).model_dump() for user in users]
        return ApiResponse.success(
            data={"users": user_list, "total": len(user_list)},
            message="获取用户列表成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取用户列表失败: {str(e)}")


@router.get("/students", response_model=ApiResponse, summary="获取学生列表（教师/管理员）")
async def get_students(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 获取学生列表：仅教师或管理员可访问 """
    if current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
        return ApiResponse.error(code=403, message="权限不足")
    try:
        users = db.query(User).filter(User.role == UserRole.STUDENT).offset(skip).limit(limit).all()
        user_list = [UserResponse.model_validate(u).model_dump() for u in users]
        return ApiResponse.success(data={"students": user_list, "total": len(user_list)}, message="获取学生列表成功")
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取学生列表失败: {str(e)}")


@router.put("/users/{user_id}/activate", response_model=ApiResponse, summary="激活用户（管理员）")
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 激活用户接口（仅管理员可用） """
    if current_user.role != "admin":
        return ApiResponse.error(code=403, message="权限不足")
    try:
        auth_service = AuthService(db)
        auth_service.activate_user(user_id)
        return ApiResponse.success(message="用户激活成功")
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"用户激活失败: {str(e)}")


@router.put("/users/{user_id}/deactivate", response_model=ApiResponse, summary="停用用户（管理员）")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 停用用户接口（仅管理员可用） """
    if current_user.role != "admin":
        return ApiResponse.error(code=403, message="权限不足")
    try:
        auth_service = AuthService(db)
        auth_service.deactivate_user(user_id)
        return ApiResponse.success(message="用户停用成功")
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"用户停用失败: {str(e)}")


# 教师/管理员：禁言/解禁用户（最小化实现，设置 is_muted 字段）
@router.put("/users/{user_id}/mute", response_model=ApiResponse, summary="禁言/解禁用户（教师/管理员）")
async def mute_user(
    user_id: int,
    mute: bool,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 教师或管理员可以禁言（mute=True）或解禁（mute=False）用户 """
    # 仅教师或管理员可用
    if current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
        return ApiResponse.error(code=403, message="权限不足")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return ApiResponse.error(code=404, message="用户不存在")

        user.is_muted = bool(mute)
        db.commit()

        return ApiResponse.success(
            data={"user_id": user.id, "is_muted": user.is_muted},
            message="禁言状态更新成功"
        )
    except Exception as e:
        db.rollback()
        return ApiResponse.error(code=500, message=f"更新禁言状态失败: {str(e)}")


# =========================
# 新增个人资料功能（最小修改）
# =========================
@router.get("/me/profile", response_model=ApiResponse, summary="获取当前用户个人资料")
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 获取当前用户个人资料接口 """
    try:
        user_data = UserResponse.model_validate(current_user).model_dump()
        posts_count = db.query(func.count(Post.id)).filter(Post.author_id == current_user.id).scalar() or 0
        comments_count = db.query(func.count(Comment.id)).filter(Comment.author_id == current_user.id).scalar() or 0
        total_submissions = db.query(func.count(StudentResult.id)).filter(StudentResult.student_id == current_user.id).scalar() or 0
        passed_submissions = db.query(func.count(StudentResult.id)).filter(StudentResult.student_id == current_user.id, StudentResult.passed == True).scalar() or 0
        pass_rate = 0
        if total_submissions > 0:
            pass_rate = round((passed_submissions / total_submissions) * 100, 2)

        recent_posts = db.query(Post).filter(Post.author_id == current_user.id).order_by(Post.created_at.desc()).limit(5).all()
        recent_comments = db.query(Comment).filter(Comment.author_id == current_user.id, Comment.is_deleted == False).order_by(Comment.created_at.desc()).limit(5).all()

        user_data.update({
            "stats": {
                "posts_count": int(posts_count),
                "comments_count": int(comments_count),
                "total_submissions": int(total_submissions),
                "passed_submissions": int(passed_submissions),
                "pass_rate": pass_rate
            },
            "recent_posts": [p.to_dict() for p in recent_posts],
            "recent_comments": [c.to_dict() for c in recent_comments]
        })

        return ApiResponse.success(data={"user": user_data}, message="获取个人资料成功")
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取个人资料失败: {str(e)}")


@router.put("/me/profile", response_model=ApiResponse, summary="更新当前用户个人资料")
async def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """ 更新当前用户个人资料接口 """
    try:
        auth_service = AuthService(db)
        updated_user = auth_service.update_user(current_user.id, profile_data.dict(exclude_unset=True))
        return ApiResponse.success(
            data={"user": UserResponse.model_validate(updated_user).model_dump()},
            message="更新个人资料成功"
        )
    except HTTPException as e:
        return ApiResponse.error(code=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.error(code=500, message=f"更新个人资料失败: {str(e)}")


@router.get("/users/{user_id}/profile", response_model=ApiResponse, summary="获取指定用户个人资料")
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """ 获取指定用户个人资料接口（公开信息） """
    try:
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(user_id)
        if not user:
            return ApiResponse.error(code=404, message="用户不存在")
        user_data = UserResponse.model_validate(user).model_dump()
        posts_count = db.query(func.count(Post.id)).filter(Post.author_id == user.id).scalar() or 0
        comments_count = db.query(func.count(Comment.id)).filter(Comment.author_id == user.id).scalar() or 0
        total_submissions = db.query(func.count(StudentResult.id)).filter(StudentResult.student_id == user.id).scalar() or 0
        passed_submissions = db.query(func.count(StudentResult.id)).filter(StudentResult.student_id == user.id, StudentResult.passed == True).scalar() or 0
        pass_rate = 0
        if total_submissions > 0:
            pass_rate = round((passed_submissions / total_submissions) * 100, 2)

        recent_posts = db.query(Post).filter(Post.author_id == user.id).order_by(Post.created_at.desc()).limit(5).all()
        recent_comments = db.query(Comment).filter(Comment.author_id == user.id, Comment.is_deleted == False).order_by(Comment.created_at.desc()).limit(5).all()

        user_data.update({
            "stats": {
                "posts_count": int(posts_count),
                "comments_count": int(comments_count),
                "total_submissions": int(total_submissions),
                "passed_submissions": int(passed_submissions),
                "pass_rate": pass_rate
            },
            "recent_posts": [p.to_dict() for p in recent_posts],
            "recent_comments": [c.to_dict() for c in recent_comments]
        })

        return ApiResponse.success(data={"user": user_data}, message="获取个人资料成功")
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取个人资料失败: {str(e)}")


