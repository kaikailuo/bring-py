"""
评论API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.schemas.user import ApiResponse
from app.utils.security import get_current_user
from app.models.user import User, UserRole

router = APIRouter()


@router.post("/posts/{post_id}/comments/", response_model=ApiResponse, summary="创建评论")
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建评论
    """
    try:
        # 检查帖子是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 如果是回复评论，检查父评论是否存在
        if comment_data.parent_id:
            parent_comment = db.query(Comment).filter(Comment.id == comment_data.parent_id).first()
            if not parent_comment or parent_comment.post_id != post_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="父评论不存在"
                )

        # 创建评论（忽略comment_data中的post_id，使用URL中的post_id）
        # 检查是否被禁言
        if getattr(current_user, 'is_muted', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被禁言，无法发表评论"
            )

        new_comment = Comment(
            post_id=post_id,
            author_id=current_user.id,
            content=comment_data.content,
            parent_id=comment_data.parent_id
        )
        
        db.add(new_comment)
        
        # 更新帖子的评论数
        post.replies = db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.is_deleted == False
        ).count() + 1
        
        db.commit()
        db.refresh(new_comment)
        
        return ApiResponse.success(
            data=new_comment.to_dict(),
            message="评论创建成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建评论失败: {str(e)}"
        )


@router.get("/posts/{post_id}/comments/", response_model=ApiResponse, summary="获取评论列表")
async def get_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取帖子的评论列表（只获取顶级评论，不包括回复）
    """
    try:
        # 检查帖子是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 获取顶级评论（parent_id为None）
        comments = db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.parent_id == None,
            Comment.is_deleted == False
        ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
        
        comments_data = [comment.to_dict() for comment in comments]
        
        # 为每个顶级评论加载回复
        for comment_dict in comments_data:
            replies = db.query(Comment).filter(
                Comment.parent_id == comment_dict["id"],
                Comment.is_deleted == False
            ).order_by(Comment.created_at.asc()).all()
            comment_dict["replies"] = [reply.to_dict() for reply in replies]
        
        return ApiResponse.success(
            data=comments_data,
            message="获取评论列表成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取评论列表失败: {str(e)}"
        )


@router.put("/comments/{comment_id}/like", response_model=ApiResponse, summary="点赞/取消点赞评论")
async def toggle_comment_like(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    点赞或取消点赞评论
    """
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="评论不存在"
            )
        
        # 简单实现：直接增加点赞数（实际应该用关联表记录点赞关系）
        comment.likes += 1
        db.commit()
        db.refresh(comment)
        
        return ApiResponse.success(
            data={"likes": comment.likes},
            message="点赞成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"点赞失败: {str(e)}"
        )


@router.delete("/comments/{comment_id}", response_model=ApiResponse, summary="删除评论")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除评论（只能删除自己的评论）
    """
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="评论不存在"
            )
        
        # 检查权限：评论作者、教师或管理员可删除
        if comment.author_id != current_user.id and current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此评论"
            )
        
        # 软删除
        comment.is_deleted = True
        
        # 更新帖子的评论数
        post = db.query(Post).filter(Post.id == comment.post_id).first()
        if post:
            post.replies = db.query(Comment).filter(
                Comment.post_id == comment.post_id,
                Comment.is_deleted == False
            ).count()
        
        db.commit()
        
        return ApiResponse.success(
            message="评论删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"删除评论失败: {str(e)}"
        )

