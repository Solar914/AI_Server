#!/usr/bin/env python3
"""WebSocket服务器启动脚本 - ESP32客户端通信"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from ai_core.websocket.websocket_server import WebSocketServer


def main():
    """主函数 - 启动WebSocket服务器"""
    print("=" * 50)
    print("🌐 AI Server - WebSocket服务器")
    print("=" * 50)
    
    # 创建WebSocket服务器
    # 监听所有网络接口，ESP32可通过局域网IP连接
    server = WebSocketServer(host="0.0.0.0", port=8765)
    
    # 可选：自定义消息处理函数
    # server.set_message_handler(my_custom_handler)
    
    # 获取本机IP提示
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"💡 本机IP: {local_ip}")
        print(f"💡 ESP32连接地址: ws://{local_ip}:8765")
    except:
        print(f"💡 ESP32连接地址: ws://<your-ip>:8765")
    
    print(f"\n📝 使用说明:")
    print(f"   1. ESP32发送: 'hello world'")
    print(f"   2. 服务器响应: 'hello world2'")
    print(f"   3. 其他消息会收到带时间戳的回复")
    print()
    
    # 启动服务器
    server.start()


if __name__ == "__main__":
    main()
