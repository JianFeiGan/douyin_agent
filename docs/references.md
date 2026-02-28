# 参考案例研究

本文档收集了与本项目相关的开源参考案例。

---

## 1. 多智能体框架

### 1.1 MetaGPT

**仓库地址**: https://github.com/FoundationAgents/MetaGPT

**核心特点**:
- 模拟软件公司流程，包含 PM、Architect、Engineer 等角色
- 输入需求 → 输出完整的软件项目结构、文档、代码
- Code = SOP(Team) 核心理念
- 支持 Data Interpreter、Researcher 等专业角色

**适用场景**:
- 复杂任务的分解与协同
- 软件开发流程自动化

**架构借鉴**:
- 多角色 SOP 协作机制
- 任务分解与结果汇总模式

```
用户需求 → PM → Architect → Engineer → 测试 → 输出
```

---

### 1.2 CowAgent (chatgpt-on-wechat)

**仓库地址**: https://github.com/zhayujie/chatgpt-on-wechat

**核心特点**:
- 支持飞书、钉钉、企业微信、微信公众号接入
- 多模型支持：OpenAI, Claude, Gemini, DeepSeek, MiniMax, GLM, Qwen, Kimi
- Agent 模式：多轮任务决策、长期记忆、Skills 能力
- 7*24 小时运行

**支持渠道**:
- 飞书
- 钉钉
- 企业微信应用
- 微信公众号
- Web 网页
- Terminal

**配置示例**:
```json
{
  "channel_type": "feishu",
  "model": "MiniMax-M2.5",
  "minimax_api_key": "your_key",
  "agent": true,
  "agent_workspace": "~/cow",
  "agent_max_steps": 15
}
```

**适用场景**:
- 企业级 AI 助理
- 多渠道消息接入
- 需要长期记忆的任务

**架构借鉴**:
- 飞书集成（与 OpenClaw 相同）
- 多模型切换
- Skills 系统设计

---

### 1.3 AgentScope

**仓库地址**: https://github.com/agentscope-ai/agentscope

**核心特点**:
- "Build and run agents you can see, understand and trust"
- 可视化的 Agent 运行监控
- 企业级架构

**适用场景**:
- 需要可视化监控的 Agent 系统

---

### 1.4 Google ADK (Agent Development Kit)

**仓库地址**: https://github.com/google/adk-python

**核心特点**:
- Google 官方的 Agent 开发工具包
- 代码优先的 Python 工具包
- 支持构建、评估、部署复杂的 AI Agents

---

### 1.5 ruflo (OpenClaw 竞品)

**仓库地址**: https://github.com/ruvnet/ruflo

**核心特点**:
- Claude 多智能体编排平台
- 多智能体群协同
- 企业级架构
- 分布式群智能
- 原生支持 Claude Code / Codex 集成

---

## 2. 视频生成相关

### 2.1 Seedance (即梦)

**官网**: https://seedance.com

**API 能力**:
- 文本到视频生成
- 图片到视频生成
- 视频编辑

**国内可访问性**: ✅ (字节跳动)

---

## 3. 对比分析

| 框架 | 多Agent | 飞书集成 | 视频生成 | 编程辅助 | 推荐程度 |
|------|---------|----------|----------|----------|----------|
| **MetaGPT** | ✅ | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| **CowAgent** | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐⭐ |
| **AgentScope** | ✅ | ❌ | ❌ | ❌ | ⭐⭐ |
| **Google ADK** | ✅ | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| **ruflo** | ✅ | ❌ | ❌ | ✅ | ⭐⭐⭐⭐ |
| **OpenClaw (本项目)** | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |

---

## 4. 本项目定位

结合以上案例，本项目采用以下策略：

1. **OpenClaw 为主控** - 借鉴 CowAgent 的飞书集成能力
2. **多智能体架构** - 借鉴 MetaGPT 的 SOP 协作模式
3. **Claude Code 辅助** - 借鉴 ruflo 的编程助手集成
4. **Seedance 视频生成** - 专注于短视频自动化

**独特优势**:
- 专注抖音视频发布场景
- 端到端自动化
- 飞书消息驱动
- Claude Code 辅助开发

---

## 5. 相关资源

- [MetaGPT 文档](https://docs.deepwisdom.ai/main/en/)
- [CowAgent 文档](https://docs.cowagent.ai/)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Seedance 官网](https://seedance.com)

---

*最后更新: 2026-02-28*
