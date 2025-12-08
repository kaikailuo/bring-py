"""
学情分析
"""
from typing import List
from app.services.ai.client import call_llm
from app.services.ai.prompts import build_post_summary_prompt
from app.utils.database import SessionLocal
from app.models.post import Post
from app.models.comment import Comment
