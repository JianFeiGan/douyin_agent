# 抖音视频发布自动化智能体 - 系统架构设计

## 1. 系统总体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户层 (User Layer)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Web UI   │  │   REST API │  │  Scheduler  │  │  Webhook    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          服务层 (Service Layer)                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Task Scheduler (任务调度)                    │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐         │   │
│  │  │ 定时发布  │ │ 批量发布  │ │ 队列管理  │ │ 重试机制  │         │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Business Logic (业务逻辑)                      │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐         │   │
│  │  │  内容处理  │ │ 视频生成  │ │ 抖音发布  │ │  数据存储  │         │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          外部集成层 (Integration Layer)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  抖音开放API │  │ Seedance 2.0│  │  TTS 服务   │  │  对象存储   │    │
│  │             │  │  (AI视频生成) │  │ (Azure/阿里) │  │ (OSS/S3)   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. 核心模块设计

### 2.1 模块职责

| 模块 | 职责 | 主要类/函数 |
|------|------|------------|
| **TaskManager** | 任务调度、队列管理 | `TaskScheduler`, `TaskQueue`, `RetryHandler` |
| **ContentProcessor** | 文本处理、内容清洗 | `TextCleaner`, `KeywordExtractor`, `ContentAnalyzer` |
| **VideoGenerator (Seedance)** | 调用 Seedance 2.0 生成视频 | `SeedanceClient`, `VideoGenerator`, `TaskSubmitter` |
| **AudioProcessor** | 音频处理、TTS | `TTSEngine`, `AudioMixer`, `BackgroundMusic` |
| **DouyinAPI** | 抖音开放平台对接 | `DouyinClient`, `AuthManager`, `VideoUploader` |
| **StorageManager** | 文件存储管理 | `LocalStorage`, `OSSStorage`, `CacheManager` |
| **DataStore** | 数据持久化 | `SQLiteDB`, `TaskRepository`, `LogRepository` |

### 2.2 数据流设计

```
用户输入 (文本)
    │
    ▼
┌─────────────────┐
│  ContentProcessor │ ───► 关键词提取 / 内容分析
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  AudioProcessor │ ───► TTS 转换 / 音频处理 (可选)
└─────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  VideoGenerator (Seedance)  │ ───► 调用 Seedance 2.0 API 生成视频
└─────────────────────────────┘
    │
    ▼
┌─────────────────┐
│  StorageManager │ ───► 下载视频到本地 / 上传到 OSS
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   DouyinAPI    │ ───► 上传视频 / 发布到抖音
└─────────────────┘
    │
    ▼
   抖音发布成功
    │
    ▼
┌─────────────────┐
│   DataStore    │ ───► 记录任务状态 / 日志
└─────────────────┘
```

## 3. Seedance 2.0 集成设计

### 3.1 Seedance 2.0 简介

**Seedance (即梦)** 是字节跳动推出的 AI 视频生成工具，提供 API 接口支持：
- 文本到视频生成
- 图片到视频生成
- 视频编辑功能

### 3.2 Seedance API 集成

```python
class SeedanceClient:
    """Seedance 2.0 API 客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.seedance.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
    
    def create_video(self, prompt: str, **options) -> dict:
        """
        创建视频任务
        
        Args:
            prompt: 视频描述文本
            options: 其他参数 (duration, aspect_ratio, etc.)
            
        Returns:
            任务信息 {task_id, status}
        """
        pass
    
    def get_task_status(self, task_id: str) -> dict:
        """
        获取任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务状态 {status, video_url, etc.}
        """
        pass
    
    def download_video(self, video_url: str, output_path: str) -> str:
        """
        下载视频
        
        Args:
            video_url: 视频 URL
            output_path: 保存路径
            
        Returns:
            本地文件路径
        """
        pass
```

### 3.3 Seedance 配置

```yaml
seedance:
  # API 配置
  api_key: "your_seedance_api_key"
  base_url: "https://api.seedance.com/v1"
  
  # 视频生成参数
  default_duration: 5        # 默认视频时长(秒)
  default_aspect: "9:16"     # 默认宽高比 (9:16 竖屏 / 16:9 横屏)
  default_model: "seedance-pro"  # 模型版本
  
  # 任务配置
  poll_interval: 3           # 轮询间隔(秒)
  max_wait_time: 300         # 最大等待时间(秒)
  timeout: 600               # 生成超时(秒)
```

## 4. API 设计

### 4.1 REST API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/tasks` | 创建发布任务 |
| GET | `/api/v1/tasks` | 获取任务列表 |
| GET | `/api/v1/tasks/{id}` | 获取任务详情 |
| DELETE | `/api/v1/tasks/{id}` | 删除任务 |
| POST | `/api/v1/tasks/{id}/execute` | 执行任务 |
| POST | `/api/v1/auth/url` | 获取抖音授权 URL |
| POST | `/api/v1/auth/callback` | 抖音授权回调 |
| GET | `/api/v1/videos` | 获取视频列表 |
| POST | `/api/v1/upload` | 上传视频文件 |

### 4.2 Webhook 事件

| 事件 | 描述 |
|------|------|
| `task.started` | 任务开始 |
| `task.completed` | 任务完成 |
| `task.failed` | 任务失败 |
| `video.published` | 视频发布成功 |
| `douyin.auth_success` | 抖音授权成功 |

## 5. 数据模型设计

### 5.1 Task (任务)

```python
class Task:
    id: str                      # 任务 ID
    content: str                 # 文本内容 (用于生成视频)
    title: str                   # 视频标题
    description: str             # 视频描述
    status: TaskStatus           # 任务状态 (pending/running/completed/failed)
    
    # 视频生成相关
    seedance_task_id: str        # Seedance 任务 ID
    video_path: str              # 生成视频本地路径
    video_url: str               # 视频 OSS URL
    
    # 抖音相关
    douyin_video_id: str         # 抖音视频 ID
    douyin_video_url: str        # 抖音视频链接
    
    # 时间戳
    created_at: datetime         # 创建时间
    scheduled_at: datetime       # 定时发布时间
    completed_at: datetime       # 完成时间
    
    # 错误处理
    error_message: str           # 错误信息
    retry_count: int             # 重试次数
```

## 6. 部署架构

### 6.1 开发/测试环境

```
┌─────────────────────────────────────────┐
│           Docker Compose                 │
│  ┌─────────────────────────────────┐    │
│  │        douyin-agent (Python)    │    │
│  │  - FastAPI + Uvicorn            │    │
│  │  - SQLite (内嵌)                │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### 6.2 生产环境 (推荐)

```
┌─────────────────────────────────────────────────────────────┐
│                         Load Balancer                        │
│                      (Nginx / ALB)                          │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  douyin-agent │      │  douyin-agent │      │  douyin-agent │
│    (Node 1)   │      │    (Node 2)   │      │    (Node 3)   │
└───────────────┘      └───────────────┘      └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                ┌───────────────────────────┐
                │      Redis (队列/缓存)     │
                └───────────────────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │   PostgreSQL (数据库)     │
                └───────────────────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │    OSS (视频存储)         │
                └───────────────────────────┘
```

## 7. 技术选型

| 类别 | 技术 | 理由 |
|------|------|------|
| **Web 框架** | FastAPI | 异步高性能、自动生成 API 文档 |
| **任务队列** | Celery + Redis | 分布式任务处理、支持定时任务 |
| **数据库** | PostgreSQL | 可靠性高、支持复杂查询 |
| **缓存** | Redis | 高性能、支持多种数据结构 |
| **视频生成** | Seedance 2.0 (即梦) | 字节跳动 AI 视频生成工具 |
| **TTS** | Azure TTS / 阿里云 | 效果好、支持多种声音 |
| **存储** | 阿里云 OSS | 国内访问快、费用低 |

## 8. 安全性设计

1. **API 认证** - Token 鉴权 + API Key
2. **敏感信息** - 加密存储 (抖音 App Secret, Seedance API Key)
3. **请求限流** - 防止 API 滥用
4. **抖音 API 调用** - 遵循官方频率限制
5. **Seedance API 调用** - 遵循官方频率限制

## 9. 扩展性设计

1. **插件化** - 视频生成器可插拔 (Seedance / Runway / Pika)
2. **多平台** - 预留快手、视频号、小红书接口
3. **分布式** - 支持多节点部署
4. **监控** - Prometheus + Grafana 指标

---

*文档版本: 1.1*
*最后更新: 2026-02-28*
*更新内容: 新增 Seedance 2.0 视频生成集成设计*
