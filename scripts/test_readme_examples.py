"""
测试 README 中的示例代码是否正确
"""

def test_chatglm_example():
    """测试 ChatGLM 示例代码"""
    print("🧪 测试 ChatGLM 示例...")
    
    import sys
    import os
    # 添加项目根目录到路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from ai_core.llm.chatglm import ChatGLM
    from src.main import get_api_key
    
    # 方式2: 使用主程序的API key获取函数
    api_key = get_api_key()  # 会从.env文件或用户输入获取
    chatglm = ChatGLM.get_instance(api_key)
    
    # 基础对话测试
    response = chatglm.generate_response("你好")
    print(f"✅ 基础对话测试通过: {response[:20]}...")
    
    # 获取模型信息
    info = chatglm.get_model_info()
    print(f"✅ 模型信息获取成功: {info['model']}")

def test_integration_example():
    """测试集成使用示例"""
    print("\n🧪 测试集成示例...")
    
    import sys
    import os
    # 添加项目根目录到路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from ai_core.llm.chatglm import ChatGLM
    from ai_core.tts.edge import EdgeTTS
    from src.main import get_api_key
    
    # 获取API密钥
    api_key = get_api_key()
    
    # 初始化
    chatglm = ChatGLM.get_instance(api_key)
    tts = EdgeTTS.get_instance()
    
    # 对话生成
    user_question = "请用一句话介绍人工智能"
    ai_response = chatglm.generate_response(user_question)
    print(f"✅ AI对话生成成功: {ai_response}")
    
    # 语音合成
    audio_file = tts.text_to_speech(ai_response, filename="test_integration.mp3")
    print(f"✅ 语音合成成功: {audio_file}")

if __name__ == "__main__":
    print("🚀 测试 README 示例代码...")
    print("=" * 50)
    
    try:
        test_chatglm_example()
        test_integration_example()
        print("\n🎉 所有示例代码测试通过！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")