# WebSocket Server 模块

## 📡 功能说明

这是一个为ESP32设备设计的WebSocket服务器模块，支持ESP32作为客户端连接并进行双向通信。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install websockets
```

或者更新所有依赖：

```bash
pip install -r requirements.txt
```

### 2. 启动WebSocket服务器

```bash
python websocket_server.py
```

服务器将在 `0.0.0.0:8765` 上启动，监听所有网络接口。

### 3. 测试连接

#### 方式一：使用Python测试客户端

```bash
python websocket_client_test.py
```

#### 方式二：使用ESP32硬件

1. 打开 `ai_core/websocket/esp32_client_example.ino`
2. 修改WiFi和服务器配置
3. 上传到ESP32
4. 查看串口输出

## 📝 通信协议

### 基本交互

**ESP32 → 服务器:**
```
hello world
```

**服务器 → ESP32:**
```
hello world2
```

### 其他消息

发送任意消息会收到带时间戳的响应：
```
收到消息: <你的消息> (时间: HH:MM:SS)
```

## 🔧 代码使用示例

### Python服务器端

```python
from ai_core.websocket import WebSocketServer

# 创建服务器
server = WebSocketServer(host="0.0.0.0", port=8765)

# 可选：自定义消息处理函数
async def my_handler(websocket, message):
    print(f"收到: {message}")
    if message == "hello world":
        return "hello world2"
    return f"Echo: {message}"

server.set_message_handler(my_handler)

# 启动服务器
server.start()
```

### ESP32客户端

```cpp
#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ws_host = "192.168.1.100";  // 你的电脑IP
const int ws_port = 8765;

WebSocketsClient webSocket;

void setup() {
    Serial.begin(115200);
    
    // 连接WiFi
    WiFi.begin("SSID", "PASSWORD");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
    
    // 连接WebSocket
    webSocket.begin(ws_host, ws_port, "/");
    webSocket.onEvent(webSocketEvent);
}

void loop() {
    webSocket.loop();
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    if (type == WStype_CONNECTED) {
        webSocket.sendTXT("hello world");
    } else if (type == WStype_TEXT) {
        Serial.printf("收到: %s\n", payload);
    }
}
```

## 📊 服务器功能

### 已实现功能

- ✅ 支持多客户端同时连接
- ✅ 自动处理连接/断开
- ✅ "hello world" / "hello world2" 交互
- ✅ 欢迎消息（JSON格式）
- ✅ 连接状态监控
- ✅ 错误处理和日志
- ✅ 支持自定义消息处理器

### 服务器信息

```python
# 获取服务器状态
info = server.get_server_info()
print(info)
# {
#     'host': '0.0.0.0',
#     'port': 8765,
#     'is_running': True,
#     'connected_clients': 2,
#     'server_time': '2025-10-08T21:00:00'
# }

# 获取连接数
count = server.get_connection_count()

# 广播消息到所有客户端
await server.broadcast("系统通知")
```

## 🔌 网络配置

### 获取本机IP地址

**Windows:**
```bash
ipconfig
```
查找 "IPv4 地址"

**Linux/Mac:**
```bash
ifconfig
# 或
ip addr show
```

### ESP32连接地址

假设你的电脑IP是 `192.168.1.100`，ESP32应连接到：
```
ws://192.168.1.100:8765
```

## 🛠️ 故障排除

### 问题1: ESP32无法连接

**解决方案:**
1. 确认ESP32和电脑在同一WiFi网络
2. 检查防火墙是否阻止端口8765
3. 验证IP地址是否正确
4. 测试用Python客户端先验证服务器工作正常

### 问题2: 连接后立即断开

**解决方案:**
1. 检查WiFi信号强度
2. 增加重连间隔时间
3. 查看服务器日志输出

### 问题3: Windows防火墙阻止

**解决方案:**
1. 打开Windows Defender防火墙设置
2. 允许Python通过防火墙
3. 或临时关闭防火墙测试

## 📚 项目结构

```
ai_core/websocket/
├── __init__.py                 # 模块初始化
├── websocket_server.py         # WebSocket服务器核心代码
├── esp32_client_example.ino   # ESP32客户端示例代码
└── README.md                   # 本文档

根目录/
├── websocket_server.py         # 服务器启动脚本
└── websocket_client_test.py   # Python测试客户端
```

## 🎯 扩展开发

### 添加AI功能集成

```python
from ai_core.websocket import WebSocketServer
from ai_core.tts.edge import EdgeTTS
from ai_core.asr.funasr_wrapper import FunASR

server = WebSocketServer()

async def ai_handler(websocket, message):
    # 语音识别
    asr = FunASR.get_instance()
    text = asr.transcribe_file(audio_file)
    
    # TTS生成语音
    tts = EdgeTTS.get_instance()
    tts.text_to_speech(text, "output.mp3")
    
    return f"处理完成: {text}"

server.set_message_handler(ai_handler)
server.start()
```

## 📄 许可证

与主项目相同

## 🤝 贡献

欢迎提交Issue和Pull Request！
