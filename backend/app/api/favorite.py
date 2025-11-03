"""
收藏API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.favorite import Favorite
from app.models.post import Post
from app.schemas.user import ApiResponse
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/posts/{post_id}/favorite", response_model=ApiResponse, summary="收藏/取消收藏帖子")
async def toggle_favorite(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    收藏或取消收藏帖子
    """
    try:
        # 检查帖子是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 检查是否已收藏
        favorite = db.query(Favorite).filter(
            Favorite.post_id == post_id,
            Favorite.user_id == current_user.id
        ).first()
        
        if favorite:
            # 取消收藏
            db.delete(favorite)
            is_favorited = False
            message = "取消收藏成功"
        else:
            # 添加收藏
            new_favorite = Favorite(
                post_id=post_id,
                user_id=current_user.id
            )
            db.add(new_favorite)
            is_favorited = True
            message = "收藏成功"
        
        db.commit()
        
        return ApiResponse.success(
            data={"is_favorited": is_favorited},
            message=message
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"操作失败: {str(e)}"
        )


@router.get("/posts/{post_id}/favorite", response_model=ApiResponse, summary="检查是否已收藏")
async def check_favorite(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    检查当前用户是否已收藏该帖子
    """
    try:
        favorite = db.query(Favorite).filter(
            Favorite.post_id == post_id,
            Favorite.user_id == current_user.id
        ).first()
        
        return ApiResponse.success(
            data={"is_favorited": favorite is not None},
            message="查询成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败: {str(e)}"
        )


@router.get("/users/me/favorites", response_model=ApiResponse, summary="获取我的收藏列表")
async def get_my_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的收藏列表
    """
    try:
        favorites = db.query(Favorite).filter(
            Favorite.user_id == current_user.id
        ).order_by(Favorite.created_at.desc()).offset(skip).limit(limit).all()
        
        posts_data = [favorite.post.to_dict() for favorite in favorites if favorite.post]
        
        return ApiResponse.success(
            data=posts_data,
            message="获取收藏列表成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取收藏列表失败: {str(e)}"
        )


