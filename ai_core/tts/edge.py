import edge_tts
import asyncio
import os
import time
from typing import Optional, List, Dict
from pathlib import Path


class EdgeTTS:
    """Edge TTS 语音合成封装类"""
    
    # 类变量用于单例模式
    _instance = None
    
    def __init__(self, voice: str = "zh-CN-XiaoyiNeural", rate: str = "+0%", volume: str = "+0%"):
        """
        初始化EdgeTTS客户端
        
        Args:
            voice: 语音角色，默认为中文女声
            rate: 语速调节，如 "+20%" 表示快20%，"-10%" 表示慢10%
            volume: 音量调节，如 "+50%" 表示大50%，"-20%" 表示小20%
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        
        # 设置默认输出目录（不预先创建）
        self.output_dir = Path("outputs/tts")
        
        # 常用中文语音列表
        self.chinese_voices = {
            "xiaoyou": "zh-CN-XiaoyouNeural",  # 中文男声
            "xiaoyi": "zh-CN-XiaoyiNeural",   # 中文女声
            "yunjian": "zh-CN-YunjianNeural", # 中文男声
            "yunxi": "zh-CN-YunxiNeural",     # 中文男声
            "yunxia": "zh-CN-YunxiaNeural",   # 中文女声
            "yunyang": "zh-CN-YunyangNeural", # 中文男声
            "xiaoxiao": "zh-CN-XiaoxiaoNeural", # 中文女声
            "xiaohan": "zh-CN-XiaohanNeural",   # 中文女声
            "xiaomo": "zh-CN-XiaomoNeural",     # 中文女声
            "xiaoxuan": "zh-CN-XiaoxuanNeural", # 中文女声
        }
    
    @classmethod
    def get_instance(cls, voice: str = None, rate: str = "+0%", volume: str = "+0%") -> 'EdgeTTS':
        """
        获取EdgeTTS单例实例
        
        Args:
            voice: 语音角色，如果已有实例则忽略
            rate: 语速调节，如果已有实例则忽略
            volume: 音量调节，如果已有实例则忽略
            
        Returns:
            EdgeTTS实例
        """
        if cls._instance is None:
            if voice is None:
                voice = "zh-CN-XiaoyiNeural"
            cls._instance = cls(voice=voice, rate=rate, volume=volume)
        return cls._instance
    
    async def _generate_speech_async(self, text: str, output_path: str) -> bool:
        """
        异步生成语音文件
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            
        Returns:
            是否生成成功
        """
        try:
            # 创建TTS通信对象
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
            
            # 生成语音文件
            await communicate.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"语音生成失败: {str(e)}")
            return False
    
    def text_to_speech(self, 
                      text: str, 
                      filename: Optional[str] = None,
                      voice: Optional[str] = None,
                      rate: Optional[str] = None,
                      volume: Optional[str] = None) -> Optional[str]:
        """
        将文本转换为语音文件
        
        Args:
            text: 要转换的文本内容
            filename: 输出文件名，不指定则自动生成
            voice: 临时使用的语音角色，不指定则使用默认
            rate: 临时语速调节，不指定则使用默认
            volume: 临时音量调节，不指定则使用默认
            
        Returns:
            生成的音频文件路径，失败时返回None
            
        Raises:
            Exception: 当语音生成失败时抛出异常
        """
        try:
            # 验证文本内容
            if not text or not text.strip():
                raise Exception("文本内容不能为空")
            
            # 生成输出文件名
            if filename is None:
                timestamp = int(time.time())
                filename = f"tts_output_{timestamp}.mp3"
            
            # 确保文件扩展名
            if not filename.endswith(('.mp3', '.wav')):
                filename += '.mp3'
            
            # 完整的输出路径
            # 如果filename包含路径分隔符，说明是完整路径
            if '/' in filename or '\\' in filename:
                output_path = Path(filename)
                # 确保目录存在
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                # 确保默认输出目录存在
                self.output_dir.mkdir(parents=True, exist_ok=True)
                output_path = self.output_dir / filename
            
            # 使用临时参数或默认参数
            current_voice = voice if voice else self.voice
            current_rate = rate if rate else self.rate
            current_volume = volume if volume else self.volume
            
            # 临时修改实例参数
            original_voice = self.voice
            original_rate = self.rate
            original_volume = self.volume
            
            self.voice = current_voice
            self.rate = current_rate
            self.volume = current_volume
            
            try:
                # 运行异步方法
                success = asyncio.run(self._generate_speech_async(text, str(output_path)))
                
                if success and output_path.exists():
                    print(f"✅ 语音文件生成成功: {output_path}")
                    return str(output_path)
                else:
                    raise Exception("语音文件生成失败")
                    
            finally:
                # 恢复原始参数
                self.voice = original_voice
                self.rate = original_rate
                self.volume = original_volume
                
        except Exception as e:
            raise Exception(f"EdgeTTS 语音生成失败: {str(e)}")
    
    def set_voice(self, voice: str):
        """设置默认语音角色"""
        self.voice = voice
    
    def set_voice_by_name(self, name: str):
        """通过简化名称设置语音角色"""
        if name.lower() in self.chinese_voices:
            self.voice = self.chinese_voices[name.lower()]
        else:
            raise ValueError(f"未找到语音角色: {name}。可用选项: {list(self.chinese_voices.keys())}")
    
    def set_speech_params(self, rate: str = None, volume: str = None):
        """设置语速和音量参数"""
        if rate:
            self.rate = rate
        if volume:
            self.volume = volume
    
    def get_available_voices(self) -> Dict[str, str]:
        """获取可用的中文语音列表"""
        return self.chinese_voices.copy()
    
    async def get_all_voices(self) -> List[Dict]:
        """异步获取所有可用语音（包括其他语言）"""
        try:
            voices = await edge_tts.list_voices()
            return voices
        except Exception as e:
            print(f"获取语音列表失败: {str(e)}")
            return []
    
    def get_tts_info(self) -> Dict:
        """获取当前TTS配置信息"""
        return {
            "voice": self.voice,
            "rate": self.rate,
            "volume": self.volume,
            "output_dir": str(self.output_dir),
            "available_chinese_voices": len(self.chinese_voices)
        }
