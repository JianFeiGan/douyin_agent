"""
任务数据模型
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """任务"""
    id: str
    content: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    video_path: Optional[str] = None
    douyin_video_id: Optional[str] = None
    douyin_video_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'video_path': self.video_path,
            'douyin_video_id': self.douyin_video_id,
            'douyin_video_url': self.douyin_video_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """从字典创建"""
        return cls(
            id=data['id'],
            content=data['content'],
            title=data['title'],
            description=data.get('description', ''),
            status=TaskStatus(data.get('status', 'pending')),
            video_path=data.get('video_path'),
            douyin_video_id=data.get('douyin_video_id'),
            douyin_video_url=data.get('douyin_video_url'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            scheduled_at=datetime.fromisoformat(data['scheduled_at']) if data.get('scheduled_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            error_message=data.get('error_message'),
            retry_count=data.get('retry_count', 0),
            max_retries=data.get('max_retries', 3),
        )
