/*
 * ESP32 WebSocket客户端示例代码
 * 连接到AI Server并发送"hello world"
 */

#include <WiFi.h>
#include <WebSocketsClient.h>

// WiFi配置
const char* ssid = "YOUR_WIFI_SSID";        // 替换为你的WiFi名称
const char* password = "YOUR_WIFI_PASSWORD"; // 替换为你的WiFi密码

// WebSocket服务器配置
const char* ws_host = "192.168.1.100";  // 替换为你的电脑IP地址
const int ws_port = 8765;                // WebSocket服务器端口
const char* ws_path = "/";               // WebSocket路径

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("[WebSocket] 已断开连接");
            break;
            
        case WStype_CONNECTED:
            Serial.println("[WebSocket] 已连接到服务器");
            Serial.printf("[WebSocket] 服务器地址: ws://%s:%d%s\n", ws_host, ws_port, ws_path);
            
            // 连接成功后发送"hello world"
            webSocket.sendTXT("hello world");
            Serial.println("[WebSocket] 发送: hello world");
            break;
            
        case WStype_TEXT:
            Serial.printf("[WebSocket] 收到消息: %s\n", payload);
            
            // 如果收到"hello world2"，说明通信成功
            if (strcmp((char*)payload, "hello world2") == 0) {
                Serial.println("[WebSocket] ✅ 通信成功！收到预期响应");
            }
            break;
            
        case WStype_BIN:
            Serial.println("[WebSocket] 收到二进制数据");
            break;
            
        case WStype_ERROR:
            Serial.println("[WebSocket] 错误");
            break;
            
        case WStype_PING:
            Serial.println("[WebSocket] 收到PING");
            break;
            
        case WStype_PONG:
            Serial.println("[WebSocket] 收到PONG");
            break;
    }
}

void setup() {
    // 初始化串口
    Serial.begin(115200);
    Serial.println("\n\n=================================");
    Serial.println("ESP32 WebSocket客户端启动");
    Serial.println("=================================\n");
    
    // 连接WiFi
    Serial.printf("正在连接WiFi: %s\n", ssid);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\n✅ WiFi连接成功");
    Serial.printf("IP地址: %s\n", WiFi.localIP().toString().c_str());
    Serial.printf("信号强度: %d dBm\n\n", WiFi.RSSI());
    
    // 初始化WebSocket客户端
    Serial.printf("正在连接WebSocket服务器: ws://%s:%d%s\n", ws_host, ws_port, ws_path);
    webSocket.begin(ws_host, ws_port, ws_path);
    
    // 设置事件处理函数
    webSocket.onEvent(webSocketEvent);
    
    // 设置重连间隔（毫秒）
    webSocket.setReconnectInterval(5000);
    
    Serial.println("WebSocket客户端已初始化\n");
}

void loop() {
    // 保持WebSocket连接
    webSocket.loop();
    
    // 可选：每10秒发送一次"hello world"
    static unsigned long lastSendTime = 0;
    unsigned long currentTime = millis();
    
    if (currentTime - lastSendTime > 10000) {  // 10秒
        if (webSocket.isConnected()) {
            webSocket.sendTXT("hello world");
            Serial.println("[WebSocket] 发送: hello world");
        }
        lastSendTime = currentTime;
    }
    
    delay(10);
}

/*
 * 📝 使用说明：
 * 
 * 1. 安装依赖库：
 *    - 在Arduino IDE中安装 "WebSockets" by Markus Sattler
 * 
 * 2. 配置参数：
 *    - 修改 ssid 和 password 为你的WiFi信息
 *    - 修改 ws_host 为运行WebSocket服务器的电脑IP地址
 * 
 * 3. 上传到ESP32并打开串口监视器（115200波特率）
 * 
 * 4. 预期输出：
 *    - WiFi连接成功
 *    - WebSocket连接成功
 *    - 发送: hello world
 *    - 收到: hello world2
 *    - ✅ 通信成功！
 */
