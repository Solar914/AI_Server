"""WebSocket服务器封装类 - 用于ESP32客户端通信"""

import asyncio
import websockets
from typing import Optional, Callable
from datetime import datetime
import json


class WebSocketServer:
    """WebSocket服务器类 - 支持ESP32设备连接"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        """初始化WebSocket服务器
        
        Args:
            host: 服务器地址，默认0.0.0.0监听所有网络接口
            port: 服务器端口，默认8765
        """
        self.host = host
        self.port = port
        self.server = None
        self.connected_clients = set()
        self.message_handler = None
        self.is_running = False
        
    def set_message_handler(self, handler: Callable):
        """设置自定义消息处理函数
        
        Args:
            handler: 消息处理函数，接收(websocket, message)参数，返回响应消息
        """
        self.message_handler = handler
        
    async def default_message_handler(self, websocket, message: str) -> str:
        """默认消息处理函数 - ESP32 hello world示例
        
        Args:
            websocket: WebSocket连接对象
            message: 接收到的消息
            
        Returns:
            响应消息字符串
        """
        print(f"📩 收到消息: {message}")
        
        # ESP32 hello world交互逻辑
        if message.strip().lower() == "hello world":
            response = "hello world2"
            print(f"📤 发送响应: {response}")
            return response
        else:
            # 其他消息的默认响应
            response = f"收到消息: {message} (时间: {datetime.now().strftime('%H:%M:%S')})"
            print(f"📤 发送响应: {response}")
            return response
    
    async def handle_client(self, websocket):
        """处理客户端连接
        
        Args:
            websocket: WebSocket连接对象
        """
        # 获取客户端信息
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        print(f"✅ 新客户端连接: {client_info}")
        
        # 添加到已连接客户端集合
        self.connected_clients.add(websocket)
        
        try:
            # 发送欢迎消息
            welcome_msg = json.dumps({
                "type": "welcome",
                "message": "欢迎连接到AI Server WebSocket!",
                "server_time": datetime.now().isoformat(),
                "client_count": len(self.connected_clients)
            })
            await websocket.send(welcome_msg)
            print(f"📤 发送欢迎消息到 {client_info}")
            
            # 持续接收和处理消息
            async for message in websocket:
                try:
                    # 使用自定义处理函数或默认处理函数
                    handler = self.message_handler if self.message_handler else self.default_message_handler
                    response = await handler(websocket, message)
                    
                    # 发送响应
                    if response:
                        await websocket.send(response)
                        
                except Exception as e:
                    error_msg = f"处理消息时出错: {e}"
                    print(f"❌ {error_msg}")
                    await websocket.send(f"ERROR: {error_msg}")
                    
        except websockets.exceptions.ConnectionClosedOK:
            print(f"👋 客户端正常断开: {client_info}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"⚠️ 客户端异常断开: {client_info} - {e}")
        except Exception as e:
            print(f"❌ 连接错误: {client_info} - {e}")
        finally:
            # 从已连接客户端集合中移除
            self.connected_clients.discard(websocket)
            print(f"📊 当前连接数: {len(self.connected_clients)}")
    
    async def start_async(self):
        """异步启动WebSocket服务器"""
        self.is_running = True
        
        print(f"🚀 启动WebSocket服务器...")
        print(f"📡 监听地址: {self.host}:{self.port}")
        print(f"💡 ESP32连接示例: ws://<your-ip>:{self.port}")
        print(f"=" * 50)
        
        # 启动WebSocket服务器
        # ping_interval: 每隔多少秒发送一次ping (默认20秒，设为60秒)
        # ping_timeout: 等待pong响应的超时时间 (默认20秒，设为60秒)
        # close_timeout: 关闭连接的超时时间 (默认10秒，设为30秒)
        async with websockets.serve(
            self.handle_client, 
            self.host, 
            self.port,
            ping_interval=60,  # 每60秒发送一次ping
            ping_timeout=60,   # 等待pong响应60秒
            close_timeout=30   # 关闭连接超时30秒
        ):
            print(f"✅ WebSocket服务器运行中，按Ctrl+C停止...")
            
            # 保持服务器运行
            await asyncio.Future()  # 永久运行
    
    def start(self):
        """启动WebSocket服务器（同步方式）"""
        try:
            asyncio.run(self.start_async())
        except KeyboardInterrupt:
            print(f"\n⏹️ 服务器已停止")
            self.is_running = False
        except Exception as e:
            print(f"❌ 服务器启动失败: {e}")
            self.is_running = False
    
    async def broadcast(self, message: str):
        """向所有连接的客户端广播消息
        
        Args:
            message: 要广播的消息
        """
        if self.connected_clients:
            tasks = [client.send(message) for client in self.connected_clients]
            await asyncio.gather(*tasks, return_exceptions=True)
            print(f"📢 已向 {len(self.connected_clients)} 个客户端广播消息")
    
    def get_connection_count(self) -> int:
        """获取当前连接的客户端数量"""
        return len(self.connected_clients)
    
    def get_server_info(self) -> dict:
        """获取服务器信息"""
        return {
            'host': self.host,
            'port': self.port,
            'is_running': self.is_running,
            'connected_clients': len(self.connected_clients),
            'server_time': datetime.now().isoformat()
        }


# 单例模式
_websocket_server_instance = None

def get_websocket_server(host: str = "0.0.0.0", port: int = 8765) -> WebSocketServer:
    """获取WebSocket服务器单例实例
    
    Args:
        host: 服务器地址
        port: 服务器端口
        
    Returns:
        WebSocketServer实例
    """
    global _websocket_server_instance
    if _websocket_server_instance is None:
        _websocket_server_instance = WebSocketServer(host, port)
    return _websocket_server_instance
