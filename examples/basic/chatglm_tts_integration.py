"""
ChatGLM + EdgeTTS 集成使用示例

演示如何使用 ChatGLM 进行对话生成和 EdgeTTS 进行语音合成的完整流程。
包含完整的错误处理、配置管理和用户交互功能。
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def get_api_key():
    """
    获取智谱AI的API密钥
    
    Returns:
        str: API密钥
    """
    # 首先尝试从环境变量获取
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if not api_key:
        # 尝试从.env文件获取
        env_file = Path(project_root) / '.env'
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('ZHIPU_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
    
    if not api_key:
        print("❌ 未找到 ZHIPU_API_KEY")
        print("💡 请在 .env 文件中配置：ZHIPU_API_KEY=your_api_key_here")
        api_key = input("请输入您的智谱AI API密钥: ").strip()
        
        if not api_key:
            raise ValueError("API密钥不能为空")
    
    return api_key

def test_chatglm_basic():
    """测试 ChatGLM 基础功能"""
    print("� 测试 ChatGLM 基础功能...")
    print("-" * 40)
    
    try:
        from ai_core.llm.chatglm import ChatGLM
        
        # 获取API密钥
        api_key = get_api_key()
        
        # 初始化ChatGLM
        chatglm = ChatGLM.get_instance(api_key)
        
        # 基础对话测试
        test_questions = [
            "你好",
            "请用一句话介绍你自己",
            "什么是人工智能？"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n🔍 测试问题 {i}: {question}")
            response = chatglm.generate_response(question)
            print(f"✅ AI回复: {response[:50]}..." if len(response) > 50 else f"✅ AI回复: {response}")
        
        # 获取模型信息
        info = chatglm.get_model_info()
        print(f"\n📊 模型信息: {info}")
        
        print("\n✅ ChatGLM 基础功能测试完成")
        return chatglm
        
    except Exception as e:
        print(f"❌ ChatGLM 测试失败: {e}")
        raise

def test_edgetts_basic():
    """测试 EdgeTTS 基础功能"""
    print("\n🎵 测试 EdgeTTS 基础功能...")
    print("-" * 40)
    
    try:
        from ai_core.tts.edge import EdgeTTS
        
        # 初始化EdgeTTS
        tts = EdgeTTS.get_instance()
        
        # 基础语音合成测试
        test_texts = [
            "你好，这是语音合成测试。",
            "EdgeTTS语音合成功能正常。"
        ]
        
        generated_files = []
        for i, text in enumerate(test_texts, 1):
            print(f"\n🔍 合成文本 {i}: {text}")
            filename = f"test_tts_{i}.mp3"
            audio_file = tts.text_to_speech(text, filename=filename)
            generated_files.append(audio_file)
            print(f"✅ 语音文件: {audio_file}")
        
        # 显示TTS配置信息
        info = tts.get_tts_info()
        print(f"\n📊 TTS配置: {info}")
        
        print("\n✅ EdgeTTS 基础功能测试完成")
        return tts, generated_files
        
    except Exception as e:
        print(f"❌ EdgeTTS 测试失败: {e}")
        raise

def test_integration_workflow():
    """测试 ChatGLM + EdgeTTS 集成工作流"""
    print("\n🔗 测试 ChatGLM + EdgeTTS 集成工作流...")
    print("-" * 40)
    
    try:
        # 获取组件实例
        chatglm = test_chatglm_basic()
        tts, _ = test_edgetts_basic()
        
        print("\n🎯 开始集成演示...")
        
        # 集成工作流演示
        integration_scenarios = [
            {
                "user_input": "请介绍一下Python编程语言的特点",
                "voice": "zh-CN-XiaoyiNeural",
                "filename": "python_intro.mp3"
            },
            {
                "user_input": "如何学习机器学习？",
                "voice": "zh-CN-YunyangNeural", 
                "filename": "ml_learning.mp3"
            }
        ]
        
        results = []
        for i, scenario in enumerate(integration_scenarios, 1):
            print(f"\n📝 场景 {i}: {scenario['user_input']}")
            
            # ChatGLM 生成回复
            ai_response = chatglm.generate_response(scenario['user_input'])
            print(f"🤖 AI回复: {ai_response[:100]}..." if len(ai_response) > 100 else f"🤖 AI回复: {ai_response}")
            
            # EdgeTTS 语音合成
            audio_file = tts.text_to_speech(
                ai_response, 
                voice=scenario['voice'],
                filename=scenario['filename']
            )
            print(f"🎵 语音文件: {audio_file}")
            
            results.append({
                "question": scenario['user_input'],
                "answer": ai_response,
                "audio": audio_file
            })
        
        print("\n✅ 集成工作流测试完成")
        return results
        
    except Exception as e:
        print(f"❌ 集成工作流测试失败: {e}")
        raise

def interactive_demo():
    """交互式演示模式"""
    print("\n🎮 进入交互式演示模式...")
    print("-" * 40)
    print("💡 输入 'quit' 或 'exit' 退出演示")
    print("💡 输入 'config' 查看当前配置")
    print("💡 输入 'help' 显示帮助信息")
    
    try:
        from ai_core.llm.chatglm import ChatGLM
        from ai_core.tts.edge import EdgeTTS
        
        # 初始化组件
        api_key = get_api_key()
        chatglm = ChatGLM.get_instance(api_key)
        tts = EdgeTTS.get_instance()
        
        conversation_count = 0
        
        while True:
            user_input = input("\n👤 您: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 再见！")
                break
            elif user_input.lower() == 'config':
                print(f"🤖 ChatGLM配置: {chatglm.get_model_info()}")
                print(f"🎵 EdgeTTS配置: {tts.get_tts_info()}")
                continue
            elif user_input.lower() == 'help':
                print("📖 可用命令:")
                print("   - 直接输入问题进行对话")
                print("   - config: 显示当前配置")
                print("   - help: 显示此帮助")
                print("   - quit/exit: 退出演示")
                continue
            elif not user_input:
                print("💡 请输入您的问题...")
                continue
            
            try:
                conversation_count += 1
                
                # 生成AI回复
                print("🤖 AI正在思考...")
                ai_response = chatglm.generate_response(user_input)
                print(f"🤖 AI: {ai_response}")
                
                # 语音合成
                print("🎵 正在生成语音...")
                filename = f"interactive_demo_{conversation_count:03d}.mp3"
                audio_file = tts.text_to_speech(ai_response, filename=filename)
                print(f"🎵 语音已保存: {audio_file}")
                
            except Exception as e:
                print(f"❌ 处理失败: {e}")
                print("💡 请重试或检查网络连接")
        
    except Exception as e:
        print(f"❌ 交互式演示启动失败: {e}")
        raise

def main():
    """主程序入口"""
    print("🚀 ChatGLM + EdgeTTS 集成演示")
    print("=" * 60)
    print("本示例演示 ChatGLM 对话生成 + EdgeTTS 语音合成的完整集成流程")
    print("=" * 60)
    
    # 显示功能菜单
    print("📋 可用功能:")
    print("   1. 基础功能测试")
    print("   2. 集成工作流演示")  
    print("   3. 交互式演示模式")
    print("   4. 完整功能演示")
    
    choice = input("\n请选择功能 (1-4, 直接回车选择4): ").strip()
    
    try:
        if choice == "1":
            test_chatglm_basic()
            test_edgetts_basic()
        elif choice == "2":
            test_integration_workflow()
        elif choice == "3":
            interactive_demo()
        else:  # 默认选择完整演示
            print("\n🎯 运行完整功能演示...")
            test_integration_workflow()
            
            # 询问是否进入交互模式
            if input("\n是否进入交互式演示? (y/N): ").strip().lower() in ['y', 'yes']:
                interactive_demo()
        
        print("\n🎉 演示完成！")
        print("� 生成的语音文件保存在 outputs/tts/ 目录中")
        print("💡 您可以播放这些文件来体验语音合成效果")
        
    except KeyboardInterrupt:
        print("\n\n👋 用户取消，演示结束")
    except Exception as e:
        print(f"\n❌ 演示运行失败: {e}")
        print("\n💡 故障排除建议:")
        print("   1. 检查 .env 文件中的 ZHIPU_API_KEY 配置")
        print("   2. 确认网络连接正常（ChatGLM和EdgeTTS都需要网络）")
        print("   3. 验证所有依赖包已正确安装")
        print("   4. 检查系统音频相关权限")

if __name__ == "__main__":
    main()