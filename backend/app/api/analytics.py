"""
学情分析API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from app.utils.database import get_db
from app.models.student_result import StudentResult
from app.models.user import User, UserRole
from app.schemas.user import ApiResponse
from app.utils.security import get_current_user
from app.services.problems_service import load_index

router = APIRouter()


@router.get("/analytics/student-answer-stats", response_model=ApiResponse, summary="获取学生答题数统计")
async def get_student_answer_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取每个学生的答题数统计（仅教师和管理员可访问）
    返回格式：
    {
        "students": [
            {
                "student_id": 1,
                "student_name": "张三",
                "total_attempts": 50,
                "total_passed": 30,
                "total_problems": 20
            },
            ...
        ]
    }
    """
    try:
        # 检查权限：只有教师和管理员可以访问
        if current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此资源"
            )
        
        # 获取所有学生
        students = db.query(User).filter(User.role == UserRole.STUDENT).all()
        
        # 统计每个学生的答题情况
        stats = []
        for student in students:
            # 查询该学生的所有答题记录
            results = db.query(StudentResult).filter(
                StudentResult.student_id == student.id
            ).all()
            
            # 计算统计数据
            total_attempts = sum(r.attempts for r in results)
            total_passed = sum(1 for r in results if r.passed)
            # 统计答题的题目数（去重）
            total_problems = len(set((r.lesson, r.problem) for r in results if r.lesson and r.problem))
            
            stats.append({
                "student_id": student.id,
                "student_name": student.name,
                "username": student.username,
                "total_attempts": total_attempts,
                "total_passed": total_passed,
                "total_problems": total_problems,
                "pass_rate": round((total_passed / total_problems * 100) if total_problems > 0 else 0, 2)
            })
        
        # 按答题数降序排序
        stats.sort(key=lambda x: x["total_attempts"], reverse=True)
        
        return ApiResponse.success(
            data={
                "students": stats,
                "total_students": len(stats)
            },
            message="获取学生答题统计成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学生答题统计失败: {str(e)}"
        )


@router.get("/analytics/student-answer-detail/{student_id}", response_model=ApiResponse, summary="获取单个学生详细答题情况")
async def get_student_answer_detail(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个学生的详细答题情况（仅教师和管理员可访问）
    """
    try:
        # 检查权限
        if current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此资源"
            )
        
        # 获取学生信息
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.STUDENT
        ).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生不存在"
            )
        
        # 获取该学生的所有答题记录
        results = db.query(StudentResult).filter(
            StudentResult.student_id == student_id
        ).order_by(StudentResult.last_submitted_at.desc()).all()
        
        # 加载题目索引
        problems_index = load_index() or []
        problems_dict = {}
        for prob in problems_index:
            if isinstance(prob, dict):
                lesson = prob.get("lesson")
                problem = prob.get("problem")
                if lesson and problem:
                    key = (str(lesson), str(problem))
                    problems_dict[key] = {
                        "title": prob.get("title", ""),
                        "path": prob.get("path", ""),
                        "has_test": prob.get("has_test", True)
                    }
        
        # 增强答题记录，添加题目信息
        enhanced_results = []
        for result in results:
            result_dict = result.to_dict()
            # 尝试匹配题目信息
            lesson_key = str(result.lesson) if result.lesson else None
            problem_key = str(result.problem) if result.problem else None
            if lesson_key and problem_key:
                prob_info = problems_dict.get((lesson_key, problem_key))
                if prob_info:
                    result_dict["problem_title"] = prob_info["title"]
                    result_dict["problem_path"] = prob_info["path"]
                    result_dict["has_test"] = prob_info["has_test"]
                else:
                    result_dict["problem_title"] = f"第{lesson_key}课-第{problem_key}题"
                    result_dict["problem_path"] = None
                    result_dict["has_test"] = True
            else:
                result_dict["problem_title"] = "未知题目"
                result_dict["problem_path"] = None
                result_dict["has_test"] = True
            enhanced_results.append(result_dict)
        
        # 按课程分组统计
        lesson_stats = {}
        for result in results:
            lesson_key = result.lesson or "未分类"
            if lesson_key not in lesson_stats:
                lesson_stats[lesson_key] = {
                    "lesson": lesson_key,
                    "total_problems": 0,
                    "total_attempts": 0,
                    "passed_problems": 0
                }
            
            lesson_stats[lesson_key]["total_problems"] += 1
            lesson_stats[lesson_key]["total_attempts"] += result.attempts
            if result.passed:
                lesson_stats[lesson_key]["passed_problems"] += 1
        
        return ApiResponse.success(
            data={
                "student": {
                    "id": student.id,
                    "name": student.name,
                    "username": student.username
                },
                "results": enhanced_results,
                "lesson_stats": list(lesson_stats.values())
            },
            message="获取学生详细答题情况成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学生详细答题情况失败: {str(e)}"
        )

