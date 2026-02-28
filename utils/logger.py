"""
日志配置
"""
from loguru import logger
import yaml
from pathlib import Path


def setup_logger(config_path: str = "config.yaml"):
    """配置日志"""
    # 读取配置
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        log_config = config.get('log', {})
        level = log_config.get('level', 'INFO')
        format_str = log_config.get('format')
        rotation = log_config.get('rotation', '100 MB')
        retention = log_config.get('retention', '7 days')
    else:
        level = 'INFO'
        format_str = None
        rotation = '100 MB'
        retention = '7 days'
    
    # 移除默认处理器
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sink=lambda msg: print(msg),
        format=format_str,
        level=level,
        colorize=True
    )
    
    # 添加文件输出
    logger.add(
        sink="logs/douyin_agent.log",
        format=format_str,
        level=level,
        rotation=rotation,
        retention=retention,
        encoding='utf-8'
    )
    
    return logger
