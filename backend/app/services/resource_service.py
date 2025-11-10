import os
import shutil
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from datetime import datetime
from app.models.resource import Resource, ResourceType
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.models.user import User

# 修改文件存储路径处理逻辑
# 获取当前文件所在目录的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取backend目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# 配置文件存储绝对路径，uploads目录应该在backend目录下
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 用于数据库存储的相对路径根目录
DB_PATH_PREFIX = "uploads/"

# 文件类型和大小限制配置
# 允许的文件类型映射表：{扩展名: (对应的ResourceType, 允许的MIME类型列表)}
ALLOWED_FILE_TYPES = {
    'ppt': (ResourceType.PPT, ['application/vnd.ms-powerpoint']),
    'pptx': (ResourceType.PPT, ['application/vnd.openxmlformats-officedocument.presentationml.presentation']),
    'pdf': (ResourceType.PDF, ['application/pdf']),
    'doc': (ResourceType.DOC, ['application/msword']),
    'docx': (ResourceType.DOC, ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']),
    'mp4': (ResourceType.VIDEO, ['video/mp4']),
    'avi': (ResourceType.VIDEO, ['video/x-msvideo']),
    'mov': (ResourceType.VIDEO, ['video/quicktime']),
    'wmv': (ResourceType.VIDEO, ['video/x-ms-wmv']),
    # 可以根据需要添加更多文件类型
}

# 最大允许的文件大小（字节），这里设置为100MB
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

class ResourceService:
    """资源服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_resource_by_id(self, resource_id: int) -> Resource:
        """根据ID获取资源"""
        resource = self.db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资源不存在"
            )
        return resource
    
    def get_resources(self, page: int = 1, page_size: int = 10, search: str = "", 
                     type_filter: str = None, category_filter: str = None, 
                     course_id_filter: str = None, user: User = None) -> dict:
        """获取资源列表，支持分页、搜索和筛选"""
        query = self.db.query(Resource)
        
        # 根据用户角色进行过滤
        if user and user.role == "student":
            # 学生只能看到关联了课程的资源
            query = query.filter(Resource.course_id.isnot(None))
        # 教师可以看到所有资源
        
        # 搜索
        if search:
            query = query.filter(Resource.title.contains(search) | Resource.description.contains(search))
        
        # 类型筛选
        if type_filter:
            query = query.filter(Resource.type == type_filter)
        
        # 分类筛选
        if category_filter:
            query = query.filter(Resource.category == category_filter)
        
        # 课程ID筛选
        if course_id_filter:
            query = query.filter(Resource.course_id == course_id_filter)
        
        # 总数
        total = query.count()
        
        # 分页
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "page_size": page_size
        }
    
    def validate_file(self, file: UploadFile) -> tuple[str, ResourceType]:
        """验证文件类型和大小"""
        # 获取文件扩展名
        file_extension = os.path.splitext(file.filename)[1].lower().lstrip('.')
        
        # 验证文件类型
        if file_extension not in ALLOWED_FILE_TYPES:
            allowed_extensions = ', '.join(ALLOWED_FILE_TYPES.keys())
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件类型。允许的文件类型: {allowed_extensions}"
            )
        
        # 验证MIME类型
        allowed_mime_types = ALLOWED_FILE_TYPES[file_extension][1]
        if file.content_type and file.content_type not in allowed_mime_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件MIME类型不匹配。请确保上传的是正确的{file_extension.upper()}文件。"
            )
        
        # 获取资源类型
        resource_type = ALLOWED_FILE_TYPES[file_extension][0]
        
        # 验证文件大小
        # 注意：这里我们假设file对象有size属性，如果没有，需要在保存文件后验证
        if hasattr(file.file, 'size') and file.file.size > MAX_FILE_SIZE:
            max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件大小超过限制。最大允许大小: {max_size_mb}MB"
            )
        
        return file_extension, resource_type
    
    def create_resource(self, resource_data: ResourceCreate, file: UploadFile, user: User) -> Resource:
        """创建新资源"""
        # 验证文件类型和大小
        file_extension, validated_type = self.validate_file(file)
        
        # 生成唯一的文件名，避免冲突
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}_{user.id}_{os.path.basename(file.filename)}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        # 保存文件
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文件保存失败: {str(e)}"
            )
        finally:
            file.file.close()
        
        # 再次验证文件大小（确保实际保存的文件符合大小限制）
        actual_size = os.path.getsize(file_path)
        if actual_size > MAX_FILE_SIZE:
            # 删除已保存的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件大小超过限制。最大允许大小: {max_size_mb}MB"
            )
        
        # 创建资源记录 - 存储相对路径，不存储绝对路径
        try:
            # 存储相对路径而不是绝对路径
            db_resource = Resource(
                title=resource_data.title,
                description=resource_data.description,
                file_path=f"{DB_PATH_PREFIX}{file_name}",  # 存储相对路径
                file_name=file.filename,
                format=file_extension if file_extension else "unknown",
                size=actual_size,
                type=validated_type,  # 使用验证后的类型，而不是用户提供的类型
                category=resource_data.category,
                created_by=user.id,
                course_id=resource_data.course_id,
                course_name=resource_data.course_name
            )
            
            self.db.add(db_resource)
            self.db.commit()
            self.db.refresh(db_resource)
            
            return db_resource
        except Exception as e:
            # 如果数据库操作失败，删除已保存的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"创建资源失败: {str(e)}"
            )
    
    def update_resource(self, resource_id: int, resource_data: ResourceUpdate) -> Resource:
        """更新资源信息"""
        db_resource = self.get_resource_by_id(resource_id)
        
        # 更新字段
        update_data = resource_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_resource, key, value)
        
        self.db.commit()
        self.db.refresh(db_resource)
        
        return db_resource

    def delete_resource(self, resource_id: int):
        """删除资源"""
        db_resource = self.get_resource_by_id(resource_id)

        # 删除文件 - 使用相对路径构建绝对路径
        file_path = os.path.join(BASE_DIR, db_resource.file_path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"文件删除失败: {str(e)}"
                )
        
        # 删除数据库记录
        self.db.delete(db_resource)
        self.db.commit()
        
        return {
            "message": "资源删除成功"
        }
    
    def increment_download_count(self, resource_id: int):
        """增加资源下载次数"""
        db_resource = self.get_resource_by_id(resource_id)
        db_resource.downloads += 1
        self.db.commit()
        return db_resource