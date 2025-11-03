"""
问题相关的服务层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import re
from collections import Counter
from app.models.question import Question, QuestionCategory, QuestionReply, QuestionSummary, QuestionStatus, QuestionPriority
from app.models.user import User
from app.services.ai_analysis import AIAnalysisService
from app.schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionCategoryCreate, QuestionCategoryUpdate,
    QuestionReplyCreate, QuestionSummaryCreate, QuestionFilterParams, QuestionSummaryParams
)


class QuestionService:
    """问题服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIAnalysisService()

    # 问题分类相关方法
    def create_category(self, category_data: QuestionCategoryCreate) -> QuestionCategory:
        """创建问题分类"""
        category = QuestionCategory(**category_data.dict())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[QuestionCategory]:
        """获取问题分类列表"""
        return self.db.query(QuestionCategory).filter(
            QuestionCategory.is_active == True
        ).offset(skip).limit(limit).all()

    def get_category_by_id(self, category_id: int) -> Optional[QuestionCategory]:
        """根据ID获取问题分类"""
        return self.db.query(QuestionCategory).filter(
            QuestionCategory.id == category_id
        ).first()

    def update_category(self, category_id: int, category_data: QuestionCategoryUpdate) -> Optional[QuestionCategory]:
        """更新问题分类"""
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        """删除问题分类"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        
        self.db.delete(category)
        self.db.commit()
        return True

    # 问题相关方法
    def create_question(self, question_data: QuestionCreate, student_id: int) -> Question:
        """创建问题"""
        question_dict = question_data.dict()
        question_dict['student_id'] = student_id
        
        # 处理标签
        if question_dict.get('tags'):
            question_dict['tags'] = question_dict['tags']
        
        # AI分析问题内容
        content = question_dict.get('title', '') + ' ' + question_dict.get('content', '')
        ai_analysis = self.ai_service.analyze_question_content(content)
        
        # 如果没有指定分类，使用AI分析的分类
        if not question_dict.get('category_id'):
            # 查找匹配的分类
            category = self.db.query(QuestionCategory).filter(
                QuestionCategory.name == ai_analysis['category']
            ).first()
            if category:
                question_dict['category_id'] = category.id
        
        # 设置AI分析的优先级
        priority_mapping = {
            'high': QuestionPriority.HIGH,
            'medium': QuestionPriority.MEDIUM,
            'low': QuestionPriority.LOW
        }
        question_dict['priority'] = priority_mapping.get(ai_analysis['priority'], QuestionPriority.MEDIUM)
        
        question = Question(**question_dict)
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def get_questions(self, filters: QuestionFilterParams) -> List[Question]:
        """获取问题列表"""
        query = self.db.query(Question)
        
        # 应用筛选条件
        if filters.category_id:
            query = query.filter(Question.category_id == filters.category_id)
        if filters.status:
            query = query.filter(Question.status == filters.status)
        if filters.priority:
            query = query.filter(Question.priority == filters.priority)
        if filters.student_id:
            query = query.filter(Question.student_id == filters.student_id)
        if filters.teacher_id:
            query = query.filter(Question.teacher_id == filters.teacher_id)
        if filters.keyword:
            query = query.filter(
                or_(
                    Question.title.contains(filters.keyword),
                    Question.content.contains(filters.keyword)
                )
            )
        if filters.start_date:
            query = query.filter(Question.created_at >= filters.start_date)
        if filters.end_date:
            query = query.filter(Question.created_at <= filters.end_date)
        
        return query.order_by(desc(Question.created_at)).offset(filters.skip).limit(filters.limit).all()

    def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """根据ID获取问题"""
        return self.db.query(Question).filter(Question.id == question_id).first()

    def update_question(self, question_id: int, question_data: QuestionUpdate) -> Optional[Question]:
        """更新问题"""
        question = self.get_question_by_id(question_id)
        if not question:
            return None
        
        update_data = question_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(question, field, value)
        
        # 如果更新了答案，设置回答时间
        if 'answer' in update_data and update_data['answer']:
            question.answer_time = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(question)
        return question

    def assign_question(self, question_id: int, teacher_id: int) -> Optional[Question]:
        """分配问题给教师"""
        question = self.get_question_by_id(question_id)
        if not question:
            return None
        
        question.teacher_id = teacher_id
        self.db.commit()
        self.db.refresh(question)
        return question

    def delete_question(self, question_id: int) -> bool:
        """删除问题"""
        question = self.get_question_by_id(question_id)
        if not question:
            return False
        
        self.db.delete(question)
        self.db.commit()
        return True

    # 问题回复相关方法
    def create_reply(self, question_id: int, reply_data: QuestionReplyCreate, user_id: int) -> Optional[QuestionReply]:
        """创建问题回复"""
        question = self.get_question_by_id(question_id)
        if not question:
            return None
        
        # 判断是否为教师回复
        user = self.db.query(User).filter(User.id == user_id).first()
        is_teacher_reply = user.role == "teacher" if user else False
        
        reply_dict = reply_data.dict()
        reply_dict['question_id'] = question_id
        reply_dict['user_id'] = user_id
        reply_dict['is_teacher_reply'] = is_teacher_reply
        
        reply = QuestionReply(**reply_dict)
        self.db.add(reply)
        
        # 如果是解决方案，更新问题状态
        if reply_data.is_solution:
            question.status = QuestionStatus.RESOLVED
        
        self.db.commit()
        self.db.refresh(reply)
        return reply

    def get_question_replies(self, question_id: int) -> List[QuestionReply]:
        """获取问题的回复列表"""
        return self.db.query(QuestionReply).filter(
            QuestionReply.question_id == question_id
        ).order_by(QuestionReply.created_at).all()

    # 问题统计相关方法
    def get_question_stats(self, teacher_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
        """获取问题统计信息"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        query = self.db.query(Question).filter(
            Question.created_at >= start_date,
            Question.created_at <= end_date
        )
        
        if teacher_id:
            query = query.filter(Question.teacher_id == teacher_id)
        
        questions = query.all()
        
        # 基础统计
        total_questions = len(questions)
        pending_questions = len([q for q in questions if q.status == QuestionStatus.PENDING])
        answered_questions = len([q for q in questions if q.status == QuestionStatus.ANSWERED])
        resolved_questions = len([q for q in questions if q.status == QuestionStatus.RESOLVED])
        
        # 分类分布
        category_distribution = {}
        for question in questions:
            if question.category:
                category_name = question.category.name
                category_distribution[category_name] = category_distribution.get(category_name, 0) + 1
        
        # 优先级分布
        priority_distribution = {}
        for question in questions:
            if question.priority:
                priority_distribution[question.priority.value] = priority_distribution.get(question.priority.value, 0) + 1
        
        # 每日问题数量
        daily_counts = {}
        for question in questions:
            date_str = question.created_at.strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        daily_question_count = [
            {"date": date, "count": count} 
            for date, count in sorted(daily_counts.items())
        ]
        
        # 常见关键词
        all_content = " ".join([q.title + " " + q.content for q in questions])
        keywords = self._extract_keywords(all_content)
        
        # 最近问题
        recent_questions = questions[:10]
        
        return {
            "total_questions": total_questions,
            "pending_questions": pending_questions,
            "answered_questions": answered_questions,
            "resolved_questions": resolved_questions,
            "category_distribution": category_distribution,
            "priority_distribution": priority_distribution,
            "daily_question_count": daily_question_count,
            "common_keywords": keywords,
            "recent_questions": recent_questions
        }

    def _extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """提取关键词"""
        # 简单的关键词提取（可以后续集成更复杂的NLP库）
        # 移除标点符号和数字
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        
        # 分词并过滤停用词
        words = text.lower().split()
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        words = [word for word in words if word not in stop_words and len(word) > 1]
        
        # 统计词频
        word_counts = Counter(words)
        return [{"word": word, "count": count} for word, count in word_counts.most_common(top_n)]

    # 问题总结相关方法
    def generate_question_summary(self, params: QuestionSummaryParams, teacher_id: int) -> QuestionSummary:
        """生成问题总结"""
        # 确定时间范围
        if params.start_date and params.end_date:
            start_date = params.start_date
            end_date = params.end_date
        else:
            end_date = datetime.utcnow()
            if params.summary_type == "daily":
                start_date = end_date - timedelta(days=1)
            elif params.summary_type == "weekly":
                start_date = end_date - timedelta(weeks=1)
            else:  # monthly
                start_date = end_date - timedelta(days=30)
        
        # 获取问题数据
        questions = self.db.query(Question).filter(
            Question.created_at >= start_date,
            Question.created_at <= end_date
        ).all()
        
        # 使用AI服务生成总结
        questions_data = [question.to_dict() for question in questions]
        ai_summary = self.ai_service.generate_question_summary(questions_data)
        
        # 创建总结
        summary = QuestionSummary(
            title=f"{params.summary_type.title()}问题总结 - {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}",
            content=ai_summary["summary_text"],
            summary_type=params.summary_type,
            period_start=start_date,
            period_end=end_date,
            teacher_id=teacher_id,
            question_count=ai_summary["total_questions"],
            resolved_count=ai_summary["resolved_count"],
            pending_count=ai_summary["pending_count"],
            category_stats=json.dumps(ai_summary["category_stats"], ensure_ascii=False),
            common_issues=json.dumps(ai_summary["common_issues"], ensure_ascii=False),
            recommendations=json.dumps(ai_summary["recommendations"], ensure_ascii=False)
        )
        
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        return summary

    def _generate_summary_content(self, questions: List[Question], summary_type: str) -> str:
        """生成总结内容"""
        total_questions = len(questions)
        resolved_questions = len([q for q in questions if q.status == QuestionStatus.RESOLVED])
        pending_questions = len([q for q in questions if q.status == QuestionStatus.PENDING])
        
        content = f"在{summary_type}期间，共收到{total_questions}个问题，其中已解决{resolved_questions}个，待处理{pending_questions}个。\n\n"
        
        if total_questions > 0:
            resolution_rate = (resolved_questions / total_questions) * 100
            content += f"问题解决率为{resolution_rate:.1f}%。\n\n"
        
        # 按分类统计
        category_counts = {}
        for question in questions:
            if question.category:
                category_name = question.category.name
                category_counts[category_name] = category_counts.get(category_name, 0) + 1
        
        if category_counts:
            content += "问题分类分布：\n"
            for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                content += f"- {category}: {count}个问题\n"
        
        return content

    def _identify_common_issues(self, questions: List[Question]) -> List[Dict[str, Any]]:
        """识别常见问题"""
        # 简单的常见问题识别（可以后续集成更复杂的NLP分析）
        issue_patterns = {
            "语法错误": ["语法", "错误", "报错", "SyntaxError"],
            "逻辑问题": ["逻辑", "算法", "思路", "方法"],
            "环境配置": ["环境", "配置", "安装", "设置"],
            "调试问题": ["调试", "bug", "问题", "不工作"],
            "概念理解": ["理解", "概念", "原理", "不懂"]
        }
        
        common_issues = []
        for pattern_name, keywords in issue_patterns.items():
            count = 0
            for question in questions:
                content = (question.title + " " + question.content).lower()
                if any(keyword.lower() in content for keyword in keywords):
                    count += 1
            
            if count > 0:
                common_issues.append({
                    "category": pattern_name,
                    "count": count,
                    "percentage": round((count / len(questions)) * 100, 1) if questions else 0
                })
        
        return sorted(common_issues, key=lambda x: x["count"], reverse=True)

    def _generate_recommendations(self, questions: List[Question], category_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成改进建议"""
        recommendations = []
        
        # 基于解决率的建议
        total_questions = len(questions)
        resolved_questions = len([q for q in questions if q.status == QuestionStatus.RESOLVED])
        
        if total_questions > 0:
            resolution_rate = (resolved_questions / total_questions) * 100
            
            if resolution_rate < 70:
                recommendations.append({
                    "type": "解决率",
                    "title": "提高问题解决率",
                    "description": f"当前解决率为{resolution_rate:.1f}%，建议加强问题跟踪和及时回复。",
                    "priority": "high"
                })
            elif resolution_rate > 90:
                recommendations.append({
                    "type": "解决率",
                    "title": "保持高质量服务",
                    "description": f"当前解决率为{resolution_rate:.1f}%，继续保持良好的问题处理效率。",
                    "priority": "low"
                })
        
        # 基于分类的建议
        for category, stats in category_stats.items():
            if stats["total"] > 5:  # 只对问题数量较多的分类给出建议
                pending_rate = (stats["pending"] / stats["total"]) * 100
                if pending_rate > 30:
                    recommendations.append({
                        "type": "分类管理",
                        "title": f"关注{category}分类",
                        "description": f"{category}分类有{pending_rate:.1f}%的问题待处理，建议优先处理。",
                        "priority": "medium"
                    })
        
        # 基于问题内容的建议
        if total_questions > 10:
            all_content = " ".join([q.title + " " + q.content for q in questions])
            keywords = self._extract_keywords(all_content, 5)
            
            if keywords:
                top_keyword = keywords[0]["word"]
                recommendations.append({
                    "type": "内容分析",
                    "title": "重点关注热门话题",
                    "description": f"'{top_keyword}'是学生最常提到的问题，建议准备相关教学材料。",
                    "priority": "medium"
                })
        
        return recommendations

    def get_summaries(self, teacher_id: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[QuestionSummary]:
        """获取问题总结列表"""
        query = self.db.query(QuestionSummary)
        
        if teacher_id:
            query = query.filter(QuestionSummary.teacher_id == teacher_id)
        
        return query.order_by(desc(QuestionSummary.created_at)).offset(skip).limit(limit).all()

    def get_summary_by_id(self, summary_id: int) -> Optional[QuestionSummary]:
        """根据ID获取问题总结"""
        return self.db.query(QuestionSummary).filter(QuestionSummary.id == summary_id).first()
