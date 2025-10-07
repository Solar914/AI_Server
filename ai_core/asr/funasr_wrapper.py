"""FunASR 语音识别封装类"""

from pathlib import Path
from typing import Optional, Union
import torch

class FunASR:
    """FunASR 语音识别封装类"""
    
    _instance = None
    
    def __init__(self, model: Optional[str] = None, device: Optional[str] = None):
        """初始化FunASR实例"""
        if model is None:
            self.model_path = Path(__file__).parent / "models"
        else:
            self.model_path = Path(model)
        self.asr_model = None
        
        # 自动检测最佳设备
        if device is None:
            device = self._detect_best_device()
        self.device = device
        print(f"🎯 FunASR 设备选择: {self.device}")
        
    def _detect_best_device(self) -> str:
        """检测最佳计算设备"""
        # 1. 优先NVIDIA GPU
        if torch.cuda.is_available():
            return "cuda"
            
        # 2. 尝试Intel GPU (XPU)
        try:
            if hasattr(torch, 'xpu') and torch.xpu.is_available():
                return "xpu"
        except:
            pass
            
        # 3. 回退到CPU
        return "cpu"
        
    @classmethod
    def get_instance(cls, model: Optional[str] = None, device: Optional[str] = None) -> 'FunASR':
        """获取FunASR单例实例"""
        if cls._instance is None:
            cls._instance = cls(model=model, device=device)
        return cls._instance
    
    def initialize_model(self):
        """初始化ASR模型"""
        if self.asr_model is not None:
            return True
            
        try:
            from funasr import AutoModel
            
            # 根据设备类型初始化模型
            if self.device == "cuda":
                print("🚀 使用NVIDIA GPU加速")
                self.asr_model = AutoModel(model=str(self.model_path), device="cuda")
            elif self.device == "xpu":
                print("🔷 使用Intel GPU加速 (实验性)")
                try:
                    import intel_extension_for_pytorch as ipex
                    self.asr_model = AutoModel(model=str(self.model_path))
                    # 尝试将模型移到XPU设备
                    # 注意：这是实验性功能，可能不完全支持
                    print("⚠️  Intel GPU支持可能有限，如遇问题请切换回CPU")
                except Exception as e:
                    print(f"⚠️  Intel GPU初始化失败，回退到CPU: {e}")
                    self.device = "cpu"
                    self.asr_model = AutoModel(model=str(self.model_path))
            else:
                print("💻 使用CPU模式")
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
