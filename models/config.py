"""
应用配置模型
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DouyinConfig:
    """抖音配置"""
    app_id: str = ""
    app_secret: str = ""
    api_base_url: str = "https://open.douyin.com"
    redirect_uri: str = "http://localhost:8080/callback"
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


@dataclass
class VideoConfig:
    """视频配置"""
    output_dir: str = "./output"
    width: int = 720
    height: int = 1280
    fps: int = 30
    duration: int = 60


@dataclass
class TTSConfig:
    """TTS配置"""
    provider: str = "azure"  # azure, aliyun, baidu
    voice: str = "zh-CN-XiaoxiaoNeural"
    speed: int = 1.0
    volume: float = 1.0


@dataclass
class StorageConfig:
    """存储配置"""
    type: str = "local"  # local, oss
    local_path: str = "./uploads"
    oss_endpoint: str = ""
    oss_bucket: str = ""
    oss_access_key: str = ""
    oss_secret_key: str = ""


@dataclass
class LogConfig:
    """日志配置"""
    level: str = "INFO"
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    rotation: str = "100 MB"
    retention: str = "7 days"


@dataclass
class ServerConfig:
    """服务配置"""
    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = True


@dataclass
class AppConfig:
    """应用配置"""
    douyin: DouyinConfig = field(default_factory=DouyinConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    log: LogConfig = field(default_factory=LogConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AppConfig':
        """从字典创建"""
        return cls(
            douyin=DouyinConfig(**data.get('douyin', {})),
            video=VideoConfig(**data.get('video', {})),
            tts=TTSConfig(**data.get('tts', {})),
            storage=StorageConfig(**data.get('storage', {})),
            log=LogConfig(**data.get('log', {})),
            server=ServerConfig(**data.get('server', {})),
        )
