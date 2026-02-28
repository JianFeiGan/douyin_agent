"""
OpenClaw Handler
将抖音智能体接入 OpenClaw
"""
import sys
import os
import json
import subprocess
from pathlib import Path

# 添加路径
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from agents.coordinator import AgentCoordinator


class DouyinOpenClawHandler:
    """OpenClaw 处理器"""
    
    def __init__(self):
        self.coordinator = AgentCoordinator()
    
    def handle(self, user_message: str) -> str:
        """处理用户消息"""
        message = user_message.strip()
        
        # 解析命令
        if message.startswith("/create ") or "帮我做" in message:
            return self._handle_create(message)
        elif message.startswith("/status "):
            return self._handle_status(message)
        elif message == "/list":
            return self._handle_list(message)
        elif message == "/help":
            return self._handle_help()
        else:
            return self._handle_create(message)
    
    def _handle_create(self, message: str) -> str:
        """处理创建任务"""
        # 提取文本内容
        text = message.replace("/create", "").strip()
        text = text.replace("帮我做", "").replace("做个", "").replace("视频", "").strip()
        
        if not text:
            return "请提供视频内容，例如：/create 帮我做一个AI科普视频"
        
        # 提取标题（可选）
        title = None
        if "--title" in message:
            parts = message.split("--title")
            if len(parts) > 1:
                title = parts[1].strip()
        
        # 执行
        try:
            result = self.coordinator.run(
                user_input=text,
                title=title
            )
            
            if result.get("success"):
                video_url = result.get("publish", {}).get("video_url", "未知")
                task_id = result.get("task_id", "")
                return f"""✅ 视频发布成功！

任务ID: {task_id}
视频链接: {video_url}

可通过 /status {task_id} 查看详情"""
            else:
                error = result.get("error", "未知错误")
                return f"❌ 发布失败: {error}"
                
        except Exception as e:
            return f"❌ 执行错误: {str(e)}"
    
    def _handle_status(self, message: str) -> str:
        """处理状态查询"""
        parts = message.split()
        if len(parts) < 2:
            return "请提供任务ID，例如：/status task_xxx"
        
        task_id = parts[1]
        result = self.coordinator.get_status(task_id)
        
        if not result:
            return f"未找到任务: {task_id}"
        
        success = result.get("success", False)
        created_at = result.get("created_at", "未知")
        
        status_text = "✅ 成功" if success else "❌ 失败"
        
        info = f"""📋 任务状态: {status_text}
任务ID: {task_id}
创建时间: {created_at}
"""
        
        if result.get("publish"):
            info += f"视频链接: {result['publish'].get('video_url', '未知')}"
        
        return info
    
    def _handle_list(self, message: str) -> str:
        """处理列表查询"""
        tasks = self.coordinator.list_tasks()
        
        if not tasks:
            return "暂无任务记录"
        
        return f"共有 {len(tasks)} 个任务:\n" + "\n".join([f"- {t}" for t in tasks[:10]])
    
    def _handle_help(self) -> str:
        """帮助信息"""
        return """📖 抖音视频发布智能体

命令:
  /create [内容]     - 创建视频任务
  /status [任务ID]   - 查看任务状态
  /list             - 列出所有任务
  /help             - 显示帮助

示例:
  /create 帮我做一个AI科普视频
  /create 做美食视频 --title 美味佳肴
  /status task_20260228_001"""


# OpenClaw 集成函数
def douyin_handler(user_message: str) -> str:
    """OpenClaw 调用的主函数"""
    handler = DouyinOpenClawHandler()
    return handler.handle(user_message)


if __name__ == "__main__":
    # 测试
    if len(sys.argv) > 1:
        print(douyin_handler(" ".join(sys.argv[1:])))
    else:
        print(douyin_handler("/help"))
