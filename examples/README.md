# AI Server 示例集合

本目录包含AI Server的各种使用示例和演示代码。

## 🎵 音频处理示例 (audio/)

### `audio_processing_sample.py`
完整的音频处理流程演示，展示：
- MP3 → Opus编码 (下行处理)
- Opus → WAV解码 (上行处理) 
- WAV → Opus重新编码
- 详细的字节流分析和参数对比

**运行方式：**
```bash
python examples/audio/audio_processing_sample.py
```

## 🤖 基础功能示例 (basic/)

### `chatglm_basic_usage.py`
ChatGLM 语言模型基础功能演示：
- 基础对话功能
- 参数调节演示
- 系统提示词使用
- 流式输出演示
- 配置信息展示

### `edgetts_basic_usage.py` 
EdgeTTS 语音合成基础功能演示：
- 基础文本转语音
- 不同语音角色演示
- 语速和音量调节
- 批量文本处理
- 语音文件管理

### `chatglm_tts_integration.py`
ChatGLM + EdgeTTS 集成演示：
- ChatGLM 基础功能测试
- 完整的对话+语音合成流程
- 错误处理和异常情况

**运行方式：**
```bash
python examples/basic/chatglm_basic_usage.py
python examples/basic/edgetts_basic_usage.py  
python examples/basic/chatglm_tts_integration.py
```

## 📁 目录结构

```
examples/
├── README.md                       # 本文件
├── audio/                         # 音频处理相关示例
│   └── audio_processing_sample.py # 完整音频处理流程
└── basic/                         # 基础功能示例
    ├── chatglm_basic_usage.py     # ChatGLM 基础使用
    ├── chatglm_tts_integration.py # ChatGLM + TTS 集成
    └── edgetts_basic_usage.py     # EdgeTTS 基础使用
```

## 🚀 运行示例

1. **确保环境配置：**
   ```bash
   # 回到项目根目录
   cd ../../
   
   # 检查.env配置
   cat .env.example
   ```

2. **运行音频示例：**
   ```bash
   # 进入示例目录
   cd examples/audio
   
   # 运行完整音频处理演示
   python audio_processing_sample.py
   ```

3. **查看输出：**
   - 音频转换流程日志
   - Opus字节流十六进制内容
   - 文件大小对比分析
   - 编码预设效果对比

## 📝 添加新示例

如果要添加新的示例：

1. 在相应目录下创建示例文件
2. 添加详细的文档注释
3. 更新本README文件
4. 确保示例可以独立运行

## ⚠️ 注意事项

- 所有示例都假设从项目根目录运行
- 确保已正确配置环境变量
- 某些示例可能需要特定的测试数据文件