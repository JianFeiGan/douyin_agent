# Douyin Agent Skill

飞书/终端调用抖音视频发布自动化智能体的技能

## 触发方式

当用户发送以下内容时激活：
- 包含"抖音"或"视频发布"的请求
- 指令 `/create`, `/publish`, `/status`

## 功能

1. **创建视频任务** - 输入文本内容，自动生成并发布视频
2. **查看任务状态** - 查看任务进度和结果
3. **列出所有任务** - 查看历史任务

## 使用方式

```
用户: 帮我做一个AI科普视频发布到抖音
→ 调用 Content Agent → Animation Agent → Video Agent → Publish Agent
→ 返回结果
```

## 配置

需要配置以下环境变量：
- SEEDANCE_API_KEY: Seedance API 密钥
- DOUYIN_APP_ID: 抖音开放平台 App ID
- DOUYIN_APP_SECRET: 抖音开放平台 App Secret

## 注意事项

- 视频生成需要 Seedance API
- 抖音发布需要 OAuth 授权
- 当前为模拟实现，需要替换为真实 API 调用
