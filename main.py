"""
抖音视频发布自动化智能体 - 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api import router
from utils import setup_logger

# 初始化日志
logger = setup_logger()

# 创建 FastAPI 应用
app = FastAPI(
    title="Douyin Agent API",
    description="抖音视频发布自动化智能体 API",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["Douyin Agent"])


@app.on_event("startup")
async def startup_event():
    """启动事件"""
    logger.info("Douyin Agent 启动中...")


@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    logger.info("Douyin Agent 关闭中...")


if __name__ == "__main__":
    import yaml
    from pathlib import Path
    
    # 读取配置
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        server_config = config.get('server', {})
        host = server_config.get('host', '0.0.0.0')
        port = server_config.get('port', 8080)
        reload = server_config.get('reload', True)
    else:
        host = '0.0.0.0'
        port = 8080
        reload = True
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
