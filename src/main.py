from ai_core.llm.chatglm import ChatGLM
from ai_core.tts.edge import EdgeTTS
import time
import os
import getpass
from dotenv import load_dotenv


def get_api_key():
    """获取API密钥的函数"""
    # 加载.env文件
    load_dotenv()
    
    # 从.env文件中获取
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if api_key:
        print(f"✅ 从.env文件获取到API密钥: {api_key[:10]}...")
        return api_key
    
    # 如果.env文件中没有，提示用户输入
    print("🔑 请输入您的智谱AI API密钥:")
    print("💡 提示: 可以在项目根目录创建 .env 文件并添加: ZHIPU_API_KEY=你的密钥")
    
    # 使用input获取用户输入
    api_key = input("API密钥: ").strip()
    
    if not api_key:
        raise ValueError("API密钥不能为空!")
    
    return api_key


def hello_world():
    """打印Hello World的函数"""
    print("=" * 50)
    print("🚀 AI Server - ChatGLM + EdgeTTS 演示")
    print("=" * 50)


def simple_chatglm_tts_demo():
    """简单的ChatGLM + EdgeTTS演示"""
    print("\n🎯 ChatGLM + EdgeTTS 简单演示")
    print("-" * 40)
    
    try:
        # 获取API密钥
        api_key = get_api_key()
        
        # 初始化ChatGLM和EdgeTTS
        print("📝 正在初始化AI组件...")
        chatglm = ChatGLM.get_instance(api_key)
        tts = EdgeTTS.get_instance()
        print("✅ 初始化完成")
        
        # 用户问题
        user_question = "请简单介绍一下你自己，控制在50字以内"
        print(f"\n❓ 问题: {user_question}")
        
        # ChatGLM生成回复
        print("🤖 正在生成AI回复...")
        ai_response = chatglm.generate_response(user_question, system_message="你是一个卡车司机", temperature=0.7)
        print(f"💬 AI回复: {ai_response}")
        
        # EdgeTTS生成语音
        print("\n🎵 正在生成语音文件...")
        audio_path = tts.text_to_speech(ai_response, filename="demo_output.mp3", voice="zh-CN-XiaoyouNeural", rate="+0%", volume="+0%")
        
        if audio_path:
            print(f"🎉 演示完成! 语音文件: {audio_path}")
        else:
            print("❌ 语音生成失败")
            
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {str(e)}")
        return False


def test_generate_response():
    """测试ChatGLM的generate_response方法"""
    print("\n📝 正在初始化ChatGLM...")
    
    try:
        # 获取API密钥
        api_key = get_api_key()
        
        # 获取ChatGLM实例
        chatglm = ChatGLM.get_instance(api_key)
        print("✅ ChatGLM实例创建成功")
        
        # 显示模型信息
        model_info = chatglm.get_model_info()
        print(f"📊 模型信息: {model_info['model']}")
        print(f"📚 库版本: {model_info['zai_version']}")
        
        print("\n" + "=" * 30 + " 测试用例 " + "=" * 30)
        
        # 测试用例1: 基础对话
        print("\n🔵 测试用例1: 基础对话")
        print("-" * 40)
        user_input = "你好，请简单介绍一下你自己"
        print(f"👤 用户输入: {user_input}")
        
        start_time = time.time()
        response = chatglm.generate_response(user_input, temperature=0.7)
        end_time = time.time()
        
        print(f"🤖 AI回复: {response}")
        print(f"⏱️  响应时间: {end_time - start_time:.2f}秒")
        
        # 测试用例2: 自定义系统提示词
        print("\n🔴 测试用例2: 自定义系统提示词")
        print("-" * 40)
        user_input = "请告诉我今天的天气怎么样"
        system_msg = "你是一个幽默风趣的AI助手，喜欢用表情符号，但要诚实地告诉用户你无法获取实时信息。"
        print(f"👤 用户输入: {user_input}")
        print(f"🛠️  系统提示: {system_msg}")
        
        start_time = time.time()
        response = chatglm.generate_response(
            user_message=user_input,
            system_message=system_msg,
            temperature=0.8
        )
        end_time = time.time()
        
        print(f"🤖 AI回复: {response}")
        print(f"⏱️  响应时间: {end_time - start_time:.2f}秒")
        
        # 测试用例3: 对话历史
        print("\n🟢 测试用例3: 带对话历史")
        print("-" * 40)
        conversation_history = [
            {"role": "user", "content": "我叫小明"},
            {"role": "assistant", "content": "你好小明！很高兴认识你。"}
        ]
        user_input = "你还记得我的名字吗？"
        print(f"📜 对话历史: {len(conversation_history)} 条消息")
        print(f"👤 用户输入: {user_input}")
        
        start_time = time.time()
        response = chatglm.generate_response(
            user_message=user_input,
            conversation_history=conversation_history,
            temperature=0.6
        )
        end_time = time.time()
        
        print(f"🤖 AI回复: {response}")
        print(f"⏱️  响应时间: {end_time - start_time:.2f}秒")
        
        # 测试用例4: 低温度设置
        print("\n🟡 测试用例4: 低温度设置 (更稳定)")
        print("-" * 40)
        user_input = "请用一句话总结人工智能的定义"
        print(f"👤 用户输入: {user_input}")
        print("🌡️  温度设置: 0.1 (更稳定、一致)")
        
        start_time = time.time()
        response = chatglm.generate_response(
            user_message=user_input,
            temperature=0.1
        )
        end_time = time.time()
        
        print(f"🤖 AI回复: {response}")
        print(f"⏱️  响应时间: {end_time - start_time:.2f}秒")
        
        print("\n" + "=" * 60)
        print("✅ 所有测试用例执行完成!")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False
    
    return True


def main():
    """主函数"""
    hello_world()
    
    # 执行简单的ChatGLM + EdgeTTS演示
    print("\n🚀 开始演示...")
    success = simple_chatglm_tts_demo()
    
    if success:
        print("\n🎉 演示完成!")
    else:
        print("\n💥 演示失败，请检查错误信息")
    
    print("\n👋 程序结束")


if __name__ == "__main__":
    main()