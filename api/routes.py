"""
API 路由
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import tempfile
import shutil

from core import VideoGenerator, DouyinPublisher

router = APIRouter()

# 初始化
video_generator = VideoGenerator()
douyin_publisher = DouyinPublisher()


class GenerateVideoRequest(BaseModel):
    """生成视频请求"""
    text: str
    title: str
    description: Optional[str] = ""


class PublishVideoRequest(BaseModel):
    """发布视频请求"""
    video_path: str
    title: str
    description: Optional[str] = ""


@router.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "message": "Douyin Agent API"}


@router.post("/generate")
async def generate_video(request: GenerateVideoRequest):
    """生成视频"""
    try:
        output_name = f"{request.title}.mp4"
        video_path = video_generator.generate(request.text, output_name)
        return {
            "status": "success",
            "video_path": video_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/publish")
async def publish_video(request: PublishVideoRequest):
    """发布视频到抖音"""
    try:
        result = douyin_publisher.upload_video(
            request.video_path,
            request.title,
            request.description
        )
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """上传视频文件"""
    try:
        # 保存上传的文件
        save_dir = Path("./uploads")
        save_dir.mkdir(parents=True, exist_ok=True)
        
        save_path = save_dir / file.filename
        
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "file_path": str(save_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/auth/url")
async def get_auth_url():
    """获取抖音授权 URL"""
    url = douyin_publisher.get_authorization_url()
    return {"auth_url": url}
