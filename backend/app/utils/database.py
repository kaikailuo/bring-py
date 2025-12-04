"""
数据库配置和连接工具
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库
    """
    # 导入所有模型以确保它们被注册
    from app.models.user import User
    from app.models.post import Post
    from app.models.comment import Comment
    from app.models.favorite import Favorite
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建默认账户（学生和教师）
    create_default_accounts()
    # 创建默认帖子（如不存在）
    create_default_posts()
    # 创建默认评论（如不存在）
    create_default_comments()
    # 创建默认收藏（如不存在）
    create_default_favorites()


def create_default_accounts():
    """
    创建默认账户：8 个学生、2 个老师

    规则：
    - username = "身份+序号"，如 student1, teacher1
    - password = "123456"
    - role = UserRole.STUDENT / UserRole.TEACHER
    - name = 一些中文名（非张三李四）
    - email = "序号@example.com"，学生使用 1-8，教师使用 9-10
    """
    from app.services.auth import AuthService
    from app.schemas.user import UserCreate
    from app.models.user import UserRole

    db = SessionLocal()
    try:
        auth_service = AuthService(db)

        # 学生账户（1-8）
        student_names = [
            "王怡然",
            "刘思源",
            "陈馨予",
            "赵明轩",
            "周婧涵",
            "胡雅楠",
            "侯子辰",
            "钱悦彤",
        ]

        for i in range(1, 9):
            username = f"student{i}"
            email = f"{i}@example.com"
            # 检查是否存在
            if auth_service.get_user_by_username(username) or auth_service.get_user_by_email(email):
                continue
            user_data = UserCreate(
                username=username,
                password="123456",
                role=UserRole.STUDENT,
                name=student_names[i-1],
                email=email
            )
            try:
                auth_service.create_user(user_data)
                print(f"已创建学生账户: {username}/123456")
            except Exception as e:
                print(f"创建学生 {username} 失败: {e}")

        # 教师账户（teacher1, teacher2），emails 9@example.com, 10@example.com
        teacher_names = ["李博文", "苏欣怡"]
        t_email_start = 9
        for j in range(1, 3):
            username = f"teacher{j}"
            email = f"{t_email_start + j - 1}@example.com"
            if auth_service.get_user_by_username(username) or auth_service.get_user_by_email(email):
                continue
            user_data = UserCreate(
                username=username,
                password="123456",
                role=UserRole.TEACHER,
                name=teacher_names[j-1],
                email=email
            )
            try:
                auth_service.create_user(user_data)
                print(f"已创建教师账户: {username}/123456")
            except Exception as e:
                print(f"创建教师 {username} 失败: {e}")

    except Exception as e:
        print(f"创建默认账户失败: {e}")
    finally:
        db.close()


def create_default_posts():
    """
    创建一些示例帖子，作者为已创建的用户（如 teacher1 或 student1/2）。
    如果同标题帖子已存在则跳过，避免重复创建。
    """
    from app.models.post import Post
    from app.models.user import User

    db = SessionLocal()
    try:
        sample_posts = [
            {
            "title": "欢迎来到讨论区",
            "content": (
                "欢迎大家正式加入我们的在线学习社区！🎉\n\n"
                "在这里，你可以：\n"
                "- 提问课堂相关的知识点\n"
                "- 分享学习资料与心得\n"
                "- 发布算法题求助\n"
                "- 自由讨论编程、竞赛或学习方法\n\n"
                "我们希望这里能成为一个轻松、友好、互帮互助的空间。\n"
                "新来的同学可以先在评论区打个招呼哦～😊"
            ),
            "category": "公告",
            "tags": ["welcome", "公告"],
            "author_usernames": ["teacher1", "teacher2"]
           },
           {
            "title": "Python 学习资源推荐",
            "content": (
                "为了帮助同学们更轻松地入门 Python，这里整理了一些不错的学习资源：\n\n"
                "1️⃣ **官方文档**：结构清晰、内容全面，适合作为工具书使用。\n"
                "2️⃣ **廖雪峰 Python 教程**：对初学者非常友好，例子简单易懂。\n"
                "3️⃣ **菜鸟教程 Python**：适合查语法、查函数，非常实用。\n"
                "4️⃣ **牛客 Python 入门题单**：练习题丰富，适合巩固基础。\n\n"
                "如果你有更好的资源推荐，也欢迎补充到评论区～📚"
            ),
            "category": "python-basic",
            "tags": ["python", "资源"],
            "author_usernames": ["teacher1", "teacher2"]
           },
           {
            "title": "算法题讨论区",
            "content": (
                "这里是算法题的专属讨论区！🧠💡\n\n"
                "不管你是在刷 LeetCode、做蓝桥杯练习，还是准备期末，都可以：\n"
                "- 发布自己不会的题目\n"
                "- 分享自己的解法\n"
                "- 和大家一起讨论优化思路\n\n"
                "刷题的路上不必一个人战斗，让我们一起进步吧！🔥"
            ),
            "category": "algorithm",
            "tags": ["算法", "练习"],
            "author_usernames": ["teacher1", "teacher2"]
           },
           {
            "title": "数据结构入门指南",
            "content": (
                "学习数据结构是提升编程能力的重要一步！下面是一些常见数据结构的简单说明：\n\n"
                "📌 **数组**：查询快，插入删除慢\n"
                "📌 **链表**：插入删除快，但随机访问不方便\n"
                "📌 **栈与队列**：适合管理处理顺序，后进先出 / 先进先出\n"
                "📌 **哈希表**：使用哈希函数实现快速查找\n"
                "📌 **树与二叉树**：用于组织层次结构数据\n\n"
                "如果你想进一步学习，我推荐《数据结构与算法分析》（Java/C 版均可）。📖"
            ),
            "category": "data-structure",
            "tags": ["数据结构", "基础"],
            "author_usernames": ["teacher1", "teacher2"]
            }
        ]


        for p in sample_posts:
            # 检查是否已存在同标题帖子，避免重复创建
            exists = db.query(Post).filter(Post.title == p["title"]).first()
            if exists:
                continue

            # 按优先顺序查找可用作者
            author = None
            for uname in p.get("author_usernames", []):
                author = db.query(User).filter(User.username == uname).first()
                if author:
                    break

            # 若未找到优先作者，取任意一个已存在用户作为作者
            if not author:
                author = db.query(User).first()

            if not author:
                # 如果数据库中没有用户（极少见），跳过该帖子创建
                print(f"跳过创建帖子 '{p['title']}'：没有可用作者")
                continue

            new_post = Post(
                title=p["title"],
                content=p["content"],
                category=p["category"],
                tags=p.get("tags", []),
                author_id=author.id
            )
            db.add(new_post)

        db.commit()
        print("已创建默认示例帖子")
    except Exception as e:
        db.rollback()
        print(f"创建默认帖子失败: {e}")
    finally:
        db.close()


def create_default_comments():
    """
    为示例帖子创建一些默认评论，避免重复创建。
    """
    from app.models.comment import Comment
    from app.models.post import Post
    from app.models.user import User

    db = SessionLocal()
    try:
        sample_comments = [
            # --- 欢迎帖子 ---
            {
                "post_title": "欢迎来到讨论区",
                "author_usernames": ["student1"],
                "content": "哈哈，我来报到啦～希望以后能和大家多交流！😊",
                "parent": None
            },
            {
                "post_title": "欢迎来到讨论区",
                "author_usernames": ["student3"],
                "content": "界面挺好看的，比我想象中更专业。",
                "parent": None
            },
            {
                "post_title": "欢迎来到讨论区",
                "author_usernames": ["student5"],
                "content": "期待算法区能活跃点，我最近在刷题感觉好孤单😂",
                "parent": None
            },

            # --- Python 学习资源推荐 ---
            {
                "post_title": "Python 学习资源推荐",
                "author_usernames": ["student2"],
                "content": "我也推廖雪峰的教程，当时入门几乎全靠他了！",
                "parent": None
            },
            {
                "post_title": "Python 学习资源推荐",
                "author_usernames": ["student4"],
                "content": "推荐一个 b 站 up：代码不码，他讲 Python 入门已经很全啦～",
                "parent": None
            },
            {
                "post_title": "Python 学习资源推荐",
                "author_usernames": ["student6"],
                "content": "想问一下有没有适合练习的题单？我刷力扣感觉有点难😥",
                "parent": None
            },

            # --- 算法题讨论区 ---
            {
                "post_title": "算法题讨论区",
                "author_usernames": ["student1"],
                "content": "今天做了双指针的题，有点理解顺了！希望以后可以多发点题目～",
                "parent": None
            },
            {
                "post_title": "算法题讨论区",
                "author_usernames": ["student7"],
                "content": "有没有人一起做周赛？感觉自己做不动了😭",
                "parent": None
            },
            {
                "post_title": "算法题讨论区",
                "author_usernames": ["student8"],
                "content": "推荐把题目按类型整理，一开始先刷数组、哈希表会轻松很多！",
                "parent": None
            },

            # --- 数据结构入门指南 ---
            {
                "post_title": "数据结构入门指南",
                "author_usernames": ["teacher1"],
                "content": "同学们如果在课堂上听不懂，直接在这里提问就好，不用不好意思～",
                "parent": None
            },
            {
                "post_title": "数据结构入门指南",
                "author_usernames": ["student4"],
                "content": "最近看二叉树看到头疼，感觉递归逻辑老绕不清😵‍💫",
                "parent": None
            },
            {
                "post_title": "数据结构入门指南",
                "author_usernames": ["student2"],
                "content": "我觉得树的结构图画出来会更好理解，推荐大家试一下！",
                "parent": None
            }
        ]


        for c in sample_comments:
            post = db.query(Post).filter(Post.title == c["post_title"]).first()
            if not post:
                # 跳过无法匹配的帖子
                continue

            # 选择作者（优先列表 -> 任意已有用户）
            author = None
            for uname in c.get("author_usernames", []):
                author = db.query(User).filter(User.username == uname).first()
                if author:
                    break
            if not author:
                author = db.query(User).first()
            if not author:
                continue

            # 避免重复：如果相同内容在同一帖子已存在则跳过
            exists = db.query(Comment).filter(
                Comment.post_id == post.id,
                Comment.content == c["content"]
            ).first()
            if exists:
                continue

            new_comment = Comment(
                post_id=post.id,
                author_id=author.id,
                content=c["content"],
                parent_id=None
            )
            db.add(new_comment)

            # 提交一次以确保刷新关系，然后更新回复计数
            db.commit()
            post.replies = db.query(Comment).filter(
                Comment.post_id == post.id,
                Comment.is_deleted == False
            ).count()
            db.add(post)
            db.commit()

        print("已创建默认评论")
    except Exception as e:
        db.rollback()
        print(f"创建默认评论失败: {e}")
    finally:
        db.close()


def create_default_favorites():
    """
    为示例帖子创建一些默认收藏记录，避免重复创建。
    """
    from app.models.favorite import Favorite
    from app.models.post import Post
    from app.models.user import User

    db = SessionLocal()
    try:
        sample_favs = [
            {"post_title": "Python 学习资源推荐", "username": "student1"},
            {"post_title": "算法题讨论区", "username": "student2"},
            {"post_title": "数据结构入门指南", "username": "teacher1"},
            {"post_title": "算法题讨论区", "username": "student3"},
        ]

        for f in sample_favs:
            post = db.query(Post).filter(Post.title == f["post_title"]).first()
            user = db.query(User).filter(User.username == f["username"]).first()
            if not post or not user:
                continue

            exists = db.query(Favorite).filter(
                Favorite.post_id == post.id,
                Favorite.user_id == user.id
            ).first()
            if exists:
                continue

            new_fav = Favorite(post_id=post.id, user_id=user.id)
            db.add(new_fav)

        db.commit()
        print("已创建默认收藏")
    except Exception as e:
        db.rollback()
        print(f"创建默认收藏失败: {e}")
    finally:
        db.close()
