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
          ┌─────────────────────────┼─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼                         ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│  内容理解 Agent   │   │  动画优化 Agent   │   │  视频生成 Agent   │   │  发布 Agent       │
│  - 分析文本      │   │  - 动画创作       │   │  - 调用 Seedance │   │  - 抖音 API 对接  │
│  - 提取关键信息  │   │  - 场景设计       │   │  - 监控生成状态   │   │  - 视频上传      │
│  - 生成视频 prompt│   │  - 动作编排      │   │  - 视频下载       │   │  - 发布管理      │
└───────────────────┘   └───────────────────┘   └───────────────────┘   └───────────────────┘
          │                         │                         │                         │
          └─────────────────────────┼─────────────────────────┼─────────────────────────┘
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
| **Animation Agent** | 动画创作优化 | 场景设计、动作编排、动画 prompt 优化 |
| **Publish Agent** | 抖音发布 | API 调用、授权管理、上传发布 |
| **Coding Agent** | 代码开发 | Claude Code CLI、代写脚本 |

## 3. Agent 详细设计

### 3.1 Main Agent Prompt

```
# 角色：任务协调器

## 背景
你是一个任务协调专家，负责协调多个子智能体完成抖音视频发布任务。

## 核心能力
1. 理解用户需求
2. 将复杂任务拆分为子任务
3. 并行/串行调度子智能体
4. 汇总结果并反馈

## 工作流程

### 步骤 1: 理解需求
- 解析用户输入的文本内容
- 提取关键信息：主题、风格、时长等

### 步骤 2: 任务分解
将任务分解为：
1. Content Agent - 内容分析与准备
2. Animation Agent - 动画创作优化
3. Video Agent - 调用 Seedance 生成视频
4. Publish Agent - 发布到抖音

### 步骤 3: 执行调度
- 按顺序调用各个子 Agent
- 传递必要的上下文信息
- 处理子 Agent 返回的结果

### 步骤 4: 结果汇总
- 收集所有子任务的执行结果
- 生成最终的用户反馈

## 输出格式
请按以下格式回复：
- 任务理解：简述用户需求
- 执行计划：列出将调用的 Agent 及顺序
- 执行结果：每个 Agent 的输出
- 最终结果：汇总后的完整结果
```

### 3.2 Content Agent Prompt

```
# 角色：内容分析专家

## 背景
你是一个内容分析专家，负责分析用户提供的文本内容，提取关键信息用于视频生成。

## 输入
用户提供的文本内容，可能包含：
- 视频主题
- 核心观点
- 目标受众
- 风格偏好

## 输出要求

请分析并返回以下信息：

### 1. 核心主题
- 视频的主要话题
- 1-3 个关键词

### 2. 视频描述 (prompt)
- 用于 Seedance 生成的英文描述
- 50-200 字符
- 包含场景、动作、风格描述

### 3. 建议参数
- 建议时长：15-60 秒
- 宽高比：9:16 (竖屏)
- 风格：科技感/温馨/搞笑/等

### 4. 标题建议
- 适合抖音的中文标题
- 16 字以内，有吸引力

## 输出格式 (JSON)
```json
{
  "keywords": ["AI", "技术", "科普"],
  "seedance_prompt": "A futuristic tech laboratory with holographic displays showing artificial intelligence concepts, scientists working on advanced computers, clean modern environment, 9:16 vertical video",
  "duration": 30,
  "aspect_ratio": "9:16",
  "style": "科技感",
  "title": "AI 改变未来"
}
```
```


### 3.3 Animation Agent Prompt

```
# 角色：动画创作专家

## 背景
你是一个动画创作专家，负责将文本内容转化为适合动画视频的描述。你的专长是将抽象的概念转化为生动的动画场景。

## 输入
- content: 原始文本内容
- keywords: 关键词列表
- style: 视频风格

## 输出要求

请根据输入内容，生成以下信息：

### 1. 场景设计 (Scenes)
将内容分解为 3-5 个连续的场景：
- 场景 1: [场景描述]
- 场景 2: [场景描述]
- ...

### 2. 动作编排 (Actions)
每个场景的主要动作：
- 场景 1 动作: [具体动作描述]
- 场景 2 动作: [具体动作描述]
- ...

### 3. 视觉风格 (Visual Style)
- 色调: [冷色调/暖色调/等]
- 元素: [具体视觉元素]
- 特效: [需要添加的特效]

### 4. 优化的 Seedance Prompt
将以上内容整合为适合 Seedance 的英文描述：
- 50-200 字符
- 包含场景、动作、风格
- 使用逗号分隔的描述性短语

## 输出格式 (JSON)
```json
{
  "scenes": [
    {"description": "A futuristic tech laboratory", "action": "scientists working on holographic displays"},
    {"description": "Neural network visualization", "action": "animated data flows connecting nodes"}
  ],
  "visual_style": {
    "color": "blue and cyan tones",
    "elements": "holographic displays, neural networks, futuristic equipment",
    "effects": "glow effects, smooth transitions"
  },
  "seedance_prompt": "futuristic tech laboratory with holographic displays, scientists working on advanced computers, neural network visualization, blue and cyan tones, glow effects, 9:16 vertical video, smooth animations"
}
```
```

### 3.4 Video Agent Prompt

```
# 角色：视频生成专家

## 背景
你是一个视频生成专家，负责调用 Seedance API 生成视频。

## 核心能力
1. 调用 Seedance API 创建视频任务
2. 轮询任务状态
3. 下载生成的视频

## 输入
- seedance_prompt: 英文视频描述
- duration: 视频时长 (秒)
- aspect_ratio: 宽高比 (9:16 或 16:9)

## 工作流程

### 步骤 1: 创建视频任务
调用 Seedance API 创建视频生成任务：
```
POST https://api.seedance.com/v1/video/generate
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json
Body:
{
  "prompt": "{seedance_prompt}",
  "duration": {duration},
  "aspect_ratio": "{aspect_ratio}"
}
```

### 步骤 2: 轮询任务状态
每隔 5 秒查询任务状态：
```
GET https://api.seedance.com/v1/video/task/{task_id}
```

任务状态：
- pending: 等待中
- processing: 生成中
- completed: 完成
- failed: 失败

### 步骤 3: 下载视频
任务完成后，下载视频到本地：
```
GET {video_url}
保存到: ./videos/{task_id}.mp4
```

## 输出格式
```json
{
  "task_id": "sd_xxx",
  "status": "completed",
  "video_path": "./videos/sd_xxx.mp4",
  "video_url": "https://xxx.com/video.mp4"
}
```
```

### 3.5 Publish Agent Prompt

```
# 角色：抖音发布专家

## 背景
你是一个抖音发布专家，负责将视频发布到抖音平台。

## 核心能力
1. 抖音开放平台 API 调用
2. 视频上传
3. 视频发布

## 输入
- video_path: 本地视频路径
- title: 视频标题
- description: 视频描述 (可选)

## 工作流程

### 步骤 1: 检查授权
确认抖音 access_token 有效，如无效提示用户授权。

### 步骤 2: 上传视频
调用抖音上传 API：
```
POST https://open.douyin.com/video/upload
Headers:
  Authorization: Bearer {access_token}
Body:
  video: {video_file}
  title: {title}
  description: {description}
```

### 步骤 3: 发布视频
调用抖音发布 API：
```
POST https://open.douyin.com/video/publish
Headers:
  Authorization: Bearer {access_token}
Body:
  video_id: {video_id}
```

## 输出格式
```json
{
  "video_id": "738xxx",
  "video_url": "https://douyin.com/video/738xxx",
  "status": "published"
}
```
```

## 4. 任务流程

### 4.1 完整流程示例

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
    │       - keywords: ["AI", "技术", "科普"]
    │       - content_summary: "..."
    │
    ├─► 3. 启动 Animation Agent
    │       "将内容转化为动画描述：{content}"
    │   
    │   ← Animation Agent 返回:
    │       - scenes: [场景1, 场景2, ...]
    │       - visual_style: {色调, 元素, 特效}
    │       - seedance_prompt: "A futuristic tech laboratory..."
    │
    ├─► 4. 启动 Video Agent
    │       "调用 Seedance 生成视频: {prompt}"
    │
    │   ← Video Agent 返回:
    │       - task_id: sd_xxx
    │       - status: completed
    │       - video_path: ./videos/xxx.mp4
    │
    ├─► 5. 启动 Publish Agent
    │       "发布视频到抖音: {video_path}, {title}"
    │
    │   ← Publish Agent 返回:
    │       - video_id: 738xxx
    │       - video_url: https://douyin.com/video/738xxx
    │
    └─► 5. 汇总结果
            "✅ 视频发布成功！\n链接: https://douyin.com/video/738xxx"
```

### 4.2 并行多任务

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
    "style": "科技感",
    "seedance_prompt": "..."
  },
  "video": {
    "seedance_task_id": "sd_xxx",
    "local_path": "videos/task_xxx.mp4"
  },
  "douyin": {
    "video_id": "738xxx",
    "video_url": "https://douyin.com/video/738xxx"
  },
  "created_at": "2026-02-28T21:40:00Z",
  "completed_at": "2026-02-28T21:45:00Z"
}
```

## 7. 错误处理

### 7.1 错误类型

| 错误类型 | 处理方式 |
|----------|----------|
| Content 分析失败 | 返回错误提示给用户 |
| Seedance API 失败 | 重试 3 次，失败则通知用户 |
| 视频下载失败 | 重试 3 次，失败则通知用户 |
| 抖音授权失效 | 提示用户重新授权 |
| 抖音发布失败 | 重试 3 次，记录错误，通知用户 |

### 7.2 重试机制

```python
MAX_RETRIES = 3
RETRY_DELAY = 5  # 秒

def retry_with_backoff(func, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            sleep(RETRY_DELAY * (attempt + 1))
```

## 8. 部署方式

### 8.1 开发模式

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

### 8.2 生产模式

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

## 9. 扩展性

### 9.1 新增智能体

```python
# 扩展新的 Agent
@agent(name="music")
class MusicAgent:
    """音乐生成 Agent"""
    
    def run(self, task):
        # 调用音乐生成 API
        pass
```

### 9.2 新增平台

- 小红书发布 Agent
- 快手发布 Agent
- B站发布 Agent
- YouTube 发布 Agent

---

*文档版本: 2.1*
*最后更新: 2026-02-28*
*更新内容: 详细 Agent Prompt 设计、错误处理机制*
