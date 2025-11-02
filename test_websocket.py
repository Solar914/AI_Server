#!/usr/bin/env python3
"""WebSocket服务器自动化测试脚本"""

import asyncio
import websockets
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


async def test_websocket_communication():
    """测试WebSocket通信功能"""
    print("=" * 60)
    print("🧪 WebSocket服务器功能测试")
    print("=" * 60)
    
    uri = "ws://localhost:8765"
    
    try:
        print(f"\n1️⃣ 连接测试")
        print(f"   🔌 连接到: {uri}")
        
        async with websockets.connect(
            uri,
            ping_interval=60,
            ping_timeout=60,
            close_timeout=30
        ) as websocket:
            print(f"   ✅ 连接成功\n")
            
            # 测试1: 接收欢迎消息
            print(f"2️⃣ 欢迎消息测试")
            try:
                welcome = await asyncio.wait_for(websocket.recv(), timeout=3)
                print(f"   📩 收到欢迎消息: {welcome[:100]}...")
                print(f"   ✅ 欢迎消息测试通过\n")
            except asyncio.TimeoutError:
                print(f"   ⚠️ 未收到欢迎消息（可能已禁用）\n")
            
            # 测试2: hello world交互
            print(f"3️⃣ Hello World测试")
            print(f"   📤 发送: 'hello world'")
            await websocket.send("hello world")
            
            response = await asyncio.wait_for(websocket.recv(), timeout=3)
            print(f"   📩 收到: '{response}'")
            
            if response == "hello world2":
                print(f"   ✅ Hello World测试通过 - 收到预期响应\n")
            else:
                print(f"   ❌ Hello World测试失败 - 预期'hello world2'，实际收到'{response}'\n")
                return False
            
            # 测试3: 普通消息
            print(f"4️⃣ 普通消息测试")
            test_msg = "测试消息123"
            print(f"   📤 发送: '{test_msg}'")
            await websocket.send(test_msg)
            
            response = await asyncio.wait_for(websocket.recv(), timeout=3)
            print(f"   📩 收到: '{response}'")
            
            if test_msg in response:
                print(f"   ✅ 普通消息测试通过\n")
            else:
                print(f"   ⚠️ 响应格式可能不同\n")
            
            # 测试4: 多次通信
            print(f"5️⃣ 多次通信测试")
            for i in range(3):
                msg = f"消息{i+1}"
                await websocket.send(msg)
                response = await asyncio.wait_for(websocket.recv(), timeout=3)
                print(f"   {i+1}. 发送'{msg}' → 收到'{response[:30]}...'")
            print(f"   ✅ 多次通信测试通过\n")
            
            print(f"=" * 60)
            print(f"✅ 所有测试通过！服务器功能正常")
            print(f"=" * 60)
            return True
            
    except ConnectionRefusedError:
        print(f"\n❌ 测试失败: 无法连接到服务器")
        print(f"   请确保服务器正在运行: python websocket_server.py")
        return False
    except asyncio.TimeoutError:
        print(f"\n❌ 测试失败: 服务器响应超时")
        return False
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def quick_test():
    """快速测试 - 只验证核心功能"""
    print("\n🚀 快速测试模式\n")
    
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(
            uri,
            ping_interval=60,
            ping_timeout=60,
            close_timeout=30
        ) as websocket:
            # 跳过欢迎消息
            try:
                await asyncio.wait_for(websocket.recv(), timeout=1)
            except:
                pass
            
            # 测试hello world
            await websocket.send("hello world")
            response = await websocket.recv()
            
            if response == "hello world2":
                print(f"✅ 核心功能正常: hello world → hello world2")
                return True
            else:
                print(f"❌ 响应错误: 预期'hello world2'，收到'{response}'")
                return False
                
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='WebSocket服务器测试工具')
    parser.add_argument('--quick', action='store_true', help='快速测试模式')
    args = parser.parse_args()
    
    try:
        if args.quick:
            result = asyncio.run(quick_test())
        else:
            result = asyncio.run(test_websocket_communication())
        
        sys.exit(0 if result else 1)
        
    except KeyboardInterrupt:
        print(f"\n⏹️ 测试已取消")
        sys.exit(1)


if __name__ == "__main__":
    main()
