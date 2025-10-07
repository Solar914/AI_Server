"""
AI音频处理模块 - 设备通信音频编解码

提供两个核心处理器：
- DownlinkProcessor: TTS音频 → Opus编码 → 下位机传输
- UplinkProcessor: 下位机Opus → 音频解码 → ASR处理

音频规格：16kHz采样率，立体声，16bit位深
"""

from .audio import (
    DownlinkProcessor, UplinkProcessor, find_ffmpeg_path, get_ffmpeg_executable
)

__all__ = [
    'DownlinkProcessor',     # 下行处理器 (TTS→Opus)
    'UplinkProcessor',       # 上行处理器 (Opus→ASR)  
    'find_ffmpeg_path',      # FFmpeg路径检测工具
    'get_ffmpeg_executable'  # FFmpeg可执行文件获取
]