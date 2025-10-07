#!/usr/bin/env python3
"""AI Server 主程序入口"""

import sys
import os
import glob
import traceback
from datetime import datetime
import json
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

class TestSessionManager:
    """测试会话管理器 - 负责保存测试输出和结果"""
    
    def __init__(self):
        """初始化测试会话"""
        self.session_time = datetime.now()
        self.timestamp = self.session_time.strftime("%Y%m%d_%H%M%S")
        self.test_results = {}
        self.created_folders = set()  # 记录已创建的case文件夹
        
        # 确保outputs目录存在
        os.makedirs("outputs", exist_ok=True)
    
    def log_test_result(self, test_name, result_data):
        """记录测试结果"""
        self.test_results[test_name] = {
            'timestamp': datetime.now().isoformat(),
            'result': result_data
        }
        
    def get_case_path(self, case_name):
        """获取指定case的输出路径（按需创建文件夹）"""
        path = f"outputs/{self.timestamp}/{case_name}"
        if case_name not in self.created_folders:
            os.makedirs(path, exist_ok=True)
            self.created_folders.add(case_name)
            print(f"📁 创建测试输出文件夹: {path}")
        return path
    
    def save_session_summary(self):
        """保存测试会话总结"""
        summary = {
            'session_info': {
                'start_time': self.session_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'timestamp': self.timestamp,
                'created_cases': list(self.created_folders)
            },
            'test_results': self.test_results
        }
        
        summary_file = f"outputs/{self.timestamp}/test_summary.json"
        os.makedirs(f"outputs/{self.timestamp}", exist_ok=True)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 测试会话总结已保存: {summary_file}")
        return summary_file

# 全局测试会话管理器
test_session = TestSessionManager()

def get_performance_tips(inference_time, has_cuda):
    """生成性能优化建议"""
    tips = []
    
    # GPU相关建议
    if not has_cuda:
        tips.append("� **GPU加速选项**:")
        
        # Intel GPU 优化建议
        tips.append("🔹 **Intel Iris显卡用户**:")
        tips.append("   1. Intel XPU支持 (实验性，提升有限 ~20-30%):")
        tips.append("      pip install intel-extension-for-pytorch")
        tips.append("      pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu")
        tips.append("   ⚠️  注意: Intel GPU对AI模型支持有限，效果不如NVIDIA GPU")
        
        tips.append("🔹 **NVIDIA GPU用户 (最佳选择)**:")
        tips.append("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        tips.append("   🚀 性能提升: 5-10倍 (强烈推荐)")
        
        tips.append("🔹 **CPU优化 (当前方案)**:")
        tips.append("   - 确保使用所有CPU核心")
        tips.append("   - 关闭其他占用CPU的程序")
        tips.append("   - 使用更短的音频片段")
    
    # 速度分级建议  
    if inference_time > 8.0:
        tips.append("🐌 **推理很慢** (>8秒):")
        tips.append("   - Intel Iris: 预计提升20-30% → 约6-7秒")
        tips.append("   - NVIDIA GPU: 预计提升500-1000% → 约1-2秒")
        tips.append("   - 音频分割: <30秒片段处理")
    elif inference_time > 5.0:
        tips.append("🐌 **推理较慢** (5-8秒):")
        tips.append("   - Intel Iris: 可尝试，但提升有限")
        tips.append("   - 建议使用独立NVIDIA显卡")
    elif inference_time > 2.0:
        tips.append("⚡ **可优化** (2-5秒):")
        tips.append("   - 性能已较好，GPU优化可选")
    elif inference_time < 1.0:
        tips.append("🎉 **性能优秀** (<1秒)!")
        
    # Intel Iris 专用建议
    tips.append("🔷 **Intel Iris显卡说明**:")
    tips.append("   - Intel GPU主要用于视频编解码，AI推理能力有限")
    tips.append("   - FunASR等语音模型对Intel GPU支持不完善")
    tips.append("   - 预期性能提升: 20-30% (相比纯CPU)")
    tips.append("   - 仍建议使用NVIDIA GPU获得最佳性能")
        
    # 通用优化建议
    tips.append("📊 **通用优化**:")
    tips.append("   - 批量处理多个文件")
    tips.append("   - 使用16kHz采样率音频")
    tips.append("   - 监控CPU/GPU使用率")
    
    return tips

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
        print("🎤 EdgeTTS 测试")
        print("=" * 40)
        
        tts = EdgeTTS.get_instance()
        
        # 使用EdgeTTS case文件夹
        tts_folder = test_session.get_case_path("EdgeTTS")
        
        text = input("🎤 请输入要合成的文字 (直接回车使用默认): ").strip()
        if not text:
            text = "你好，这是EdgeTTS语音合成测试"
        
        # 保存到会话文件夹
        output_filename = f"edgetts_test_{datetime.now().strftime('%H%M%S')}.mp3"
        output_path = os.path.join(tts_folder, output_filename)
        
        # EdgeTTS现在支持完整路径
        result = tts.text_to_speech(text, output_path)
        
        test_result = {
            'test_type': 'EdgeTTS',
            'input_text': text,
            'output_file': result,
            'status': 'success' if result else 'failed'
        }
        
        if result:
            print(f"✅ TTS成功: {result}")
            print(f"📁 文件保存至: {result}")
        else:
            print("❌ TTS失败")
            
        # 记录测试结果
        test_session.log_test_result('EdgeTTS', test_result)
            
    except Exception as e:
        print(f"❌ TTS失败: {e}")
        test_session.log_test_result('EdgeTTS', {
            'test_type': 'EdgeTTS',
            'status': 'error',
            'error': str(e)
        })

def test_funasr():
    """FunASR测试"""
    import time
    import torch
    
    try:
        print("🎤 FunASR 语音识别测试")
        print("=" * 40)
        
        # 显示系统信息
        print(f"🖥️  设备信息:")
        print(f"   CPU核心数: {os.cpu_count()}")
        print(f"   CUDA可用: {'✅' if torch.cuda.is_available() else '❌'}")
        if torch.cuda.is_available():
            print(f"   GPU设备: {torch.cuda.get_device_name()}")
            print(f"   GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        
        # 初始化ASR（测量初始化时间）
        print(f"\n⏱️  模型加载中...")
        start_time = time.time()
        asr = FunASR.get_instance()
        init_time = time.time() - start_time
        print(f"   初始化耗时: {init_time:.2f}秒")
        
        # 查找测试音频文件（优先从当前会话的EdgeTTS，然后是所有时间戳文件夹）
        session_audio_files = glob.glob(f"outputs/{test_session.timestamp}/EdgeTTS/*.mp3")
        general_audio_files = glob.glob("outputs/*/EdgeTTS/*.mp3")
        
        audio_files = session_audio_files + general_audio_files
        
        if not audio_files:
            print("❌ 未找到测试音频文件，请先运行EdgeTTS演示")
            return
            
        audio_file = audio_files[0]
        # 获取音频文件信息
        file_size = os.path.getsize(audio_file) / 1024
        print(f"\n📁 音频文件: {os.path.basename(audio_file)}")
        print(f"   文件大小: {file_size:.1f} KB")
        
        # 执行ASR识别（测量推理时间）
        print(f"\n🔄 开始识别...")
        start_time = time.time()
        result = asr.transcribe_file(audio_file)
        inference_time = time.time() - start_time
        
        print(f"✅ 识别完成!")
        print(f"🎯 识别结果: {result}")
        print(f"⏱️  推理耗时: {inference_time:.2f}秒")
        
        # 保存ASR结果
        asr_folder = test_session.get_case_path("FunASR")
        
        result_file = os.path.join(asr_folder, "recognition_result.txt")
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(f"FunASR语音识别结果\n")
            f.write(f"=" * 30 + "\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"音频文件: {audio_file}\n")
            f.write(f"文件大小: {file_size:.1f} KB\n")
            f.write(f"识别结果: {result}\n")
            f.write(f"初始化耗时: {init_time:.2f}秒\n")
            f.write(f"推理耗时: {inference_time:.2f}秒\n")
            if result:
                chars_per_sec = len(result) / inference_time if inference_time > 0 else 0
                f.write(f"性能指标: {chars_per_sec:.1f} 字符/秒\n")
        
        print(f"📄 识别结果已保存到: {result_file}")
        
        # 计算性能指标
        if result:
            chars_per_sec = len(result) / inference_time if inference_time > 0 else 0
            print(f"📊 性能指标: {chars_per_sec:.1f} 字符/秒")
        
        # 详细的性能分析和建议
        print(f"\n� 性能分析报告:")
        print(f"   📝 总耗时: {init_time + inference_time:.2f}秒 (初始化: {init_time:.2f}s + 推理: {inference_time:.2f}s)")
        
        # 获取性能等级
        if inference_time < 1.0:
            level = "🎉 优秀"
        elif inference_time < 2.0:
            level = "✅ 良好"  
        elif inference_time < 5.0:
            level = "⚡ 一般"
        else:
            level = "🐌 较慢"
            
        print(f"   🏆 性能等级: {level}")
        
        # 显示优化建议
        print(f"\n💡 性能优化建议:")
        tips = get_performance_tips(inference_time, torch.cuda.is_available())
        for tip in tips:
            print(f"   {tip}")
        
    except Exception as e:
        print(f"❌ ASR失败: {e}")
        traceback.print_exc()

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
        
        # 保存ChatGLM对话结果
        chatglm_folder = test_session.get_case_path("ChatGLM")
        
        chat_file = os.path.join(chatglm_folder, "conversation.txt")
        with open(chat_file, "w", encoding="utf-8") as f:
            f.write(f"ChatGLM对话记录\n")
            f.write(f"=" * 30 + "\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"用户问题: {user_input}\n")
            f.write(f"AI回复: {response}\n")
        
        print(f"📄 对话记录已保存到: {chat_file}")
        
    except Exception as e:
        print(f"ChatGLM失败: {e}")

def test_audio_processing():
    """Audio处理演示"""
    try:
        
        print("🎵 Audio 处理演示")
        print("=" * 40)
        
        # 查找音频文件（从所有时间戳文件夹的EdgeTTS子文件夹中查找）
        audio_files = glob.glob("outputs/*/EdgeTTS/*.mp3")
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
        
        # 保存音频处理结果 - 先获取case文件夹
        audio_folder = test_session.get_case_path("Audio")
        
        # 上行处理演示 (Opus -> WAV) - 直接保存到case文件夹
        print("\n📥 上行处理 (Opus数据 -> WAV格式)")
        uplink = UplinkProcessor(preset="general")
        session_wav_file = os.path.join(audio_folder, "decoded.wav")
        
        # 确保opus_data是bytes类型
        if isinstance(opus_data, bytes):
            output_file = uplink.decode_opus(opus_data, output_format="file", output_path=session_wav_file)
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
        
        # 保存处理报告
        report_file = os.path.join(audio_folder, "processing_report.txt")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"音频处理测试报告\n")
            f.write(f"=" * 30 + "\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"输入文件: {input_file}\n")
            f.write(f"输出文件: {output_file}\n")
            f.write(f"原始MP3大小: {original_size:,} bytes\n")
            f.write(f"Opus编码大小: {opus_size:,} bytes\n")
            f.write(f"压缩比例: {(1-opus_size/original_size)*100:.1f}%\n")
            f.write(f"解码WAV大小: {decoded_size:,} bytes\n")
        
        # 保存Opus数据
        opus_file = os.path.join(audio_folder, "encoded.opus")
        with open(opus_file, "wb") as f:
            f.write(opus_data)
            
        print(f"📄 处理报告已保存到: {report_file}")
        print(f"📄 编码文件已保存到: {opus_file}")
        
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
        
        # 1. 用户输入
        user_text = input("💬 请输入一个问题 (直接回车使用默认): ").strip()
        if not user_text:
            user_text = "什么是人工智能?"
        
        print(f"\n🎯 用户问题: {user_text}")
        
        # 2. TTS - 将用户问题转为语音
        print("\n🎤 步骤1: 文字转语音 (TTS)")
        tts = EdgeTTS.get_instance()
        # 获取综合演示的输出文件夹
        comp_folder = test_session.get_case_path("Comprehensive")
        user_audio_path = os.path.join(comp_folder, "user_question.mp3")
        tts_result = tts.text_to_speech(user_text, user_audio_path)
        if not tts_result:
            print("❌ TTS失败")
            return
        audio_path = user_audio_path
        print(f"   ✅ 生成语音: {audio_path}")
        
        # 3. Audio处理 - 模拟IoT设备传输
        print("\n📡 步骤2: 音频编码传输 (Audio Processing)")
        
        # 下行: 编码为Opus
        downlink = DownlinkProcessor(preset="low_latency")
        opus_data = downlink.process_audio(audio_path, output_format="bytes")
        print(f"   📤 Opus编码: {len(opus_data):,} bytes")
        
        # 上行: 解码为WAV供ASR使用
        uplink = UplinkProcessor(preset="general")
        # 保存到Comprehensive文件夹中
        asr_audio_path = os.path.join(comp_folder, "for_asr.wav")
        # 确保opus_data是bytes类型
        if isinstance(opus_data, bytes):
            uplink.decode_to_file(opus_data, asr_audio_path)
        else:
            print("❌ Opus数据类型错误")
            return
        print(f"   📥 解码音频: {asr_audio_path}")
        
        # 4. ASR - 语音识别
        print("\n🎤 步骤3: 语音识别 (ASR)")
        import time
        asr = FunASR.get_instance()
        
        print("   ⏱️ 开始识别...")
        start_time = time.time()
        recognized_text = asr.transcribe_file(asr_audio_path)
        asr_time = time.time() - start_time
        
        if not recognized_text:
            print("❌ ASR失败")
            return
        print(f"   🎯 识别结果: {recognized_text}")
        print(f"   ⚡ ASR耗时: {asr_time:.2f}秒")
        
        # 5. LLM - 生成回答
        print("\n🤖 步骤4: AI生成回答 (LLM)")
        chatglm = ChatGLM.get_instance(api_key)
        ai_response = chatglm.generate_response(recognized_text)
        print(f"   💡 AI回答: {ai_response}")
        
        # 6. TTS - 将AI回答转为语音
        print("\n🔊 步骤5: 回答转语音 (TTS)")
        ai_audio_path = os.path.join(comp_folder, "ai_response.mp3") 
        tts_result = tts.text_to_speech(ai_response, ai_audio_path)
        if tts_result:
            print(f"   ✅ 回答语音: {tts_result}")
        
        # 保存综合报告
        demo_report_file = os.path.join(comp_folder, "demo_report.txt")
        with open(demo_report_file, "w", encoding="utf-8") as f:
            f.write(f"AI Server 综合演示报告\n")
            f.write(f"=" * 40 + "\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"流程: 用户输入 -> TTS -> Audio处理 -> ASR -> LLM -> TTS\n\n")
            f.write(f"1. 用户问题: {user_text}\n")
            f.write(f"2. TTS生成语音: {audio_path}\n")
            f.write(f"3. Opus编码大小: {len(opus_data):,} bytes\n")
            f.write(f"4. 解码音频: {asr_audio_path}\n")
            f.write(f"5. ASR识别结果: {recognized_text}\n")
            f.write(f"6. ASR耗时: {asr_time:.2f}秒\n")
            f.write(f"7. AI回答: {ai_response}\n")
            f.write(f"8. 回答语音: {tts_result}\n")
        
        # 文件已直接生成到正确位置，无需复制
        
        print("\n🎉 综合演示完成!")
        print(f"📄 演示报告已保存到: {demo_report_file}")
        print(f"📂 所有输出文件保存在: {comp_folder}/")
        
    except Exception as e:
        print(f"综合演示失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()