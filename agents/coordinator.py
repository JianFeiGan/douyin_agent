"""
智能体协调器
负责协调各个 Agent 完成视频发布任务
"""
from .content_agent import ContentAgent
from .animation_agent import AnimationAgent
from .video_agent import VideoAgent
from .publish_agent import PublishAgent
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
import json
from pathlib import Path


class AgentCoordinator:
    """多智能体协调器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.task_id = None
        
        # 初始化各个 Agent
        self.content_agent = ContentAgent(config)
        self.animation_agent = AnimationAgent(config)
        self.video_agent = VideoAgent(config)
        self.publish_agent = PublishAgent(config)
    
    def run(self, user_input: str, title: str = None, description: str = None) -> Dict[str, Any]:
        """
        执行完整的视频发布流程
        
        Args:
            user_input: 用户输入的文本内容
            title: 视频标题
            description: 视频描述
            
        Returns:
            最终结果
        """
        # 生成任务 ID
        self.task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        print(f"\n{'='*50}")
        print(f"开始执行任务: {self.task_id}")
        print(f"{'='*50}\n")
        
        # 步骤 1: 内容分析
        print("[1/4] 启动 Content Agent...")
        content_result = self.content_agent.run({
            "text": user_input,
            "task_id": self.task_id
        })
        
        title = title or content_result.get("title_suggestion", "新视频")
        duration = content_result.get("suggested_duration", 30)
        style = content_result.get("suggested_style", "通用")
        
        print(f"  ✓ 内容分析完成 - 关键词: {content_result.get('keywords')}")
        
        # 步骤 2: 动画优化
        print("\n[2/4] 启动 Animation Agent...")
        animation_result = self.animation_agent.run({
            "content": user_input,
            "keywords": content_result.get("keywords", []),
            "style": style,
            "task_id": self.task_id
        })
        
        seedance_prompt = animation_result.get("seedance_prompt")
        
        print(f"  ✓ 动画优化完成 - 场景数: {len(animation_result.get('scenes', []))}")
        
        # 步骤 3: 视频生成
        print("\n[3/4] 启动 Video Agent...")
        video_result = self.video_agent.run({
            "seedance_prompt": seedance_prompt,
            "duration": duration,
            "aspect_ratio": "9:16",
            "task_id": self.task_id
        })
        
        if video_result.get("status") != "completed":
            return {
                "success": False,
                "task_id": self.task_id,
                "error": "视频生成失败",
                "details": video_result
            }
        
        video_path = video_result.get("video_path")
        
        print(f"  ✓ 视频生成完成: {video_path}")
        
        # 步骤 4: 发布到抖音
        print("\n[4/4] 启动 Publish Agent...")
        publish_result = self.publish_agent.run({
            "video_path": video_path,
            "title": title,
            "description": description or "",
            "task_id": self.task_id
        })
        
        if publish_result.get("status") != "published":
            return {
                "success": False,
                "task_id": self.task_id,
                "error": "视频发布失败",
                "video_path": video_path,
                "details": publish_result
            }
        
        print(f"  ✓ 视频发布成功: {publish_result.get('video_url')}")
        
        # 保存最终结果
        final_result = {
            "success": True,
            "task_id": self.task_id,
            "content_analysis": content_result,
            "animation": animation_result,
            "video": video_result,
            "publish": publish_result,
            "created_at": datetime.now().isoformat()
        }
        
        self._save_task_result(final_result)
        
        print(f"\n{'='*50}")
        print(f"任务完成!")
        print(f"{'='*50}\n")
        
        return final_result
    
    def get_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        task_file = Path(f"tasks/{task_id}/task_result.json")
        
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def list_tasks(self) -> list:
        """列出所有任务"""
        tasks_dir = Path("tasks")
        
        if not tasks_dir.exists():
            return []
        
        tasks = []
        for task_path in tasks_dir.iterdir():
            if task_path.is_dir():
                tasks.append(task_path.name)
        
        return sorted(tasks, reverse=True)
    
    def _save_task_result(self, result: Dict[str, Any]):
        """保存任务结果"""
        task_id = result.get("task_id")
        
        task_dir = Path(f"tasks/{task_id}")
        task_dir.mkdir(parents=True, exist_ok=True)
        
        result_file = task_dir / "task_result.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
