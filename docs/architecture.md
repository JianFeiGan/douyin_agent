# 抖音视频发布自动化智能体 - 基于 OpenClaw 多智能体架构设计

## 1. 设计理念

### 1.1 核心思想

**以 OpenClaw 为核心调度系统，Claude Code 作为编程助手，多智能体协同完成自动化任务。**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           OpenClaw (主控 Agent)                          │
│                    所有任务的入口、调度器和协调者                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│  内容理解 Agent   │   │  视频生成 Agent   │   │  发布 Agent       │
│  - 分析文本      │   │  - 调用 Seedance │   │  - 抖音 API 对接  │
│  - 提取关键信息  │   │  - 监控生成状态   │   │  - 视频上传      │
└───────────────────┘   └───────────────────┘   └───────────────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    ▼
                    ┌───────────────────────────┐
                    │   Claude Code (编程助手)   │
                    │   - 开发新功能脚本          │
                    │   - 调试和问题排查          │
                    │   - 代码优化                │
                    └───────────────────────────┘
```

### 1.2 OpenClaw 能力

| 能力 | 说明 |
|------|------|
| **多会话管理** | 同时管理多个任务会话 |
| **子智能体** | spawn sub-agents 并行处理任务 |
| **消息路由** | 支持多种渠道 (Feishu, Discord, etc.) |
| **心跳检测** | 定时检查任务状态 |
| **文件系统** | 读写本地文件 |
| **执行命令** | 运行 shell 命令 |
| **浏览器控制** | 自动化 Web 操作 |

## 2. 系统架构

### 2.1 整体架构

```
                              用户 (Feishu/终端)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         OpenClaw Gateway                                 │
│                    (消息路由、认证、会话管理)                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      OpenClaw Main Agent                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     任务理解与分解                               │    │
│  │  1. 解析用户意图                                                │    │
│  │  2. 拆分为子任务                                                │    │
│  │  3. 分配给子 Agents                                             │    │
│  │  4. 汇总结果                                                    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│  Content Agent    │   │  Video Agent     │   │  Publish Agent    │
│  (内容处理)        │   │  (视频生成)        │   │  (抖音发布)        │
│                   │   │                   │   │                   │
│ - 文本分析        │   │ - Seedance API   │   │ - 抖音开放平台    │
│ - 关键词提取      │   │ - 任务状态监控    │   │ - 视频上传        │
│ - 摘要生成        │   │ - 视频下载        │   │ - 发布管理        │
└───────────────────┘   └───────────────────┘   └───────────────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │    Claude Code            │
                    │    (编程助手)              │
                    │                           │
                    │  - 生成新脚本             │
                    │  - 调试代码               │
                    │  - 优化实现               │
                    └───────────────────────────┘
```

### 2.2 智能体职责

| 智能体 | 职责 | 工具/能力 |
|--------|------|----------|
| **Main Agent** | 任务协调、结果汇总 | message, sessions_spawn, memory |
| **Content Agent** | 文本处理、内容理解 | 读取文件、分析文本、提取信息 |
| **Video Agent** | 视频生成任务 | API 调用、状态轮询、文件下载 |
| **Publish Agent** | 抖音发布 | API 调用、授权管理、上传发布 |
| **Coding Agent** | 代码开发 | Claude Code CLI、代写脚本 |

## 3. 任务流程

### 3.1 完整流程示例

```
用户: "帮我发布一个抖音视频，内容是关于AI技术的科普"

Main Agent
    │
    ├─► 1. 理解任务
    │       "用户需要一个AI科普视频，需要生成并发布到抖音"
    │
    ├─► 2. 启动 Content Agent
    │       "分析这段文本，提取关键信息：{text}"
    │   
    │   ← Content Agent 返回:
    │       - 关键词: AI, 技术, 科普
    │       - 时长建议: 30秒
    │       - 风格: 科技感
    │
    ├─► 3. 启动 Video Agent
    │       "调用 Seedance 生成视频: {prompt}"
    │
    │   ← Video Agent 返回:
    │       - 任务ID: sd_xxx
    │       - 状态: completed
    │       - 视频路径: ./videos/xxx.mp4
    │
    ├─► 4. 启动 Publish Agent
    │       "发布视频到抖音: {video_path}, {title}"
    │
    │   ← Publish Agent 返回:
    │       - 抖音视频ID: 738xxx
    │       - 视频链接: https://douyin.com/video/738xxx
    │
    └─► 5. 汇总结果
            "✅ 视频发布成功！\n链接: https://douyin.com/video/738xxx"
```

### 3.2 多任务并行

```
用户: "帮我生成3个不同主题的视频"

Main Agent
    │
    ├─► Spawn Video Agent 1 (主题: 美食)
    ├─► Spawn Video Agent 2 (主题: 旅游)  
    ├─► Spawn Video Agent 3 (主题: 科技)
    │
    ├─► 等待所有 Agent 完成
    │
    └─► 汇总结果
        "✅ 3个视频全部生成完成！"
```

## 4. 技术实现

### 4.1 OpenClaw 配置

```yaml
# openclaw.yaml
agents:
  main:
    role: coordinator
    capabilities:
      - message
      - sessions_spawn
      - memory
  
  content:
    role: subagent
    prompt: "你是一个内容分析专家..."
  
  video:
    role: subagent
    prompt: "你负责调用 Seedance API 生成视频..."
  
  publish:
    role: subagent
    prompt: "你负责发布视频到抖音..."

channels:
  - feishu
  - terminal
```

### 4.2 子智能体调用

```python
# Main Agent 中调用子智能体
from sessions_spawn import sessions_spawn

# 启动内容分析子任务
content_result = sessions_spawn(
    task="分析以下文本: {user_text}",
    label="content-agent",
    runtime="subagent"
)

# 启动视频生成子任务
video_result = sessions_spawn(
    task="调用 Seedance API 生成视频: {prompt}",
    label="video-agent", 
    runtime="subagent"
)
```

### 4.3 Claude Code 集成

```bash
# 开发新功能脚本
claude -p "创建一个调用 Seedance API 的 Python 脚本..."

# 调试问题
claude -p "帮我调试这个错误: {error_log}"

# 代码优化
claude -p "优化这段代码的性能: {code}"
```

## 5. 消息/指令格式

### 5.1 用户指令

| 指令 | 说明 | 示例 |
|------|------|------|
| `/create` | 创建视频任务 | `/create 帮我做一个AI科普视频` |
| `/publish` | 发布到抖音 | `/publish video.mp4` |
| `/status` | 查看任务状态 | `/status task_123` |
| `/list` | 列出所有任务 | `/list` |
| `/help` | 帮助信息 | `/help` |

### 5.2 任务状态

| 状态 | 说明 |
|------|------|
| pending | 等待处理 |
| analyzing | 内容分析中 |
| generating | 视频生成中 |
| uploading | 上传抖音中 |
| published | 发布成功 |
| failed | 失败 |

## 6. 存储设计

### 6.1 本地存储结构

```
douyin_agent/
├── .openclaw/              # OpenClaw 配置
│   └── config.yaml
├── tasks/                  # 任务记录
│   └── YYYY-MM-DD/
│       └── task_xxx.json
├── videos/                 # 生成的视频
│   └── task_xxx.mp4
├── scripts/                # Claude Code 生成的脚本
│   ├── seedance_api.py
│   ├── douyin_api.py
│   └── utils/
└── logs/                   # 日志
    └── douyin_agent.log
```

### 6.2 任务数据

```json
{
  "id": "task_20260228_001",
  "user_input": "帮我做一个AI科普视频",
  "status": "published",
  "content_analysis": {
    "keywords": ["AI", "技术", "科普"],
    "style": "科技感"
  },
  "video": {
    "seedance_task_id": "sd_xxx",
    "local_path": "videos/task_xxx.mp4"
  },
  "douyin": {
    "video_id": "738xxx",
    "video_url": "https://douyin.com/video/738xxx"
  },
  "created_at": "2026-02-28T21:40:00Z"
}
```

## 7. 部署方式

### 7.1 开发模式

```
OpenClaw (本地运行)
    │
    └── Gateway: localhost:8080
            │
            └── Main Agent (当前会话)
                    │
                    ├── Content Agent (sub-agent)
                    ├── Video Agent (sub-agent)
                    └── Publish Agent (sub-agent)
```

### 7.2 生产模式

```
                           用户 (Feishu/Telegram)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                     │
│                   (云服务器/Docker)                       │
└─────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │ Main Agent│   │Main Agent │   │Main Agent │
            │  (Node 1) │   │ (Node 2)  │   │ (Node 3)  │
            └───────────┘   └───────────┘   └───────────┘
```

## 8. 扩展性

### 8.1 新增智能体

```python
# 扩展新的 Agent
@agent(name="music")
class MusicAgent:
    """音乐生成 Agent"""
    
    def run(self, task):
        # 调用音乐生成 API
        pass
```

### 8.2 新增平台

- 小红书发布 Agent
- 快手发布 Agent
- B站发布 Agent
- YouTube 发布 Agent

---

*文档版本: 2.0*
*最后更新: 2026-02-28*
*设计理念: 基于 OpenClaw 多智能体架构 + Claude Code 编程助手*
