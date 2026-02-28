#!/usr/bin/env python3
"""
OpenClaw 集成入口
简化版 - 供 OpenClaw 通过 exec 调用
"""
import sys
import os
import json
import argparse

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator import AgentCoordinator


def main():
    # 解析 JSON 输入
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help='JSON 输入: {"text": "...", "title": "..."}')
    args = parser.parse_args()
    
    if args.input:
        # 解析 JSON
        data = json.loads(args.input)
        text = data.get("text", "")
        title = data.get("title", "")
        description = data.get("description", "")
    else:
        # 从环境变量或 stdin 读取
        text = os.getenv("DOUYIN_TEXT", "")
        title = os.getenv("DOUYIN_TITLE", "")
        description = os.getenv("DOUYIN_DESC", "")
    
    if not text:
        print("Usage: python3 run.py --input '{\"text\": \"内容\", \"title\": \"标题\"}'")
        sys.exit(1)
    
    # 初始化协调器
    coordinator = AgentCoordinator()
    
    # 执行任务
    result = coordinator.run(
        user_input=text,
        title=title,
        description=description
    )
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 返回状态码
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
