#!/usr/bin/env python3
"""
AI Server 主程序入口

提供 ChatGLM + EdgeTTS 集成服务的启动入口
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """主程序入口"""
    print("🚀 AI Server - ChatGLM + EdgeTTS 集成服务")
    print("=" * 50)
    
    # 显示菜单
    print("📋 可用功能:")
    print("   1. ChatGLM + EdgeTTS 集成演示")
    print("   2. 基础功能测试")
    print("   3. 音频处理演示")
    print("   0. 退出")
    
    try:
        choice = input("\n请选择功能 (0-3, 默认1): ").strip() or "1"
        
        if choice == "1":
            print("\n🔗 启动 ChatGLM + EdgeTTS 集成演示")
            from examples.basic.chatglm_tts_integration import main as demo_main
            demo_main()
        elif choice == "2":
            print("\n🧪 运行基础功能测试")
            test_basic_functions()
        elif choice == "3":
            print("\n🎵 启动音频处理演示")
            try:
                import examples.audio.audio_processing_sample
                print("✅ 音频处理演示已运行")
            except ImportError:
                print("❌ 音频处理示例未找到")
        elif choice == "0":
            print("👋 再见！")
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户取消，程序退出")
    except Exception as e:
        print(f"\n❌ 程序运行失败: {e}")

def test_basic_functions():
    """基础功能测试"""
    try:
        # 测试 EdgeTTS
        print("🎵 测试 EdgeTTS...")
        from ai_core.tts.edge import EdgeTTS
        tts = EdgeTTS.get_instance()
        print("   ✅ EdgeTTS 初始化成功")
        
        # 测试 ChatGLM
        print("🤖 测试 ChatGLM...")
        api_key = os.getenv('ZHIPU_API_KEY')
        if api_key:
            from ai_core.llm.chatglm import ChatGLM
            chatglm = ChatGLM.get_instance(api_key)
            print("   ✅ ChatGLM 初始化成功")
        else:
            print("   ⚠️ 未配置 ZHIPU_API_KEY")
        
        print("✅ 基础功能测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

# 命令行支持
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == "--demo":
        from examples.basic.chatglm_tts_integration import main as demo_main
        demo_main()
    elif arg == "--test":
        test_basic_functions()
    else:
        print("💡 用法: python run.py [--demo|--test]")
else:
    if __name__ == "__main__":
        main()

if __name__ == "__main__":
    main()