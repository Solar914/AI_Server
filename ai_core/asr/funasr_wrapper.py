"""FunASR 语音识别封装类"""

from pathlib import Path
from typing import Optional, Union

class FunASR:
    """FunASR 语音识别封装类"""
    
    _instance = None
    
    def __init__(self, model: Optional[str] = None):
        """初始化FunASR实例"""
        if model is None:
            self.model_path = Path(__file__).parent / "models"
        else:
            self.model_path = Path(model)
        self.asr_model = None
        
    @classmethod
    def get_instance(cls, model: Optional[str] = None) -> 'FunASR':
        """获取FunASR单例实例"""
        if cls._instance is None:
            cls._instance = cls(model=model)
        return cls._instance
    
    def initialize_model(self):
        """初始化ASR模型"""
        if self.asr_model is not None:
            return True
            
        try:
            from funasr import AutoModel
            self.asr_model = AutoModel(model=str(self.model_path))
            return True
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
    def transcribe_file(self, audio_file: Union[str, Path]) -> Optional[str]:
        """识别音频文件"""
        try:
            if not self.initialize_model():
                return None
            
            audio_path = Path(audio_file)
            if not audio_path.exists():
                return None
            
            result = self.asr_model.generate(input=str(audio_path))
            return result[0]["text"] if result and len(result) > 0 else None
                
        except Exception:
            return None
    
    def transcribe_audio_data(self, audio_data, sample_rate: int = 16000) -> Optional[str]:
        """识别音频数据"""
        try:
            if not self.initialize_model():
                return None
            
            result = self.asr_model.generate(input=audio_data)
            return result[0]["text"] if result and len(result) > 0 else None
                
        except Exception:
            return None
