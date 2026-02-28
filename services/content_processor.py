"""
内容处理器 - 文本处理、内容清洗、关键词提取
"""
import re
from typing import Dict, List, Optional


class ContentProcessor:
    """内容处理器"""
    
    def __init__(self):
        self.stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人'])
    
    def clean_text(self, text: str) -> str:
        """
        清洗文本
        
        Args:
            text: 原始文本
            
        Returns:
            清洗后的文本
        """
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        return text.strip()
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        提取关键词
        
        Args:
            text: 文本内容
            top_n: 返回前 n 个关键词
            
        Returns:
            关键词列表
        """
        words = text.split()
        # 简单实现：过滤停用词，返回高频词
        filtered = [w for w in words if w not in self.stop_words]
        return filtered[:top_n]
    
    def analyze_content(self, text: str) -> Dict[str, any]:
        """
        分析内容
        
        Args:
            text: 文本内容
            
        Returns:
            分析结果
        """
        return {
            'length': len(text),
            'word_count': len(text.split()),
            'keywords': self.extract_keywords(text),
            'cleaned_text': self.clean_text(text)
        }
    
    def split_to_sentences(self, text: str) -> List[str]:
        """将文本拆分为句子"""
        return re.split(r'[。！？\n]', text)
