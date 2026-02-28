#!/usr/bin/env python3
"""
抖音视频发布自动化智能体 - 主入口
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator import AgentCoordinator
import argparse


def main():
    parser = argparse.ArgumentParser(description="抖音视频发布自动化智能体")
    parser.add_argument("--text", "-t", type=str, help="视频内容文本")
    parser.add_argument("--title", type=str, help="视频标题")
    parser.add_argument("--description", type=str, help="视频描述")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有任务")
    parser.add_argument("--status", type=str, help="查看任务状态")
    
    args = parser.parse_args()
    
    # 初始化协调器
    coordinator = AgentCoordinator()
    
    # 列出任务
    if args.list:
        tasks = coordinator.list_tasks()
        print(f"共有 {len(tasks)} 个任务:")
        for task in tasks:
            print(f"  - {task}")
        return
    
    # 查看任务状态
    if args.status:
        result = coordinator.get_status(args.status)
        if result:
            print(f"任务: {args.status}")
            print(f"状态: {'成功' if result.get('success') else '失败'}")
            if result.get('publish'):
                print(f"视频链接: {result['publish'].get('video_url')}")
        else:
            print(f"未找到任务: {args.status}")
        return
    
    # 创建任务
    if args.text:
        result = coordinator.run(
            user_input=args.text,
            title=args.title,
            description=args.description
        )
        
        if result.get("success"):
            print(f"\n✅ 视频发布成功!")
            print(f"任务ID: {result.get('task_id')}")
            print(f"视频链接: {result.get('publish', {}).get('video_url')}")
        else:
            print(f"\n❌ 任务失败: {result.get('error')}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
