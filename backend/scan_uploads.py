import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.resource import Resource, ResourceType, ResourceCategory
from app.models.user import User
from app.utils.database import Base

# 获取当前文件所在目录的绝对路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 获取backend目录路径
current_file_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(current_file_path)

# 数据库配置
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 文件存储路径
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
# 用于数据库存储的相对路径根目录
DB_PATH_PREFIX = "uploads/"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_default_teacher_id(db):
    """获取默认教师用户的ID"""
    # 优先查找管理员账户
    admin = db.query(User).filter(User.role == "admin").first()
    if admin:
        return admin.id
    
    # 其次查找教师账户
    teacher = db.query(User).filter(User.role == "teacher").first()
    if teacher:
        return teacher.id
    
    # 如果都没有，查找第一个激活的用户
    user = db.query(User).filter(User.is_active == True).first()
    if user:
        return user.id
    
    # 如果没有任何用户，创建一个临时的教师用户（实际运行中应该不会出现这种情况）
    print("警告：系统中没有找到合适的用户，创建一个临时教师用户")
    temp_teacher = User(
        username="temp_teacher",
        password_hash="temp_password",  # 实际环境中应该使用真实的密码哈希
        role="teacher",
        name="临时教师",
        email="temp_teacher@example.com",
        is_active=True
    )
    db.add(temp_teacher)
    db.commit()
    db.refresh(temp_teacher)
    return temp_teacher.id

def get_file_type(file_ext):
    """根据文件扩展名确定资源类型"""
    file_ext = file_ext.lower()
    type_map = {
        'ppt': ResourceType.PPT,
        'pptx': ResourceType.PPT,
        'pdf': ResourceType.PDF,
        'doc': ResourceType.DOC,
        'docx': ResourceType.DOC,
        'mp4': ResourceType.VIDEO,
        'avi': ResourceType.VIDEO,
        'mov': ResourceType.VIDEO,
        'wmv': ResourceType.VIDEO
    }
    return type_map.get(file_ext, ResourceType.OTHER)

def get_file_category(file_ext):
    """根据文件扩展名确定资源分类"""
    file_ext = file_ext.lower()
    # 简单的分类逻辑，可以根据实际需求调整
    if file_ext in ['ppt', 'pptx', 'pdf']:
        return ResourceCategory.COURSEWARE
    elif file_ext in ['doc', 'docx']:
        return ResourceCategory.ASSIGNMENT
    else:
        return ResourceCategory.REFERENCE

def scan_uploads():
    """扫描uploads文件夹并为未注册的文件创建数据库记录"""
    db = SessionLocal()
    try:
        # 获取默认教师ID
        default_teacher_id = get_default_teacher_id(db)
        print(f"使用默认用户ID: {default_teacher_id} 作为创建者")
        
        # 获取数据库中已存在的所有文件路径
        existing_files = set()
        resources = db.query(Resource).all()
        for resource in resources:
            # 规范化路径分隔符，确保Windows兼容性
            file_path = os.path.normpath(resource.file_path)
            existing_files.add(file_path)
        
        print(f"数据库中已存在 {len(existing_files)} 个资源记录")
        
        # 扫描uploads文件夹
        new_files_count = 0
        updated_files_count = 0
        
        if not os.path.exists(UPLOAD_DIR):
            print(f"警告：上传目录 {UPLOAD_DIR} 不存在")
            return
        
        for root, _, files in os.walk(UPLOAD_DIR):
            for file_name in files:
                # 跳过系统文件和隐藏文件
                if file_name.startswith('.') or file_name in ['Thumbs.db']:
                    continue
                
                # 获取文件的绝对路径
                abs_file_path = os.path.join(root, file_name)
                
                # 计算相对路径（相对于backend目录）
                rel_path = os.path.relpath(abs_file_path, BASE_DIR)
                
                # 规范化路径分隔符，确保与数据库中存储的路径一致
                rel_path = os.path.normpath(rel_path)
                
                # 获取文件大小
                file_size = os.path.getsize(abs_file_path)
                
                # 获取文件扩展名
                file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')
                if not file_ext:
                    file_ext = 'unknown'
                
                # 确定资源类型和分类
                resource_type = get_file_type(file_ext)
                resource_category = get_file_category(file_ext)
                
                # 检查文件是否已经在数据库中
                if rel_path in existing_files:
                    # 检查是否需要更新文件大小或其他信息
                    resource = db.query(Resource).filter(Resource.file_path == rel_path).first()
                    if resource and resource.size != file_size:
                        resource.size = file_size
                        resource.updated_at = datetime.now()
                        db.commit()
                        updated_files_count += 1
                        print(f"更新资源: {file_name} (大小: {file_size} bytes)")
                    continue
                
                # 为新文件创建资源记录
                try:
                    # 去掉时间戳前缀（如果有），以便更好地显示文件名
                    clean_file_name = file_name
                    # 尝试去掉像 "20231121123456_1_" 这样的前缀
                    parts = file_name.split('_')
                    if len(parts) >= 3 and parts[0].isdigit() and len(parts[0]) == 14 and parts[1].isdigit():
                        clean_file_name = '_'.join(parts[2:])
                    
                    new_resource = Resource(
                        title=os.path.splitext(clean_file_name)[0],  # 使用文件名（不含扩展名）作为标题
                        description="手动添加的资源",
                        file_path=rel_path,
                        file_name=file_name,
                        format=file_ext,
                        size=file_size,
                        type=resource_type,
                        category=resource_category,
                        created_by=default_teacher_id,
                        course_id=None,  # 手动添加的资源默认为不关联课程
                        course_name=None,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    
                    db.add(new_resource)
                    db.commit()
                    new_files_count += 1
                    print(f"添加新资源: {file_name} (类型: {resource_type.value}, 分类: {resource_category.value})")
                except Exception as e:
                    db.rollback()
                    print(f"添加资源 {file_name} 时出错: {str(e)}")
        
        # 提交所有更改
        db.commit()
        print(f"扫描完成！新添加了 {new_files_count} 个资源，更新了 {updated_files_count} 个资源")
        
    except Exception as e:
        db.rollback()
        print(f"扫描过程中发生错误: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("开始扫描uploads文件夹...")
    scan_uploads()
    print("扫描结束！")