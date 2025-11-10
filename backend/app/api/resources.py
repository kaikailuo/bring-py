"""
资源管理相关的API路由
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from urllib.parse import quote
from app.utils.database import get_db
from app.services.resource_service import ResourceService
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
    ResourceListResponse,
    ApiResponse
)
from app.utils.security import get_current_active_user, require_teacher
from app.models.user import User
from app.models.resource import ResourceType, ResourceCategory

# 创建路由器
router = APIRouter(prefix="/api/resources", tags=["资源管理"])


@router.post("/", response_model=ApiResponse, summary="上传资源")
async def create_resource(
    title: str = Query(..., min_length=1, max_length=255),
    description: str = Query(None),
    type: ResourceType = Query(...),
    category: ResourceCategory = Query(...),
    course_id: str = Query(None),
    course_name: str = Query(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)  # 只允许教师上传
):
    """
    上传教学资源
    
    - **title**: 资源标题
    - **description**: 资源描述
    - **type**: 资源类型
    - **category**: 资源分类
    - **course_id**: 关联课程ID
    - **course_name**: 关联课程名称
    - **file**: 上传的文件
    """
    try:
        # 创建资源数据
        resource_data = ResourceCreate(
            title=title,
            description=description,
            type=type,
            category=category,
            course_id=course_id,
            course_name=course_name
        )
        
        resource_service = ResourceService(db)
        resource = resource_service.create_resource(resource_data, file, current_user)
        
        return ApiResponse.success(
            data={"resource": ResourceResponse.from_orm(resource).dict()},
            message="资源上传成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"资源上传失败: {str(e)}"
        )


@router.get("/", response_model=ApiResponse, summary="获取资源列表")
async def get_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    type_filter: str = Query(None),
    category_filter: str = Query(None),
    course_id_filter: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # 所有已登录用户都可以获取资源列表
):
    """
    获取资源列表，支持分页、搜索和筛选
    
    - **page**: 页码
    - **page_size**: 每页数量
    - **search**: 搜索关键词
    - **type_filter**: 资源类型筛选
    - **category_filter**: 资源分类筛选
    - **course_id_filter**: 课程ID筛选
    """
    try:
        resource_service = ResourceService(db)
        result = resource_service.get_resources(
            page=page,
            page_size=page_size,
            search=search,
            type_filter=type_filter,
            category_filter=category_filter,
            course_id_filter=course_id_filter,
            user=current_user  # 传递当前用户信息
        )
        
        return ApiResponse.success(
            data={
                "total": result["total"],
                "items": [ResourceResponse.from_orm(item).dict() for item in result["items"]],
                "page": result["page"],
                "page_size": result["page_size"]
            },
            message="获取资源列表成功"
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"获取资源列表失败: {str(e)}"
        )


@router.get("/{resource_id}", response_model=ApiResponse, summary="获取资源详情")
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # 所有已登录用户都可以获取资源详情
):
    """
    获取资源详情
    
    - **resource_id**: 资源ID
    """
    try:
        resource_service = ResourceService(db)
        resource = resource_service.get_resource_by_id(resource_id)
        
        return ApiResponse.success(
            data={"resource": ResourceResponse.from_orm(resource).dict()},
            message="获取资源详情成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"获取资源详情失败: {str(e)}"
        )


@router.put("/{resource_id}", response_model=ApiResponse, summary="更新资源信息")
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)  # 只允许教师更新资源
):
    """
    更新资源信息
    
    - **resource_id**: 资源ID
    - **resource_data**: 资源更新数据
    """
    try:
        resource_service = ResourceService(db)
        resource = resource_service.update_resource(resource_id, resource_data)
        
        return ApiResponse.success(
            data={"resource": ResourceResponse.from_orm(resource).dict()},
            message="资源更新成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"资源更新失败: {str(e)}"
        )


@router.delete("/{resource_id}", response_model=ApiResponse, summary="删除资源")
async def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)  # 只允许教师删除资源
):
    """
    删除资源
    
    - **resource_id**: 资源ID
    """
    try:
        resource_service = ResourceService(db)
        result = resource_service.delete_resource(resource_id)
        
        return ApiResponse.success(
            data=result,
            message="资源删除成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"资源删除失败: {str(e)}"
        )


@router.get("/{resource_id}/download", summary="下载资源")
async def download_resource(
        resource_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)  # 所有已登录用户都可以下载资源
):
    """
    下载资源文件

    - **resource_id**: 资源ID
    """
    try:
        resource_service = ResourceService(db)
        resource = resource_service.get_resource_by_id(resource_id)

        # 获取当前文件所在目录的绝对路径
        current_file_path = os.path.abspath(__file__)
        # 获取backend目录路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        
        # 使用相对路径构建绝对路径
        # 添加路径规范化处理，确保Windows路径分隔符正确
        file_path = os.path.normpath(os.path.join(BASE_DIR, resource.file_path))
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 尝试直接使用uploads目录构建路径作为备选方案
            alternative_path = os.path.normpath(os.path.join(BASE_DIR, "uploads", os.path.basename(resource.file_path)))

            if os.path.exists(alternative_path):
                file_path = alternative_path
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="文件不存在"
                )

        # 增加下载次数
        resource_service.increment_download_count(resource_id)

        # 使用resource.file_name作为下载文件名，确保包含正确的扩展名
        # FileResponse会自动设置Content-Disposition头，只需要传入filename参数即可
        # 如果文件名包含中文或特殊字符，需要确保正确编码
        return FileResponse(
            path=file_path,
            filename=resource.file_name,  # 使用数据库中存储的原始文件名，包含扩展名
            media_type="application/octet-stream"
        )
    except HTTPException as e:
        # 直接抛出HTTPException，因为这是文件下载接口，不是JSON响应
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件下载失败: {str(e)}"
        )