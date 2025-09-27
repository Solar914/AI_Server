import zai
from zai import ZhipuAiClient
from typing import List, Dict, Optional

class ChatGLM:
    """ChatGLM 智谱AI聊天模型封装类"""
    
    # 类变量用于单例模式
    _instance = None
    
    def __init__(self, api_key: str, model: str = "glm-4.5"):
        """
        初始化ChatGLM客户端
        
        Args:
            api_key: 智谱AI的API密钥，必须提供
            model: 使用的模型名称，默认为glm-4.5
        """
        if not api_key:
            raise ValueError("API key不能为空，请提供有效的API密钥")
        self.api_key = api_key
        self.model = model
        self.client = ZhipuAiClient(api_key=api_key)
        self.default_system_message = "你是一个有帮助的AI助手。"
    
    @classmethod
    def get_instance(cls, api_key: str, model: str = "glm-4.5") -> 'ChatGLM':
        """
        获取ChatGLM单例实例
        
        Args:
            api_key: API密钥，必须提供
            model: 模型名称，如果已有实例则忽略
            
        Returns:
            ChatGLM实例
        """
        if cls._instance is None:
            cls._instance = cls(api_key=api_key, model=model)
        return cls._instance
    
    def generate_response(self, 
                         user_message: str, 
                         system_message: Optional[str] = None,
                         temperature: Optional[float] = None,
                         max_tokens: Optional[int] = None,
                         conversation_history: Optional[List[Dict]] = None) -> str:
        """
        生成AI回复
        
        Args:
            user_message: 用户输入的消息
            system_message: 系统提示词，可选
            temperature: 生成温度，控制随机性 (0-1)，可选，不指定时使用模型默认值
            max_tokens: 最大token数量，可选
            conversation_history: 对话历史记录，可选
            
        Returns:
            AI生成的回复文本
            
        Raises:
            Exception: 当API调用失败时抛出异常
        """
        try:
            # 构建消息列表
            messages = []
            
            # 添加系统消息
            if system_message is None:
                system_message = self.default_system_message
            messages.append({
                "role": "system",
                "content": system_message
            })
            
            # 添加对话历史
            if conversation_history:
                messages.extend(conversation_history)
            
            # 添加用户消息
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # 构建请求参数
            request_params = {
                "model": self.model,
                "messages": messages,
                "stream": False  # 确保非流式响应
            }
            
            # 添加可选参数
            if temperature is not None:
                request_params["temperature"] = temperature
            
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # 调用API
            response = self.client.chat.completions.create(**request_params)
            
            # 提取并返回回复文本
            try:
                # 根据实际测试结果，response是Completion对象
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    choice = response.choices[0]
                    if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                        content = choice.message.content
                        return content if content else "响应为空"
                
                # 如果上面的方法不行，返回整个响应字符串用于调试
                return str(response)
                
            except Exception as parse_error:
                raise Exception(f"解析响应失败: {str(parse_error)}")
            
        except Exception as e:
            raise Exception(f"ChatGLM API调用失败: {str(e)}")
    
    def set_default_system_message(self, message: str):
        """设置默认系统提示词"""
        self.default_system_message = message
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            "model": self.model,
            "api_key_prefix": self.api_key[:10] + "..." if self.api_key else "未设置",
            "zai_version": zai.__version__,
            "default_system_message": self.default_system_message
        }
