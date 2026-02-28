"""
内容理解 Agent
负责分析文本内容，提取关键信息
"""
from .base import BaseAgent
from typing import Dict, Any, List
import re


class ContentAgent(BaseAgent):
    """内容分析专家"""
    
    def __init__(self, config: Dict = None):
        super().__init__("ContentAgent", config)
        self.stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '这', '那', '个', '一', '也', '都'])
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析文本内容
        
        Args:
            input_data: {
                "text": "用户输入的文本内容",
                "task_id": "任务ID"
            }
            
        Returns:
            {
                "keywords": ["关键词1", "关键词2"],
                "content_summary": "内容摘要",
                "suggested_style": "建议风格",
                "suggested_duration": 建议时长,
                "title_suggestion": "标题建议"
            }
        """
        text = input_data.get("text", "")
        task_id = input_data.get("task_id", "unknown")
        
        self.log(f"开始分析文本: {text[:50]}...")
        
        # 1. 提取关键词
        keywords = self._extract_keywords(text)
        
        # 2. 生成内容摘要
        summary = self._generate_summary(text)
        
        # 3. 分析风格
        style = self._analyze_style(text)
        
        # 4. 建议时长
        duration = self._estimate_duration(text)
        
        # 5. 生成标题建议
        title = self._generate_title(keywords, text)
        
        result = {
            "keywords": keywords,
            "content_summary": summary,
            "suggested_style": style,
            "suggested_duration": duration,
            "title_suggestion": title
        }
        
        self.log(f"分析完成 - 关键词: {keywords}")
        
        # 保存结果
        self.save_result(result, task_id)
        
        return result
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单分词
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
        
        # 过滤停用词和单字
        keywords = [w for w in words if w not in self.stop_words and len(w) > 1]
        
        # 返回前5个关键词
        return list(set(keywords))[:5]
    
    def _generate_summary(self, text: str) -> str:
        """生成内容摘要"""
        # 取前100字作为摘要
        if len(text) > 100:
            return text[:100] + "..."
        return text
    
    def _analyze_style(self, text: str) -> str:
        """分析内容风格"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['ai', '人工智能', '技术', '科技', '代码', '编程']):
            return "科技感"
        elif any(word in text_lower for word in ['美食', '做菜', '烹饪', '好吃']):
            return "美食"
        elif any(word in text_lower for word in ['旅游', '旅行', '风景', '美景']):
            return "风景"
        elif any(word in text_lower for word in ['搞笑', '有趣', '段子', '幽默']):
            return "搞笑"
        elif any(word in text_lower for word in ['知识', '科普', '学习', '教程']):
            return "教育"
        else:
            return "通用"
    
    def _estimate_duration(self, text: str) -> int:
        """估算建议时长"""
        text_length = len(text)
        
        if text_length < 50:
            return 15
        elif text_length < 150:
            return 30
        elif text_length < 300:
            return 45
        else:
            return 60
    
    def _generate_title(self, keywords: List[str], text: str) -> str:
        """生成标题建议"""
        if keywords:
            # 使用第一个关键词生成标题
            return f"{keywords[0]}的奥秘"
        else:
            # 从文本中取前8个字
            return text[:8] if len(text) >= 8 else text
