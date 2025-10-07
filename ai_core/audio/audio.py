#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI音频处理模块 - 设备通信音频编解码

本模块提供两个核心处理器：
1. DownlinkProcessor - 将TTS音频编码为Opus格式发送给下位机
2. UplinkProcessor   - 将下位机Opus数据解码为音频供ASR使用

音频规格：16kHz采样率，立体声(2通道)，16bit位深
支持多种质量预设，针对不同延迟和质量需求优化
"""

import os
import io
import tempfile
import subprocess
import base64
from typing import Optional, Dict, Any, Union
from pydub import AudioSegment
from dotenv import load_dotenv

# 自动加载 .env 文件，覆盖现有环境变量
load_dotenv(override=True)


def _get_audio_config() -> Dict[str, int]:
    """
    从环境变量读取音频配置参数
    
    Returns:
        Dict[str, int]: 包含采样率、声道数、位深的配置字典
    """
    return {
        'sample_rate': int(os.getenv('AUDIO_SAMPLE_RATE', '16000')),
        'channels': int(os.getenv('AUDIO_CHANNELS', '2')),
        'bit_depth': int(os.getenv('AUDIO_BIT_DEPTH', '16'))
    }


def _get_downlink_bitrates() -> Dict[str, str]:
    """
    从环境变量读取下行处理器比特率配置
    
    Returns:
        Dict[str, str]: 各预设的比特率配置
    """
    return {
        'ultra_low_latency': f"{os.getenv('DOWNLINK_ULTRA_LOW_LATENCY_BITRATE', '64')}k",
        'low_latency': f"{os.getenv('DOWNLINK_LOW_LATENCY_BITRATE', '96')}k",
        'balanced': f"{os.getenv('DOWNLINK_BALANCED_BITRATE', '128')}k",
        'high_quality': f"{os.getenv('DOWNLINK_HIGH_QUALITY_BITRATE', '192')}k"
    }


def _get_downlink_frame_durations() -> Dict[str, str]:
    """
    从环境变量读取下行处理器帧长配置
    
    Returns:
        Dict[str, str]: 各预设的帧长配置(ms)
    """
    return {
        'ultra_low_latency': os.getenv('DOWNLINK_ULTRA_LOW_LATENCY_FRAME_DURATION', '2.5'),
        'low_latency': os.getenv('DOWNLINK_LOW_LATENCY_FRAME_DURATION', '5'),
        'balanced': os.getenv('DOWNLINK_BALANCED_FRAME_DURATION', '20'),
        'high_quality': os.getenv('DOWNLINK_HIGH_QUALITY_FRAME_DURATION', '40')
    }


def find_ffmpeg_path() -> Optional[str]:
    """
    智能查找FFmpeg可执行文件路径
    
    查找顺序：
    1. 环境变量 AI_SERVER_FFMPEG_PATH 
    2. 项目根目录下的 ffmpeg/bin/
    3. 系统PATH环境变量
    
    Returns:
        Optional[str]: FFmpeg安装路径，如果在系统PATH中则返回None
    """
    # 1. 检查环境变量
    env_ffmpeg_path = os.environ.get('AI_SERVER_FFMPEG_PATH')
    if env_ffmpeg_path and os.path.exists(os.path.join(env_ffmpeg_path, "ffmpeg.exe")):
        return env_ffmpeg_path
    
    # 2. 检查项目根目录下的ffmpeg文件夹
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    
    # 向上查找项目根目录
    while current_dir != os.path.dirname(current_dir):
        for search_file in ['requirements.txt', 'README.md', '.git']:
            if os.path.exists(os.path.join(current_dir, search_file)):
                ffmpeg_dir = os.path.join(current_dir, "ffmpeg", "bin")
                if os.path.exists(os.path.join(ffmpeg_dir, "ffmpeg.exe")):
                    return ffmpeg_dir
                break
        current_dir = os.path.dirname(current_dir)
    
    # 3. 检查系统PATH
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return None  # 系统PATH中可用
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return None


def get_ffmpeg_executable() -> str:
    """
    获取FFmpeg可执行命令字符串
    
    Returns:
        str: 完整的FFmpeg命令路径或"ffmpeg"(如果在系统PATH中)
    """
    ffmpeg_path = find_ffmpeg_path()
    if ffmpeg_path:
        return os.path.join(ffmpeg_path, "ffmpeg.exe")
    return "ffmpeg"


class DownlinkProcessor:
    """
    下行处理器 - TTS音频编码为Opus格式传输给下位机
    
    功能：将TTS生成的各种格式音频文件(MP3/WAV/FLAC等)转换为
          优化的Opus格式，用于网络传输到下位机设备播放
    
    音频规格：从环境变量读取配置(默认16kHz采样率，立体声，16bit位深)
    编码格式：Opus (针对语音通信优化)
    """
    
    @classmethod
    def _get_presets(cls) -> Dict[str, Dict[str, Any]]:
        """
        获取动态预设配置 - 从环境变量读取参数
        
        Returns:
            Dict: 预设配置字典
        """
        audio_config = _get_audio_config()
        bitrates = _get_downlink_bitrates()
        frame_durations = _get_downlink_frame_durations()
        
        return {
            "ultra_low_latency": {
                **audio_config,
                "bitrate": bitrates['ultra_low_latency'],
                "frame_duration": frame_durations['ultra_low_latency'],
                "desc": "极低延迟 - 实时对讲"
            },
            "low_latency": {
                **audio_config,
                "bitrate": bitrates['low_latency'],
                "frame_duration": frame_durations['low_latency'],
                "desc": "低延迟 - 语音助手"
            },
            "balanced": {
                **audio_config,
                "bitrate": bitrates['balanced'],
                "frame_duration": frame_durations['balanced'],
                "desc": "平衡质量和延迟"
            },
            "high_quality": {
                **audio_config,
                "bitrate": bitrates['high_quality'],
                "frame_duration": frame_durations['high_quality'],
                "desc": "高质量语音"
            }
        }
    
    @property
    def PRESETS(self) -> Dict[str, Dict[str, Any]]:
        """动态获取预设配置"""
        return self._get_presets()
    
    def __init__(self, preset: str = "balanced"):
        """
        初始化下行处理器
        
        Args:
            preset (str): 质量预设名称
                - ultra_low_latency: 64kbps，极低延迟
                - low_latency: 96kbps，低延迟 
                - balanced: 128kbps，平衡质量延迟(默认)
                - high_quality: 192kbps，高质量
        
        Raises:
            ValueError: 预设名称不存在时抛出
        """
        presets = self._get_presets()
        if preset not in presets:
            raise ValueError(f"不支持的预设: {preset}. 可用预设: {list(presets.keys())}")
        
        self.preset = preset
        config = presets[preset]
        self.sample_rate = config["sample_rate"]
        self.channels = config["channels"]
        self.bitrate = config["bitrate"]
        self.bit_depth = config["bit_depth"]
        self.frame_duration = config["frame_duration"]
        self.ffmpeg_cmd = get_ffmpeg_executable()
        
        print(f"📤 下行处理器初始化:")
        print(f"   预设: {preset} - {config['desc']}")
        print(f"   参数: {self.sample_rate}Hz, {self.channels}ch, {self.bit_depth}bit, {self.bitrate}, {self.frame_duration}ms")
    
    @classmethod
    def get_all_presets(cls) -> Dict[str, str]:
        """获取所有可用预设"""
        presets = cls._get_presets()
        return {name: config["desc"] for name, config in presets.items()}
    
    def get_preset_info(self) -> Dict[str, Any]:
        """获取当前预设信息"""
        config = self._get_presets()[self.preset]
        return {
            "preset_name": self.preset,
            "description": config["desc"],
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "bitrate": self.bitrate,
            "bit_depth": self.bit_depth,
            "frame_duration": self.frame_duration
        }
    
    def _process_audio_to_opus(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        内部方法：使用FFmpeg将音频转换为Opus格式
        
        Args:
            input_path (str): 输入音频文件路径
            output_path (Optional[str]): 输出路径，None时自动生成临时文件
            
        Returns:
            str: 输出文件路径
            
        Raises:
            RuntimeError: FFmpeg执行失败时抛出
        """
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.opus')
        
        cmd = [
            self.ffmpeg_cmd,
            "-i", input_path,
            "-c:a", "libopus",
            "-b:a", self.bitrate,
            "-frame_duration", self.frame_duration,  # Opus帧长设置
            "-ar", str(self.sample_rate),
            "-ac", str(self.channels),
            "-sample_fmt", "s16",  # 16bit采样格式
            "-application", "voip",
            "-y",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Opus编码失败: {e.stderr}")
    
    def process_to_bytes(self, input_path: str) -> bytes:
        """
        处理音频文件并返回Opus字节数据
        
        Args:
            input_path: 输入音频文件路径
            
        Returns:
            bytes: Opus编码的字节数据
        """
        print(f"📁 TTS文件: {input_path}")
        
        # 加载音频并获取信息
        audio = AudioSegment.from_file(input_path)
        duration = len(audio) / 1000.0
        print(f"   原始音频: {audio.frame_rate}Hz, {audio.channels}ch, {duration:.1f}s")
        
        # 转换为Opus
        with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            self._process_audio_to_opus(input_path, temp_path)
            
            with open(temp_path, 'rb') as f:
                opus_data = f.read()
            
            print(f"📤 Opus输出: {len(opus_data):,} bytes")
            return opus_data
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def process_to_file(self, input_path: str, output_path: str) -> str:
        """
        处理音频文件并保存为Opus文件
        
        Args:
            input_path: 输入音频文件路径
            output_path: 输出Opus文件路径
            
        Returns:
            str: 输出文件路径
        """
        print(f"📁 TTS文件: {input_path}")
        print(f"📁 输出文件: {output_path}")
        
        self._process_audio_to_opus(input_path, output_path)
        
        # 获取文件大小
        file_size = os.path.getsize(output_path)
        print(f"📤 Opus文件: {file_size:,} bytes")
        
        return output_path
    
    def process_to_base64(self, input_path: str) -> str:
        """
        处理音频文件并返回Base64编码的Opus数据
        
        Args:
            input_path: 输入音频文件路径
            
        Returns:
            str: Base64编码的Opus数据
        """
        opus_bytes = self.process_to_bytes(input_path)
        b64_data = base64.b64encode(opus_bytes).decode('utf-8')
        print(f"📤 Base64输出: {len(b64_data):,} 字符")
        return b64_data
    
    def process_audio(self, input_path: str, output_format: str = "bytes") -> Union[bytes, str]:
        """
        处理音频文件为Opus格式 - 主要接口方法
        
        Args:
            input_path (str): 输入音频文件路径(支持MP3/WAV/FLAC等格式)
            output_format (str): 输出格式选择
                - "bytes": 返回Opus字节数据(默认)
                - "base64": 返回Base64编码字符串  
                - "file": 保存文件并返回文件路径
        
        Returns:
            Union[bytes, str]: 根据output_format返回相应格式的数据
        
        Raises:
            ValueError: 输出格式不支持时抛出
            RuntimeError: Opus编码失败时抛出
        """
        if output_format == "bytes":
            return self.process_to_bytes(input_path)
        elif output_format == "base64":
            return self.process_to_base64(input_path)
        elif output_format == "file":
            # 自动生成输出文件名
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"outputs/downlink_{self.preset}_{base_name}.opus"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            return self.process_to_file(input_path, output_path)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")


class UplinkProcessor:
    """
    上行处理器 - 下位机Opus数据解码为ASR音频
    
    功能：接收下位机传输的Opus编码音频数据，解码为标准
          音频格式供ASR(语音识别)系统处理
    
    音频规格：从环境变量读取配置(默认16kHz采样率，立体声，16bit位深)  
    输出格式：WAV (ASR友好格式)
    """
    
    @classmethod
    def _get_presets(cls) -> Dict[str, Dict[str, Any]]:
        """
        获取动态预设配置 - 从环境变量读取参数
        
        Returns:
            Dict: 预设配置字典
        """
        audio_config = _get_audio_config()
        
        return {
            "whisper": {
                **audio_config,
                "format": "wav",
                "desc": "Whisper ASR优化"
            },
            "general": {
                **audio_config,
                "format": "wav",
                "desc": "通用ASR格式"
            },
            "high_quality": {
                **audio_config,
                "format": "wav",
                "desc": "高质量ASR"
            }
        }
    
    @property
    def PRESETS(self) -> Dict[str, Dict[str, Any]]:
        """动态获取预设配置"""
        return self._get_presets()
    
    def __init__(self, preset: str = "general"):
        """
        初始化上行处理器
        
        Args:
            preset (str): ASR预设名称
                - whisper: Whisper ASR模型优化
                - general: 通用ASR格式(默认)
                - high_quality: 高质量ASR处理
                
        Note: 
            所有预设均输出16kHz/立体声/16bit/WAV格式
            预设间目前配置相同，为未来扩展预留
            
        Raises:
            ValueError: 预设名称不存在时抛出
        """
        presets = self._get_presets()
        if preset not in presets:
            raise ValueError(f"不支持的预设: {preset}. 可用预设: {list(presets.keys())}")
        
        self.preset = preset
        config = presets[preset]
        self.sample_rate = config["sample_rate"]
        self.channels = config["channels"]
        self.format = config["format"]
        self.bit_depth = config["bit_depth"]
        self.ffmpeg_cmd = get_ffmpeg_executable()
        
        print(f"📥 上行处理器初始化:")
        print(f"   预设: {preset} - {config['desc']}")
        print(f"   参数: {self.sample_rate}Hz, {self.channels}ch, {self.bit_depth}bit, {self.format}")
    
    @classmethod
    def get_all_presets(cls) -> Dict[str, str]:
        """获取所有可用预设"""
        return {name: config["desc"] for name, config in cls._get_presets().items()}
    
    def get_preset_info(self) -> Dict[str, Any]:
        """获取当前预设信息"""
        config = self._get_presets()[self.preset]
        return {
            "preset_name": self.preset,
            "description": config["desc"],
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "format": self.format,
            "bit_depth": self.bit_depth
        }
    
    def _decode_opus_to_audio(self, opus_data: bytes, output_path: Optional[str] = None) -> str:
        """
        内部方法：使用FFmpeg将Opus数据解码为音频文件
        
        Args:
            opus_data (bytes): Opus字节数据
            output_path (Optional[str]): 输出路径，None时自动生成临时文件
            
        Returns:
            str: 输出文件路径
            
        Raises:
            RuntimeError: FFmpeg执行失败时抛出
        """
        if output_path is None:
            output_path = tempfile.mktemp(suffix=f'.{self.format}')
        
        # 先保存Opus数据到临时文件
        with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as temp_opus:
            temp_opus.write(opus_data)
            temp_opus_path = temp_opus.name
        
        try:
            cmd = [
                self.ffmpeg_cmd,
                "-i", temp_opus_path,
                "-ar", str(self.sample_rate),
                "-ac", str(self.channels),
                "-acodec", "pcm_s16le",  # 16bit PCM编码器
                "-f", self.format,
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return output_path
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Opus解码失败: {e.stderr}")
        finally:
            if os.path.exists(temp_opus_path):
                os.unlink(temp_opus_path)
    
    def decode_to_bytes(self, opus_data: bytes) -> bytes:
        """
        解码Opus数据并返回音频字节数据
        
        Args:
            opus_data: Opus字节数据
            
        Returns:
            bytes: 解码后的音频字节数据
        """
        print(f"📁 Opus输入: {len(opus_data):,} bytes")
        
        with tempfile.NamedTemporaryFile(suffix=f'.{self.format}', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            self._decode_opus_to_audio(opus_data, temp_path)
            
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            print(f"📥 解码输出: {len(audio_data):,} bytes")
            return audio_data
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def decode_to_file(self, opus_data: bytes, output_path: str) -> str:
        """
        解码Opus数据并保存为音频文件
        
        Args:
            opus_data: Opus字节数据
            output_path: 输出音频文件路径
            
        Returns:
            str: 输出文件路径
        """
        print(f"📁 Opus输入: {len(opus_data):,} bytes")
        print(f"📁 输出文件: {output_path}")
        
        self._decode_opus_to_audio(opus_data, output_path)
        
        # 获取文件大小
        file_size = os.path.getsize(output_path)
        print(f"📥 音频文件: {file_size:,} bytes")
        
        return output_path
    
    def decode_to_audiosegment(self, opus_data: bytes) -> AudioSegment:
        """
        解码Opus数据并返回AudioSegment对象
        
        Args:
            opus_data: Opus字节数据
            
        Returns:
            AudioSegment: 音频对象
        """
        audio_bytes = self.decode_to_bytes(opus_data)
        
        # 根据格式加载AudioSegment
        if self.format == "wav":
            return AudioSegment.from_wav(io.BytesIO(audio_bytes))
        else:
            return AudioSegment.from_file(io.BytesIO(audio_bytes), format=self.format)
    
    def decode_opus(self, opus_data: bytes, output_format: str = "bytes", output_path: Optional[str] = None) -> Union[bytes, str, AudioSegment]:
        """
        解码Opus数据为音频 - 主要接口方法
        
        Args:
            opus_data (bytes): 下位机传输的Opus字节数据
            output_format (str): 输出格式选择
                - "bytes": 返回WAV音频字节数据(默认)
                - "file": 保存WAV文件并返回文件路径
                - "audiosegment": 返回AudioSegment对象供进一步处理
            output_path (Optional[str]): 当output_format为"file"时的输出路径，None时自动生成
        
        Returns:
            Union[bytes, str, AudioSegment]: 根据output_format返回相应格式的数据
            
        Raises:
            ValueError: 输出格式不支持时抛出
            RuntimeError: Opus解码失败时抛出
        """
        if output_format == "bytes":
            return self.decode_to_bytes(opus_data)
        elif output_format == "audiosegment":
            return self.decode_to_audiosegment(opus_data)
        elif output_format == "file":
            if output_path is None:
                # 自动生成输出文件名
                output_path = f"outputs/uplink_{self.preset}_decoded.{self.format}"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            else:
                # 使用提供的路径，确保目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            return self.decode_to_file(opus_data, output_path)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")


