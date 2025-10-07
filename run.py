#!/usr/bin/env python3
"""AI Server 主程序入口"""

import sys
import os
import glob
import traceback
from dotenv import load_dotenv

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 加载.env文件
load_dotenv()

# 导入所有AI模块
from ai_core.tts.edge import EdgeTTS
from ai_core.asr.funasr_wrapper import FunASR
from ai_core.llm.chatglm import ChatGLM
from ai_core.audio.audio import DownlinkProcessor, UplinkProcessor

def main():
    """主程序入口"""
    print("🚀 AI Server")
    print("1. EdgeTTS 演示")  
    print("2. FunASR 演示")
    print("3. ChatGLM 演示")
    print("4. Audio 处理演示")
    print("5. 综合演示 (Audio+ASR+LLM+TTS)")
    print("0. 退出")
    
    try:
        choice = input("\n选择功能: ").strip() or "1"
        
        if choice == "1":
            test_edge_tts()
        elif choice == "2": 
            test_funasr()
        elif choice == "3":
            test_chatglm()
        elif choice == "4":
            test_audio_processing()
        elif choice == "5":
            test_comprehensive_demo()
        elif choice == "0":
            print("退出")
        else:
            print("无效选择")
            
    except Exception as e:
        print(f"运行失败: {e}")

def test_edge_tts():
    """EdgeTTS测试"""
    try:
        tts = EdgeTTS.get_instance()
        
        # 创建输出目录
        os.makedirs("outputs/tts", exist_ok=True)
        
        text = input("🎤 请输入要合成的文字 (直接回车使用默认): ").strip()
        if not text:
            text = "你好，这是EdgeTTS语音合成测试"
        
        result = tts.text_to_speech(text, "edge_test.mp3")
        
        if result:
            print(f"✅ TTS成功: {result}")
        else:
            print("❌ TTS失败")
            
    except Exception as e:
        print(f"TTS失败: {e}")

def test_funasr():
    """FunASR测试"""
    try:
        asr = FunASR.get_instance()
        
        # 查找测试音频文件
        audio_files = glob.glob("outputs/tts/*.mp3")
        
        if audio_files:
            result = asr.transcribe_file(audio_files[0])
            print(f"ASR结果: {result}")
        else:
            print("未找到音频文件")
    except Exception as e:
        print(f"ASR失败: {e}")

def test_chatglm():
    """ChatGLM测试"""
    try:
        # 检查API密钥
        api_key = os.getenv('ZHIPU_API_KEY')
        if not api_key:
            print("❌ 未配置ZHIPU_API_KEY环境变量")
            print("💡 请设置API密钥: export ZHIPU_API_KEY=your_api_key")
            return
        
        chatglm = ChatGLM.get_instance(api_key)
        
        # 简单对话测试
        user_input = input("💬 请输入问题 (直接回车使用默认): ").strip()
        if not user_input:
            user_input = "你好，请简单介绍一下自己"
        
        print("🤖 ChatGLM正在思考...")
        response = chatglm.generate_response(user_input)
        print(f"🤖 回复: {response}")
        
    except Exception as e:
        print(f"ChatGLM失败: {e}")

def test_audio_processing():
    """Audio处理演示"""
    try:
        
        print("🎵 Audio 处理演示")
        print("=" * 40)
        
        # 创建输出目录
        os.makedirs("outputs/audio", exist_ok=True)
        
        # 查找音频文件
        audio_files = glob.glob("outputs/tts/*.mp3")
        if not audio_files:
            print("❌ 未找到音频文件，请先运行EdgeTTS演示生成音频")
            return
        
        input_file = audio_files[0]
        print(f"📁 输入文件: {input_file}")
        
        # 下行处理演示 (TTS -> Opus)
        print("\n📤 下行处理 (TTS音频 -> Opus格式)")
        downlink = DownlinkProcessor(preset="balanced")
        opus_data = downlink.process_audio(input_file, output_format="bytes")
        print(f"   Opus数据大小: {len(opus_data):,} bytes")
        
        # 上行处理演示 (Opus -> WAV)
        print("\n📥 上行处理 (Opus数据 -> WAV格式)")
        uplink = UplinkProcessor(preset="general")
        # 确保opus_data是bytes类型
        if isinstance(opus_data, bytes):
            output_file = uplink.decode_opus(opus_data, output_format="file")
        else:
            print("❌ Opus数据类型错误")
            return
        print(f"   输出文件: {output_file}")
        
        # 显示文件大小对比  
        original_size = os.path.getsize(input_file)
        opus_size = len(opus_data)
        # 确保output_file是字符串路径
        if isinstance(output_file, str):
            decoded_size = os.path.getsize(output_file)
        else:
            decoded_size = 0
        
        print(f"\n📊 文件大小对比:")
        print(f"   原始MP3: {original_size:,} bytes")
        print(f"   Opus编码: {opus_size:,} bytes (压缩 {(1-opus_size/original_size)*100:.1f}%)")
        print(f"   解码WAV: {decoded_size:,} bytes")
        
    except Exception as e:
        print(f"Audio处理失败: {e}")

def test_comprehensive_demo():
    """综合演示: Audio+ASR+LLM+TTS"""
    try:
        import os
        print("🌟 AI Server 综合演示")
        print("=" * 50)
        print("流程: 用户输入 -> TTS -> Audio处理 -> ASR -> LLM -> TTS")
        
        # 检查API密钥
        api_key = os.getenv('ZHIPU_API_KEY')
        if not api_key:
            print("❌ 需要ZHIPU_API_KEY环境变量才能运行综合演示")
            return
        
        # 创建输出目录
        os.makedirs("outputs/comprehensive", exist_ok=True)
        
        # 1. 用户输入
        user_text = input("💬 请输入一个问题 (直接回车使用默认): ").strip()
        if not user_text:
            user_text = "什么是人工智能?"
        
        print(f"\n🎯 用户问题: {user_text}")
        
        # 2. TTS - 将用户问题转为语音
        print("\n🎤 步骤1: 文字转语音 (TTS)")
        tts = EdgeTTS.get_instance()
        tts_result = tts.text_to_speech(user_text, "user_question.mp3")
        if not tts_result:
            print("❌ TTS失败")
            return
        audio_path = tts_result
        print(f"   ✅ 生成语音: {audio_path}")
        
        # 3. Audio处理 - 模拟IoT设备传输
        print("\n📡 步骤2: 音频编码传输 (Audio Processing)")
        
        # 下行: 编码为Opus
        downlink = DownlinkProcessor(preset="low_latency")
        opus_data = downlink.process_audio(audio_path, output_format="bytes")
        print(f"   📤 Opus编码: {len(opus_data):,} bytes")
        
        # 上行: 解码为WAV供ASR使用
        uplink = UplinkProcessor(preset="general")
        asr_audio_path = "outputs/comprehensive/for_asr.wav"
        # 确保opus_data是bytes类型
        if isinstance(opus_data, bytes):
            uplink.decode_to_file(opus_data, asr_audio_path)
        else:
            print("❌ Opus数据类型错误")
            return
        print(f"   📥 解码音频: {asr_audio_path}")
        
        # 4. ASR - 语音识别
        print("\n🎤 步骤3: 语音识别 (ASR)")
        asr = FunASR.get_instance()
        recognized_text = asr.transcribe_file(asr_audio_path)
        if not recognized_text:
            print("❌ ASR失败")
            return
        print(f"   🎯 识别结果: {recognized_text}")
        
        # 5. LLM - 生成回答
        print("\n🤖 步骤4: AI生成回答 (LLM)")
        chatglm = ChatGLM.get_instance(api_key)
        ai_response = chatglm.generate_response(recognized_text)
        print(f"   💡 AI回答: {ai_response}")
        
        # 6. TTS - 将AI回答转为语音
        print("\n🔊 步骤5: 回答转语音 (TTS)")
        tts_result = tts.text_to_speech(ai_response, "ai_response.mp3")
        if tts_result:
            print(f"   ✅ 回答语音: {tts_result}")
        
        print("\n🎉 综合演示完成!")
        print("📂 所有输出文件保存在: outputs/comprehensive/")
        
    except Exception as e:
        print(f"综合演示失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()