import sys
import os
import logging
import shutil
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 获取当前文件所在目录的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取backend目录路径
BASE_DIR = os.path.dirname(os.path.dirname(current_file_path))
# 设置上传目录路径
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
# 数据库URL
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
# 用于数据库存储的相对路径根目录
DB_PATH_PREFIX = "uploads/"

# 添加项目根目录到Python路径，以便导入模型
sys.path.append(BASE_DIR)

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 导入模型
from app.models.resource import Resource, ResourceType, ResourceCategory
from app.models.user import User, UserRole

# 映射文件扩展名到资源类型
extension_to_type = {
    '.pdf': ResourceType.PDF,
    '.doc': ResourceType.DOC,
    '.docx': ResourceType.DOC,
    '.ppt': ResourceType.PPT,
    '.pptx': ResourceType.PPT,
    '.mp4': ResourceType.VIDEO,
    '.mp3': ResourceType.VIDEO,
    '.zip': ResourceType.OTHER,
    '.rar': ResourceType.OTHER,
    '.py': ResourceType.OTHER,
    '.md': ResourceType.OTHER,
}

# 映射文件扩展名到资源分类
extension_to_category = {
    '.pdf': ResourceCategory.COURSEWARE,
    '.doc': ResourceCategory.ASSIGNMENT,
    '.docx': ResourceCategory.ASSIGNMENT,
    '.ppt': ResourceCategory.COURSEWARE,
    '.pptx': ResourceCategory.COURSEWARE,
    '.mp4': ResourceCategory.COURSEWARE,
    '.mp3': ResourceCategory.COURSEWARE,
    '.zip': ResourceCategory.REFERENCE,
    '.rar': ResourceCategory.REFERENCE,
    '.py': ResourceCategory.REFERENCE,
    '.md': ResourceCategory.REFERENCE,
}

def get_course_info(file_name):
    """从文件名中提取课程信息"""
    file_name_lower = file_name.lower()
    # 根据文件名中的关键词设置课程信息
    if 'python' in file_name_lower:
        return "1", "Python基础"
    elif 'data' in file_name_lower:
        return "2", "数据结构"
    elif 'algorithm' in file_name_lower:
        return "3", "算法"
    elif 'oop' in file_name_lower or '面向对象' in file_name_lower:
        return "4", "面向对象"
    # 默认课程
    return "1", "Python基础"

def get_default_teacher_id(db):
    """获取默认教师用户的ID"""
    # 查找管理员账户
    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if admin:
        return admin.id
    
    # 查找教师账户
    teacher = db.query(User).filter(User.role == UserRole.TEACHER).first()
    if teacher:
        return teacher.id
    
    # 查找第一个用户
    user = db.query(User).first()
    if user:
        return user.id
    
    # 如果没有任何用户，创建一个临时的教师用户
    logger.warning("系统中没有找到用户，创建一个临时教师用户")
    temp_teacher = User(
        username="temp_teacher",
        password_hash="temp_password",
        role=UserRole.TEACHER,
        name="临时教师",
        email="temp_teacher@example.com",
        is_active=True
    )
    db.add(temp_teacher)
    db.commit()
    db.refresh(temp_teacher)
    return temp_teacher.id

def normalize_file_path(file_path):
    """规范化文件路径，确保路径分隔符一致"""
    return file_path.replace('\\', '/')

def scan_and_register_files():
    """扫描uploads目录并为未注册的文件创建数据库记录"""
    db = SessionLocal()
    try:
        # 获取所有已注册的文件路径
        registered_files = {resource.file_path for resource in db.query(Resource).all()}
        logger.info(f"已注册的文件数量: {len(registered_files)}")
        
        # 获取一个教师用户ID作为创建者
        default_teacher_id = get_default_teacher_id(db)
        logger.info(f"使用用户ID {default_teacher_id} 作为资源创建者")
        
        # 扫描上传目录
        new_files_count = 0
        for root, _, files in os.walk(UPLOAD_DIR):
            for file_name in files:
                # 跳过系统文件和临时文件
                if file_name.startswith('.') or file_name.endswith('.tmp'):
                    continue
                
                # 构建文件绝对路径
                absolute_path = os.path.join(root, file_name)
                
                # 构建相对路径（用于数据库存储）- 使用与系统一致的格式
                # 1. 从uploads目录开始的相对路径
                relative_path_from_uploads = os.path.relpath(absolute_path, UPLOAD_DIR)
                # 2. 添加固定的DB_PATH_PREFIX前缀
                relative_path = normalize_file_path(f"{DB_PATH_PREFIX}{relative_path_from_uploads}")
                
                # 检查文件是否已注册
                if relative_path in registered_files:
                    continue
                
                try:
                    # 获取文件信息
                    file_size = os.path.getsize(absolute_path)
                    file_ext = os.path.splitext(file_name)[1].lower()
                    
                    # 确定资源类型和分类
                    resource_type = extension_to_type.get(file_ext, ResourceType.OTHER)
                    resource_category = extension_to_category.get(file_ext, ResourceCategory.OTHER)
                    
                    # 从文件名中提取课程信息
                    course_id, course_name = get_course_info(file_name)
                    
                    # 创建资源记录
                    new_resource = Resource(
                        title=os.path.splitext(file_name)[0],
                        description="手动添加的教学资源",
                        file_path=relative_path,
                        file_name=file_name,
                        format=file_ext[1:] if file_ext else "unknown",
                        size=file_size,
                        type=resource_type,
                        category=resource_category,
                        created_by=default_teacher_id,
                        # 重要：设置course_id和course_name，这样学生才能看到资源
                        course_id=course_id,
                        course_name=course_name,
                        downloads=0,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    
                    db.add(new_resource)
                    new_files_count += 1
                    logger.info(f"已添加新资源: {file_name}, 路径: {relative_path}, 课程: {course_name}")
                    
                except Exception as e:
                    logger.error(f"添加资源 {file_name} 时出错: {str(e)}")
        
        # 提交更改
        db.commit()
        logger.info(f"扫描完成，共添加 {new_files_count} 个新资源")
        
    except Exception as e:
        logger.error(f"扫描过程中发生错误: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("开始扫描uploads目录...")
    scan_and_register_files()
    logger.info("扫描完成！")