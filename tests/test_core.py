"""
核心模块测试
"""
import pytest
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.video_generator import VideoGenerator
from core.douyin_publisher import DouyinPublisher


class TestVideoGenerator:
    """视频生成器测试"""
    
    def test_init(self):
        """测试初始化"""
        generator = VideoGenerator()
        assert generator is not None
        assert generator.output_dir.exists()


class TestDouyinPublisher:
    """抖音发布器测试"""
    
    def test_init(self):
        """测试初始化"""
        publisher = DouyinPublisher()
        assert publisher is not None
        assert publisher.app_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
