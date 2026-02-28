"""
基础 Agent 类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
from datetime import datetime


class BaseAgent(ABC):
    """所有 Agent 的基类"""
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.history = []
    
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 Agent 任务
        
        Args:
            input_data: 输入数据
            
        Returns:
            输出结果
        """
        pass
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "agent": self.name,
            "level": level,
            "message": message
        }
        self.history.append(log_entry)
        print(f"[{timestamp}] [{self.name}] {message}")
    
    def get_history(self) -> list:
        """获取执行历史"""
        return self.history
    
    def clear_history(self):
        """清空历史"""
        self.history = []
    
    def save_result(self, result: Dict[str, Any], task_id: str):
        """保存结果到文件"""
        import os
        from pathlib import Path
        
        task_dir = Path(f"tasks/{task_id}")
        task_dir.mkdir(parents=True, exist_ok=True)
        
        result_file = task_dir / f"{self.name}_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return str(result_file)
