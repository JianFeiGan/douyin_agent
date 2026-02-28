"""
存储管理器 - 本地存储、OSS存储
"""
from pathlib import Path
from typing import Optional
import shutil


class StorageManager:
    """存储管理器"""
    
    def __init__(self, storage_type: str = "local", config: Optional[dict] = None):
        self.storage_type = storage_type
        self.config = config or {}
        self.local_path = Path(self.config.get('local_path', './uploads'))
        self.local_path.mkdir(parents=True, exist_ok=True)
    
    def save_local(self, file_path: str, dest_name: Optional[str] = None) -> str:
        """
        保存到本地
        
        Args:
            file_path: 源文件路径
            dest_name: 目标文件名
            
        Returns:
            保存后的文件路径
        """
        source = Path(file_path)
        if not source.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        dest_name = dest_name or source.name
        dest = self.local_path / dest_name
        
        shutil.copy2(source, dest)
        return str(dest)
    
    def save_oss(self, file_path: str, remote_path: str) -> str:
        """
        保存到 OSS
        
        Args:
            file_path: 本地文件路径
            remote_path: 远程路径
            
        Returns:
            OSS URL
        """
        # TODO: 实现 OSS 上传
        pass
    
    def upload(self, file_path: str, remote_path: Optional[str] = None) -> str:
        """
        上传文件（自动选择存储类型）
        
        Args:
            file_path: 文件路径
            remote_path: 远程路径
            
        Returns:
            文件访问 URL
        """
        if self.storage_type == "oss":
            return self.save_oss(file_path, remote_path or "")
        else:
            return self.save_local(file_path, remote_path)
    
    def delete(self, file_path: str) -> bool:
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否删除成功
        """
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def get_url(self, file_path: str) -> str:
        """
        获取文件访问 URL
        
        Args:
            file_path: 文件路径
            
        Returns:
            访问 URL
        """
        if self.storage_type == "oss":
            # TODO: 返回 OSS URL
            pass
        else:
            return f"file://{file_path}"
