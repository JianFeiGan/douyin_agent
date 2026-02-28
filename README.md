# Douyin Agent - 抖音视频发布自动化智能体

基于 OpenClaw 多智能体架构 + Claude Code 编程助手

## 系统架构

```
                              用户 (Feishu/终端)
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    OpenClaw Main Agent    │
                    │      (任务协调器)          │
                    └───────────────────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    │                               │                               │
    ▼                               ▼                               ▼
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│ Content     │           │ Video       │           │ Publish     │
│ Agent       │           │ Agent       │           │ Agent       │
│ (内容分析)   │           │ (视频生成)   │           │ (抖音发布)  │
└─────────────┘           └─────────────┘           └─────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    Claude Code            │
                    │    (编程助手)              │
                    └───────────────────────────┘
```

## 核心特性

- 🎯 **多智能体协同** - Main Agent 协调多个专业子 Agent
- 🤖 **AI 视频生成** - 集成 Seedance 2.0 (即梦) AI 视频生成
- 📱 **一键发布** - 自动发布到抖音
- 💻 **Claude Code 辅助** - AI 协助开发和调试脚本

## 技术栈

| 组件 | 技术 |
|------|------|
| 主控系统 | OpenClaw |
| AI 编程 | Claude Code (阿里云 DashScope) |
| 视频生成 | Seedance 2.0 (即梦) |
| 社交平台 | 抖音开放平台 |
| 消息渠道 | Feishu (飞书) |

## 快速开始

### 1. 启动 OpenClaw

```bash
openclaw gateway start
```

### 2. 配置

在 Feishu 中发送指令：
- `/create [视频内容描述]` - 创建视频生成任务
- `/publish [视频路径]` - 发布视频到抖音
- `/status [任务ID]` - 查看任务状态
- `/list` - 查看所有任务

### 3. 示例

```
用户: /create 帮我做一个关于AI技术科普的视频

OpenClaw:
├── Content Agent: 分析文本，提取关键词
├── Video Agent: 调用 Seedance 生成视频
└── Publish Agent: 发布到抖音

✅ 视频发布成功！链接: https://douyin.com/video/738xxx
```

## 目录结构

```
douyin_agent/
├── .openclaw/           # OpenClaw 配置
├── docs/                # 架构文档
│   └── architecture.md  # 系统架构设计
├── tasks/               # 任务记录
├── videos/              # 生成的视频
├── scripts/             # Claude Code 生成的脚本
└── logs/                # 日志
```

## 文档

- [系统架构设计](./docs/architecture.md)

## License

MIT
