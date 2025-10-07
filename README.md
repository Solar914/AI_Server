# AI Server - 智能语音处理服务

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

集成智谱 ChatGLM、FunASR 语音识别、EdgeTTS 语音合成和 Audio 音频处理的 AI 服务器。提供完整的语音对话处理链路。

## ✨ 功能特性

- 🤖 **ChatGLM**: 智谱 GLM-4.5 大语言模型，支持自然语言对话
- 🎤 **FunASR**: 本地 Paraformer 语音识别，支持 CPU/CUDA/XPU
- 🎵 **EdgeTTS**: 多语音角色的语音合成，支持参数调节
- 🔊 **Audio**: Opus 音频编解码，支持多质量预设
- 🚀 **会话管理**: 时间戳文件夹组织输出，完整的测试链路

## 📁 项目结构

```text
AI_Server/
├── ai_core/                   # 🤖 AI 核心模块
│   ├── asr/                  # 🎤 语音识别模块
│   │   └── funasr_wrapper.py # FunASR 封装类
│   ├── audio/                # 🎵 音频处理模块
│   │   └── audio.py         # Opus 编解码处理器
│   ├── llm/                  # 🧠 大语言模型模块
│   │   └── chatglm.py       # ChatGLM 封装类
│   └── tts/                  # 🔊 语音合成模块
│       └── edge.py          # EdgeTTS 封装类
├── outputs/                   # 📂 输出文件目录
│   └── YYYYMMDD_HHMMSS/     # 按时间戳组织的会话文件夹
│       ├── EdgeTTS/         # EdgeTTS 测试输出
│       ├── FunASR/          # FunASR 测试输出
│       ├── ChatGLM/         # ChatGLM 测试输出
│       ├── Audio/           # Audio 处理测试输出
│       └── Comprehensive/   # 综合演示输出
├── scripts/                   # 🛠️ 工具脚本目录
├── tools/                     # 🔧 工具集合目录
├── docs/                      # 📚 文档目录
├── AI_Server/                # 🐍 Python 虚拟环境
├── run.py                     # 🚀 项目主入口文件
├── requirements.txt           # 📋 依赖包配置
├── .env.example              # 🔑 API 密钥配置示例
├── .gitignore               # 🚫 Git 忽略规则
├── LICENSE                  # 📄 许可证文件
└── README.md                # 📖 项目文档
```

## 🚀 快速开始

### 1. 环境准备

**激活虚拟环境：**

```bash
# Windows PowerShell
.\AI_Server\Scripts\Activate.ps1

# 或使用 cmd
AI_Server\Scripts\activate.bat
```

**安装依赖：**

```bash
pip install -r requirements.txt
```

### 2. 配置与启动

```bash
# 配置 API 密钥
cp .env.example .env
# 编辑 .env 文件: ZHIPU_API_KEY=your_api_key_here

# 启动项目
python run.py
```

**功能菜单：** EdgeTTS演示 | FunASR演示 | ChatGLM演示 | Audio处理 | 综合演示

### 3. 预期输出

所有测试输出保存在 `outputs/时间戳/模块名/` 目录下，支持完整的语音对话链路演示。

## 📚 API 使用

```python
# ChatGLM 对话
from ai_core.llm.chatglm import ChatGLM
chatglm = ChatGLM.get_instance("your_api_key")
response = chatglm.generate_response("你好")

# FunASR 语音识别  
from ai_core.asr.funasr_wrapper import FunASR
asr = FunASR.get_instance()
result = asr.transcribe_file("audio.wav")

# EdgeTTS 语音合成
from ai_core.tts.edge import EdgeTTS
tts = EdgeTTS.get_instance()
audio_path = tts.text_to_speech("你好")

# Audio 音频处理
from ai_core.audio.audio import DownlinkProcessor, UplinkProcessor
downlink = DownlinkProcessor("balanced")
opus_data = downlink.process_audio("input.mp3", "bytes")
uplink = UplinkProcessor("general")
audio_path = uplink.decode_opus(opus_data, "file", "output.wav")
```

## 📋 依赖项

Python 3.11+, zai-sdk, edge-tts, funasr, python-dotenv, pydub, torch

## 🛠️ 开发说明

- 输出文件按时间戳组织：`outputs/YYYYMMDD_HHMMSS/模块名/`
- 所有模块采用单例模式设计
- 支持 CPU/CUDA/XPU 设备自动检测

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 📧 Email: <418754178@qq.com>  
- 🐛 Issues: [GitHub Issues](https://github.com/Solar914/AI_Server/issues)

---

**⭐ 如果这个项目对您有帮助，请给个 Star！**
