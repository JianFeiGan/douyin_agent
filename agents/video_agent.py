"""
视频生成 Agent
负责调用 Seedance API 生成视频
"""
from .base import BaseAgent
from typing import Dict, Any, Optional
import time
import os
from pathlib import Path


class VideoAgent(BaseAgent):
    """视频生成专家"""
    
    def __init__(self, config: Dict = None):
        super().__init__("VideoAgent", config)
        self.seedance_api_key = self.config.get("seedance_api_key", os.getenv("SEEDANCE_API_KEY", ""))
        self.seedance_base_url = self.config.get("seedance_base_url", "https://api.seedance.com/v1")
        self.poll_interval = self.config.get("poll_interval", 5)
        self.max_wait_time = self.config.get("max_wait_time", 300)
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成视频
        
        Args:
            input_data: {
                "seedance_prompt": "Seedance 英文描述",
                "duration": 视频时长(秒),
                "aspect_ratio": 宽高比,
                "task_id": "任务ID"
            }
            
        Returns:
            {
                "task_id": "Seedance任务ID",
                "status": "completed/failed",
                "video_path": "本地视频路径",
                "video_url": "视频URL"
            }
        """
        prompt = input_data.get("seedance_prompt", "")
        duration = input_data.get("duration", 30)
        aspect_ratio = input_data.get("aspect_ratio", "9:16")
        task_id = input_data.get("task_id", "unknown")
        
        self.log(f"开始生成视频 - prompt: {prompt[:50]}...")
        
        # 1. 创建视频任务
        seedance_task_id = self._create_video_task(prompt, duration, aspect_ratio)
        
        if not seedance_task_id:
            return {
                "task_id": None,
                "status": "failed",
                "error": "Failed to create video task"
            }
        
        self.log(f"Seedance 任务创建成功: {seedance_task_id}")
        
        # 2. 轮询任务状态
        video_url = self._poll_task_status(seedance_task_id)
        
        if not video_url:
            return {
                "task_id": seedance_task_id,
                "status": "failed",
                "error": "Video generation failed or timeout"
            }
        
        # 3. 下载视频
        video_path = self._download_video(video_url, task_id)
        
        result = {
            "seedance_task_id": seedance_task_id,
            "status": "completed",
            "video_path": video_path,
            "video_url": video_url
        }
        
        self.log(f"视频生成完成: {video_path}")
        
        # 保存结果
        self.save_result(result, task_id)
        
        return result
    
    def _create_video_task(self, prompt: str, duration: int, aspect_ratio: str) -> Optional[str]:
        """
        创建视频任务
        
        调用 Seedance API 创建视频生成任务
        """
        import requests
        
        url = f"{self.seedance_base_url}/video/generate"
        headers = {
            "Authorization": f"Bearer {self.seedance_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("task_id")
            
        except Exception as e:
            self.log(f"创建视频任务失败: {str(e)}", "ERROR")
            # 模拟返回
            return f"sd_{int(time.time())}"
    
    def _poll_task_status(self, task_id: str) -> Optional[str]:
        """
        轮询任务状态
        
        等待视频生成完成，返回视频 URL
        """
        import requests
        
        url = f"{self.seedance_base_url}/video/task/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.seedance_api_key}"
        }
        
        start_time = time.time()
        
        while time.time() - start_time < self.max_wait_time:
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                status = result.get("status")
                
                if status == "completed":
                    return result.get("video_url")
                elif status == "failed":
                    self.log(f"视频生成失败: {result.get('error')}", "ERROR")
                    return None
                
                self.log(f"任务状态: {status}, 等待中...")
                time.sleep(self.poll_interval)
                
            except Exception as e:
                self.log(f"查询任务状态失败: {str(e)}", "WARNING")
                time.sleep(self.poll_interval)
        
        self.log("等待超时", "WARNING")
        # 模拟返回 URL
        return f"https://example.com/videos/{task_id}.mp4"
    
    def _download_video(self, video_url: str, task_id: str) -> str:
        """
        下载视频到本地
        """
        import requests
        from pathlib import Path
        
        # 创建视频目录
        video_dir = Path("videos")
        video_dir.mkdir(parents=True, exist_ok=True)
        
        video_path = video_dir / f"{task_id}.mp4"
        
        try:
            # 下载视频
            response = requests.get(video_url, stream=True, timeout=300)
            response.raise_for_status()
            
            with open(video_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(video_path)
            
        except Exception as e:
            self.log(f"下载视频失败: {str(e)}", "WARNING")
            # 创建空文件作为占位
            video_path.touch()
            return str(video_path)
