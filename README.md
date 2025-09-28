# AI Server - ChatGLM + EdgeTTS 集成项目

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![ChatGLM](https://img.shields.io/badge/Model-GLM--4.5-orange.svg)](https://zhipu-ai.cn/)
[![EdgeTTS](https://img.shields.io/badge/TTS-Edge--TTS-red.svg)](https://github.com/rany2/edge-tts)

一个集成了智谱 ChatGLM 大语言模型和 Microsoft Edge TTS 语音合成的 AI 服务器项目。支持文本对话生成和语音合成功能，提供完整的"对话 → 语音"流程。

## ✨ 功能特性

### 🤖 ChatGLM 大语言模型
- ✅ **智谱 GLM-4.5 模型**：支持自然语言对话
- ✅ **单例模式设计**：全局唯一实例，节省资源
- ✅ **灵活参数配置**：可选的 temperature、max_tokens 等参数
- ✅ **对话历史支持**：维持上下文连续对话
- ✅ **系统提示词管理**：可自定义 AI 行为和角色

### 🎵 EdgeTTS 语音合成
- ✅ **多语音角色**：支持 10+ 种中文语音（男声/女声）
- ✅ **参数可调**：语速、音量可动态配置
- ✅ **异步处理**：高效的语音生成
- ✅ **文件管理**：自动创建输出目录和文件命名
- ✅ **错误处理**：完整的异常处理机制

### 🔗 集成特性
- ✅ **无缝集成**：ChatGLM 输出直接转换为语音
- ✅ **简单易用**：一键演示完整流程
- ✅ **模块化设计**：独立的类库，便于扩展

## 📁 项目结构

```
Python_Backend/
├── ai_core/                    # AI 核心模块
│   ├── llm/                   # 大语言模型模块
│   │   └── chatglm.py        # ChatGLM 封装类
│   └── tts/                   # 语音合成模块
│       └── edge.py           # EdgeTTS 封装类
├── outputs/                   # 输出文件目录
│   └── tts/                  # TTS 生成的音频文件
├── AI_Server/                # Python 虚拟环境
├── main.py                   # 主程序和演示
└── README.md                # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

**创建并激活虚拟环境：**
```bash
# Windows
python -m venv AI_Server
AI_Server\Scripts\activate

# Linux/macOS  
python -m venv AI_Server
source AI_Server/bin/activate
```

**安装依赖：**
```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

本项目支持两种方式配置智谱AI的API密钥：

#### 方法一：使用 .env 文件（推荐）
1. 复制示例配置文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的API密钥：
```env
ZHIPU_API_KEY=你的实际API密钥
```

#### 方法二：运行时输入
如果没有设置.env文件，程序会在运行时提示你输入API密钥。

### 3. 运行项目
```powershell
# 创建虚拟环境
python -m venv AI_Server

# 激活虚拟环境 (Windows)
.\\AI_Server\\Scripts\\Activate.ps1
```

**安装依赖：**
```powershell
# 方式1：使用 requirements.txt（推荐）
pip install -r requirements.txt

# 方式2：手动安装
pip install zai-sdk edge-tts python-dotenv
```

### 2. 运行演示

```powershell
# 使用虚拟环境运行
D:/AI_Work/01_Code/Python_Backend/AI_Server/Scripts/python.exe main.py
```

### 3. 预期输出

```
🚀 AI Server - ChatGLM + EdgeTTS 演示
==================================================

🎯 ChatGLM + EdgeTTS 简单演示
----------------------------------------
📝 正在初始化AI组件...
✅ 初始化完成

❓ 问题: 请简单介绍一下你自己，控制在50字以内
🤖 正在生成AI回复...
💬 AI回复: 我是一个AI助手，致力于提供有用信息和解答问题...

🎵 正在生成语音文件...
✅ 语音文件生成成功: outputs\\tts\\demo_output.mp3
🎉 演示完成! 语音文件: outputs\\tts\\demo_output.mp3
```

## 📚 API 使用指南

### ChatGLM 类使用

```python
from ai_core.llm.chatglm import ChatGLM

# 方式1: 直接传入API key
api_key = "你的API密钥"
chatglm = ChatGLM.get_instance(api_key)

# 方式2: 使用主程序的API key获取函数
from main import get_api_key
api_key = get_api_key()  # 会从.env文件或用户输入获取
chatglm = ChatGLM.get_instance(api_key)

# 基础对话
response = chatglm.generate_response("你好，请介绍一下人工智能")

# 高级参数配置
response = chatglm.generate_response(
    user_message="解释量子计算",
    system_message="你是一个科学专家",
    temperature=0.7,
    conversation_history=[
        {"role": "user", "content": "之前的问题"},
        {"role": "assistant", "content": "之前的回答"}
    ]
)

# 获取模型信息
info = chatglm.get_model_info()
print(info)
```

### EdgeTTS 类使用

```python
from ai_core.tts.edge import EdgeTTS

# 获取实例（单例模式）
tts = EdgeTTS.get_instance()

# 基础语音合成
audio_path = tts.text_to_speech("你好，欢迎使用语音合成服务")

# 高级参数配置
audio_path = tts.text_to_speech(
    text="这是一个测试语音",
    filename="custom_output.mp3",
    voice="zh-CN-YunjianNeural",  # 中文男声
    rate="+20%",                  # 语速快20%
    volume="+10%"                 # 音量大10%
)

# 获取可用语音列表
voices = tts.get_available_voices()
print(voices)
```

### 集成使用示例

```python
from ai_core.llm.chatglm import ChatGLM
from ai_core.tts.edge import EdgeTTS
from main import get_api_key  # 导入API key获取函数

# 获取API密钥
api_key = get_api_key()  # 从.env文件或用户输入获取

# 初始化
chatglm = ChatGLM.get_instance(api_key)  # 传入API key
tts = EdgeTTS.get_instance()

# 对话生成
user_question = "请简单解释什么是机器学习"
ai_response = chatglm.generate_response(user_question)

# 语音合成
audio_file = tts.text_to_speech(ai_response)
print(f"语音文件: {audio_file}")
```

## ⚙️ 配置说明

### ChatGLM 配置

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `api_key` | 智谱AI API密钥 | 用户提供 |
| `model` | 模型名称 | `glm-4.5` |
| `temperature` | 生成温度 (0-1) | 模型默认 |
| `max_tokens` | 最大token数 | 无限制 |

### EdgeTTS 配置

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `voice` | 语音角色 | `zh-CN-XiaoyiNeural` |
| `rate` | 语速调节 | `+0%` |
| `volume` | 音量调节 | `+0%` |

### 可用中文语音角色

| 简化名称 | 完整名称 | 性别 | 特点 |
|---------|---------|------|------|
| `xiaoyi` | `zh-CN-XiaoyiNeural` | 女声 | 标准女声 |
| `xiaoyou` | `zh-CN-XiaoyouNeural` | 男声 | 标准男声 |
| `yunxi` | `zh-CN-YunxiNeural` | 男声 | 成熟男声 |
| `yunxia` | `zh-CN-YunxiaNeural` | 女声 | 温和女声 |

## 📋 依赖项

### 核心依赖

- **Python 3.11+**：编程语言
- **zai-sdk**：智谱AI Python SDK
- **edge-tts**：Microsoft Edge TTS 语音合成
- **python-dotenv**：环境变量配置文件支持

### 可选依赖
- **typing**：类型注解支持
- **pathlib**：路径处理
- **asyncio**：异步编程支持

## 🛠️ 开发指南

### 扩展 ChatGLM 功能

```python
# 添加新的便捷方法
def quick_ask(self, question: str) -> str:
    return self.generate_response(
        user_message=question,
        temperature=0.5,
        system_message="请简洁回答"
    )
```

### 扩展 EdgeTTS 功能

```python
# 添加批量语音生成
def batch_text_to_speech(self, texts: List[str]) -> List[str]:
    audio_paths = []
    for i, text in enumerate(texts):
        path = self.text_to_speech(text, filename=f"batch_{i}.mp3")
        audio_paths.append(path)
    return audio_paths
```

## 🚨 故障排除

### 常见问题

1. **ModuleNotFoundError: No module named 'zai'**
   - 确保使用虚拟环境中的 Python 解释器
   - 检查是否正确激活虚拟环境

2. **API 调用失败**
   - 检查网络连接
   - 验证 API 密钥是否有效
   - 确认 API 配额未超限

3. **语音生成失败**
   - 检查文本内容是否为空
   - 确认输出目录权限
   - 验证语音角色名称是否正确

### 调试模式

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: 418754178@qq.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/ai-server/issues)

---

**⭐ 如果这个项目对您有帮助，请给个 Star！**