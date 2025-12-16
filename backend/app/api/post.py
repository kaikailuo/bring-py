"""
帖子API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.schemas.user import ApiResponse
from app.utils.security import get_current_user
from app.models.user import User, UserRole

router = APIRouter()


@router.post("/posts/", response_model=ApiResponse, summary="创建帖子")
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新帖子
    """
    try:
        # 检查是否被禁言
        if getattr(current_user, 'is_muted', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被禁言，无法发帖"
            )
        # 创建帖子对象
        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            category=post_data.category,
            tags=post_data.tags or [],
            author_id=current_user.id
        )
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return ApiResponse.success(
            data=new_post.to_dict(),
            message="帖子创建成功"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建帖子失败: {str(e)}"
        )


@router.get("/posts/", response_model=ApiResponse, summary="获取帖子列表")
async def get_posts(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取帖子列表，支持按分类筛选
    """
    try:
        query = db.query(Post)
        
        # 按分类筛选
        if category and category != 'all':
            query = query.filter(Post.category == category)
        
        # 按创建时间倒序排列
        posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
        
        posts_data = [post.to_dict() for post in posts]
        
        return ApiResponse.success(
            data=posts_data,
            message="获取帖子列表成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取帖子列表失败: {str(e)}"
        )


@router.get("/posts/{post_id}", response_model=ApiResponse, summary="获取帖子详情")
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个帖子详情
    """
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 增加浏览次数
        post.views += 1
        db.commit()
        
        return ApiResponse.success(
            data=post.to_dict(),
            message="获取帖子详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取帖子详情失败: {str(e)}"
        )


@router.put("/posts/{post_id}", response_model=ApiResponse, summary="更新帖子")
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新帖子（只能更新自己的帖子）
    """
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 检查权限：只能更新自己的帖子
        if post.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此帖子"
            )
        
        # 更新字段
        if post_data.title is not None:
            post.title = post_data.title
        if post_data.content is not None:
            post.content = post_data.content
        if post_data.category is not None:
            post.category = post_data.category
        if post_data.tags is not None:
            post.tags = post_data.tags
        
        db.commit()
        db.refresh(post)
        
        return ApiResponse.success(
            data=post.to_dict(),
            message="帖子更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"更新帖子失败: {str(e)}"
        )


@router.delete("/posts/{post_id}", response_model=ApiResponse, summary="删除帖子")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除帖子（只能删除自己的帖子）
    """
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 检查权限：帖子作者、教师或管理员可删除
        if post.author_id != current_user.id and current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此帖子"
            )
        
        db.delete(post)
        db.commit()
        
        return ApiResponse.success(
            message="帖子删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"删除帖子失败: {str(e)}"
        )
