"""
AI文本分析服务
用于智能分类和总结学生问题
"""
import re
import json
from typing import List, Dict, Any, Tuple
from collections import Counter
from datetime import datetime, timedelta


class AIAnalysisService:
    """AI分析服务类"""
    
    def __init__(self):
        # 问题分类关键词映射
        self.category_keywords = {
            "Python基础": [
                "语法", "语法错误", "缩进", "IndentationError", "SyntaxError", 
                "变量", "数据类型", "字符串", "列表", "字典", "元组",
                "函数", "参数", "返回值", "作用域", "命名空间"
            ],
            "数据结构": [
                "数组", "链表", "栈", "队列", "树", "图", "哈希表",
                "线性表", "非线性", "存储", "查找", "插入", "删除",
                "排序", "搜索", "遍历", "递归"
            ],
            "算法": [
                "算法", "时间复杂度", "空间复杂度", "贪心", "动态规划",
                "分治", "回溯", "排序算法", "查找算法", "图算法",
                "字符串匹配", "最短路径", "最小生成树"
            ],
            "环境配置": [
                "环境", "配置", "安装", "pip", "conda", "虚拟环境",
                "IDE", "编辑器", "调试", "运行", "编译", "解释器",
                "依赖", "包管理", "版本", "兼容性"
            ],
            "面向对象": [
                "类", "对象", "继承", "多态", "封装", "属性", "方法",
                "构造函数", "析构函数", "抽象", "接口", "设计模式"
            ],
            "异常处理": [
                "异常", "错误", "try", "except", "finally", "raise",
                "错误处理", "调试", "日志", "错误信息"
            ]
        }
        
        # 问题优先级关键词
        self.priority_keywords = {
            "high": ["紧急", "急", "卡住", "无法运行", "崩溃", "报错", "错误"],
            "medium": ["问题", "不会", "不懂", "如何", "怎么"],
            "low": ["建议", "优化", "改进", "学习", "心得"]
        }
        
        # 停用词列表
        self.stop_words = {
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", 
            "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", 
            "没有", "看", "好", "自己", "这", "那", "什么", "怎么", "为什么", "如何"
        }

    def analyze_question_content(self, content: str) -> Dict[str, Any]:
        """分析问题内容，返回分类、优先级等信息"""
        content_lower = content.lower()
        
        # 分类分析
        category = self._classify_question(content_lower)
        
        # 优先级分析
        priority = self._analyze_priority(content_lower)
        
        # 关键词提取
        keywords = self._extract_keywords(content)
        
        # 情感分析（简单实现）
        sentiment = self._analyze_sentiment(content)
        
        return {
            "category": category,
            "priority": priority,
            "keywords": keywords,
            "sentiment": sentiment,
            "complexity": self._analyze_complexity(content)
        }

    def _classify_question(self, content: str) -> str:
        """分类问题"""
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in content:
                    score += 1
            category_scores[category] = score
        
        # 返回得分最高的分类
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        return "其他"

    def _analyze_priority(self, content: str) -> str:
        """分析问题优先级"""
        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    return priority
        return "medium"

    def _extract_keywords(self, content: str, top_n: int = 10) -> List[str]:
        """提取关键词"""
        # 移除标点符号和数字
        text = re.sub(r'[^\w\s]', ' ', content)
        text = re.sub(r'\d+', '', text)
        
        # 分词
        words = text.split()
        
        # 过滤停用词和短词
        words = [word for word in words if len(word) > 1 and word not in self.stop_words]
        
        # 统计词频
        word_counts = Counter(words)
        
        return [word for word, count in word_counts.most_common(top_n)]

    def _analyze_sentiment(self, content: str) -> str:
        """简单的情感分析"""
        positive_words = ["好", "棒", "成功", "感谢", "帮助", "解决"]
        negative_words = ["错误", "问题", "失败", "不会", "不懂", "困难", "卡住"]
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _analyze_complexity(self, content: str) -> str:
        """分析问题复杂度"""
        # 简单的复杂度分析
        if len(content) > 200:
            return "high"
        elif len(content) > 100:
            return "medium"
        else:
            return "low"

    def generate_question_summary(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成问题总结"""
        if not questions:
            return self._empty_summary()
        
        # 基础统计
        total_questions = len(questions)
        resolved_count = len([q for q in questions if q.get('status') == 'resolved'])
        pending_count = len([q for q in questions if q.get('status') == 'pending'])
        resolution_rate = (resolved_count / total_questions * 100) if total_questions > 0 else 0
        
        # 分类统计
        category_stats = self._analyze_categories(questions)
        
        # 常见问题识别
        common_issues = self._identify_common_issues(questions)
        
        # 趋势分析
        trend_analysis = self._analyze_trends(questions)
        
        # 生成改进建议
        recommendations = self._generate_recommendations(questions, category_stats, common_issues)
        
        # 生成总结文本
        summary_text = self._generate_summary_text(
            total_questions, resolved_count, pending_count, resolution_rate,
            category_stats, common_issues, recommendations
        )
        
        return {
            "total_questions": total_questions,
            "resolved_count": resolved_count,
            "pending_count": pending_count,
            "resolution_rate": round(resolution_rate, 2),
            "category_stats": category_stats,
            "common_issues": common_issues,
            "trend_analysis": trend_analysis,
            "recommendations": recommendations,
            "summary_text": summary_text
        }

    def _empty_summary(self) -> Dict[str, Any]:
        """空总结"""
        return {
            "total_questions": 0,
            "resolved_count": 0,
            "pending_count": 0,
            "resolution_rate": 0,
            "category_stats": {},
            "common_issues": [],
            "trend_analysis": {},
            "recommendations": [],
            "summary_text": "暂无问题数据"
        }

    def _analyze_categories(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析问题分类"""
        category_counts = {}
        category_resolved = {}
        
        for question in questions:
            category = question.get('category', '其他')
            if category not in category_counts:
                category_counts[category] = 0
                category_resolved[category] = 0
            
            category_counts[category] += 1
            if question.get('status') == 'resolved':
                category_resolved[category] += 1
        
        # 计算每个分类的解决率
        category_stats = {}
        for category, total in category_counts.items():
            resolved = category_resolved.get(category, 0)
            resolution_rate = (resolved / total * 100) if total > 0 else 0
            category_stats[category] = {
                "total": total,
                "resolved": resolved,
                "pending": total - resolved,
                "resolution_rate": round(resolution_rate, 2),
                "percentage": round((total / len(questions) * 100), 2)
            }
        
        return category_stats

    def _identify_common_issues(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """识别常见问题"""
        # 收集所有问题内容
        all_content = " ".join([
            q.get('title', '') + " " + q.get('content', '') 
            for q in questions
        ])
        
        # 提取关键词
        keywords = self._extract_keywords(all_content, 20)
        
        # 根据关键词识别常见问题类型
        issue_patterns = {
            "语法错误": ["语法", "错误", "缩进", "SyntaxError", "IndentationError"],
            "逻辑问题": ["逻辑", "算法", "思路", "方法", "循环", "条件"],
            "环境配置": ["环境", "配置", "安装", "pip", "conda", "IDE"],
            "调试问题": ["调试", "bug", "不工作", "报错", "异常"],
            "概念理解": ["理解", "概念", "原理", "不懂", "不明白"]
        }
        
        common_issues = []
        for issue_type, patterns in issue_patterns.items():
            count = sum(1 for pattern in patterns if pattern in all_content.lower())
            if count > 0:
                percentage = round((count / len(questions)) * 100, 2)
                common_issues.append({
                    "category": issue_type,
                    "count": count,
                    "percentage": percentage,
                    "description": f"学生经常遇到{issue_type}相关的问题"
                })
        
        return sorted(common_issues, key=lambda x: x["count"], reverse=True)

    def _analyze_trends(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析问题趋势"""
        # 按日期分组统计
        daily_counts = {}
        for question in questions:
            created_at = question.get('created_at')
            if created_at:
                date = created_at.split('T')[0] if 'T' in created_at else created_at
                daily_counts[date] = daily_counts.get(date, 0) + 1
        
        if not daily_counts:
            return {"daily_average": 0, "growth_rate": 0, "trend": "stable"}
        
        # 计算平均每日问题数
        total_days = len(daily_counts)
        total_questions = sum(daily_counts.values())
        daily_average = round(total_questions / total_days, 2)
        
        # 简单趋势分析
        dates = sorted(daily_counts.keys())
        if len(dates) >= 2:
            recent_avg = sum(daily_counts[date] for date in dates[-3:]) / min(3, len(dates))
            earlier_avg = sum(daily_counts[date] for date in dates[:3]) / min(3, len(dates))
            growth_rate = round(((recent_avg - earlier_avg) / earlier_avg * 100), 2) if earlier_avg > 0 else 0
        else:
            growth_rate = 0
        
        trend = "increasing" if growth_rate > 10 else "decreasing" if growth_rate < -10 else "stable"
        
        return {
            "daily_average": daily_average,
            "growth_rate": growth_rate,
            "trend": trend,
            "daily_counts": daily_counts
        }

    def _generate_recommendations(self, questions: List[Dict[str, Any]], 
                                category_stats: Dict[str, Any], 
                                common_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成改进建议"""
        recommendations = []
        
        # 基于解决率的建议
        overall_resolution_rate = sum(
            stats["resolution_rate"] for stats in category_stats.values()
        ) / len(category_stats) if category_stats else 0
        
        if overall_resolution_rate < 70:
            recommendations.append({
                "type": "解决率",
                "title": "提高问题解决率",
                "description": f"当前解决率为{overall_resolution_rate:.1f}%，建议加强问题跟踪和及时回复",
                "priority": "high",
                "actions": ["加强问题跟踪", "及时回复学生", "提高回复质量"]
            })
        
        # 基于分类的建议
        for category, stats in category_stats.items():
            if stats["pending"] > 5:  # 待处理问题较多的分类
                pending_rate = (stats["pending"] / stats["total"]) * 100
                recommendations.append({
                    "type": "分类管理",
                    "title": f"关注{category}分类",
                    "description": f"{category}分类有{pending_rate:.1f}%的问题待处理，建议优先处理",
                    "priority": "medium",
                    "actions": [f"优先处理{category}问题", "增加相关教学资源"]
                })
        
        # 基于常见问题的建议
        if common_issues:
            top_issue = common_issues[0]
            recommendations.append({
                "type": "教学内容",
                "title": f"加强{top_issue['category']}教学",
                "description": f"{top_issue['category']}是学生最常遇到的问题类型，建议加强相关教学",
                "priority": "medium",
                "actions": ["增加相关练习", "制作教学视频", "提供更多示例"]
            })
        
        return recommendations

    def _generate_summary_text(self, total_questions: int, resolved_count: int, 
                             pending_count: int, resolution_rate: float,
                             category_stats: Dict[str, Any], 
                             common_issues: List[Dict[str, Any]],
                             recommendations: List[Dict[str, Any]]) -> str:
        """生成总结文本"""
        summary_parts = []
        
        # 基础统计
        summary_parts.append(
            f"本次统计期间共收到{total_questions}个学生问题，"
            f"其中已解决{resolved_count}个，待处理{pending_count}个，"
            f"问题解决率为{resolution_rate:.1f}%。"
        )
        
        # 分类统计
        if category_stats:
            top_category = max(category_stats.items(), key=lambda x: x[1]["total"])
            summary_parts.append(
                f"问题主要集中在{top_category[0]}领域，"
                f"共{top_category[1]['total']}个问题，"
                f"解决率为{top_category[1]['resolution_rate']:.1f}%。"
            )
        
        # 常见问题
        if common_issues:
            top_issue = common_issues[0]
            summary_parts.append(
                f"最常见的问题是{top_issue['category']}，"
                f"占问题总数的{top_issue['percentage']:.1f}%。"
            )
        
        # 改进建议
        if recommendations:
            high_priority_recs = [r for r in recommendations if r["priority"] == "high"]
            if high_priority_recs:
                summary_parts.append(
                    f"建议重点关注：{high_priority_recs[0]['title']}，"
                    f"{high_priority_recs[0]['description']}"
                )
        
        return " ".join(summary_parts)

    def batch_analyze_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量分析问题"""
        analyzed_questions = []
        
        for question in questions:
            content = question.get('title', '') + ' ' + question.get('content', '')
            analysis = self.analyze_question_content(content)
            
            analyzed_question = question.copy()
            analyzed_question.update({
                'ai_category': analysis['category'],
                'ai_priority': analysis['priority'],
                'ai_keywords': analysis['keywords'],
                'ai_sentiment': analysis['sentiment'],
                'ai_complexity': analysis['complexity']
            })
            
            analyzed_questions.append(analyzed_question)
        
        return analyzed_questions
