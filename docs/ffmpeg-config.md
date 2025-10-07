# FFmpeg 路径配置说明

## 🎯 优化内容

音频处理模块 (`ai_core/audio/audio.py`) 已经优化了FFmpeg路径检测，不再依赖硬编码的绝对路径，具有更好的可移植性和灵活性。

## 🔧 路径检测优先级

音频处理模块按以下优先级查找FFmpeg：

### 1. **系统PATH** (最高优先级)
```bash
# Windows
where ffmpeg

# Linux/macOS  
which ffmpeg
```

### 2. **环境变量配置**
```bash
# Windows
set AI_SERVER_FFMPEG_PATH=D:\your\ffmpeg\path\bin

# Linux/macOS
export AI_SERVER_FFMPEG_PATH=/your/ffmpeg/path/bin
```

### 3. **项目相对路径** (自动检测)
支持以下目录结构：
```
项目根目录/
├── tools/ffmpeg-master-latest-win64-gpl/bin/  ← 当前使用
├── tools/ffmpeg/bin/
├── tools/ffmpeg-win64/bin/
├── bin/ffmpeg/
├── ffmpeg/bin/
├── external/ffmpeg/bin/
└── vendor/ffmpeg/bin/
```

## 🚀 部署建议

### **方案A: 系统PATH (推荐)**
```bash
# 1. 下载FFmpeg到任意位置
# 2. 将bin目录添加到系统PATH
# 3. 重启VS Code
```

### **方案B: 环境变量**
```bash
# Windows
set AI_SERVER_FFMPEG_PATH=D:\tools\ffmpeg\bin

# Linux/macOS
echo 'export AI_SERVER_FFMPEG_PATH=/opt/ffmpeg/bin' >> ~/.bashrc
source ~/.bashrc
```

### **方案C: 项目相对路径**
```bash
# 将FFmpeg放置在项目目录下
项目/tools/ffmpeg/bin/ffmpeg.exe
```

## 📊 兼容性

- ✅ **Windows**: 支持 ffmpeg.exe
- ✅ **Linux/macOS**: 支持 ffmpeg
- ✅ **相对路径**: 自动检测项目根目录
- ✅ **绝对路径**: 支持环境变量配置
- ✅ **回退机制**: 多层检测确保可用性

## 🔍 检查配置

使用以下代码检查当前配置：

```python
from ai_core.audio import find_ffmpeg_path, get_ffmpeg_executable

# 检查路径配置
ffmpeg_path = find_ffmpeg_path()
ffmpeg_exe = get_ffmpeg_executable()

print(f"FFmpeg路径: {ffmpeg_path or 'System PATH'}")
print(f"可执行文件: {ffmpeg_exe}")
```

## 🆕 新增功能

1. **智能路径检测**: 自动查找项目根目录
2. **环境变量支持**: `AI_SERVER_FFMPEG_PATH`
3. **跨平台兼容**: Windows/Linux/macOS
4. **多路径支持**: 7种常见目录结构
5. **回退机制**: 确保在各种环境下都能工作

## 🔧 故障排除

如果遇到FFmpeg找不到的问题：

1. **检查系统PATH**: `where ffmpeg` (Windows) 或 `which ffmpeg` (Linux)
2. **设置环境变量**: `AI_SERVER_FFMPEG_PATH=your_path`
3. **放置到项目目录**: `tools/ffmpeg/bin/ffmpeg.exe`
4. **重启VS Code**: 刷新环境变量

优化后的代码具有更好的可移植性，可以在不同的开发环境中无缝工作！