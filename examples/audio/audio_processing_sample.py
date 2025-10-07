#!/usr/bin/env python3
"""
完整音频处理流程演示
MP3 → Opus(bytes) → WAV → Opus(bytes)

演示下行和上行处理器的完整工作流程
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from ai_core.audio.audio import DownlinkProcessor, UplinkProcessor

def audio_processing_sample():
    """
    音频处理完整流程演示
    """
    # 相对于项目根目录的路径
    input_file = os.path.join(project_root, "outputs", "tts", "demo_output.mp3")
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return
    
    print("🎵 音频处理完整流程演示")
    print("=" * 60)
    print(f"📁 输入文件: {input_file}")
    print()
    
    # === 第一步：MP3 → Opus (bytes) ===
    print("🔄 步骤1: MP3 → Opus编码 (下行处理)")
    print("-" * 40)
    
    # 使用balanced预设进行下行处理
    downlink_processor = DownlinkProcessor("balanced")
    opus_bytes_1 = downlink_processor.process_audio(input_file, "bytes")
    
    # 确保返回的是bytes类型
    if not isinstance(opus_bytes_1, bytes):
        print(f"❌ 错误：第一次编码返回了非bytes类型: {type(opus_bytes_1)}")
        return
        
    print(f"✅ 第一次Opus编码完成")
    print(f"   输出大小: {len(opus_bytes_1):,} bytes")
    print(f"   编码参数: {downlink_processor.sample_rate}Hz, {downlink_processor.channels}ch, {downlink_processor.bitrate}, {downlink_processor.frame_duration}ms")
    
    # 打印Opus字节流内容
    print(f"📋 Opus字节流内容 (前128字节):")
    print(f"   十六进制: {opus_bytes_1[:128].hex()}")
    print(f"   字节数组: {list(opus_bytes_1[:32])}")
    print()
    
    # === 第二步：Opus → WAV ===
    print("🔄 步骤2: Opus解码 → WAV (上行处理)")
    print("-" * 40)
    
    # 使用general预设进行上行处理
    uplink_processor = UplinkProcessor("general")
    wav_bytes = uplink_processor.decode_opus(opus_bytes_1, "bytes")
    
    # 确保返回的是bytes类型
    if not isinstance(wav_bytes, bytes):
        print(f"❌ 错误：解码返回了非bytes类型: {type(wav_bytes)}")
        return
        
    print(f"✅ Opus解码完成")
    print(f"   WAV大小: {len(wav_bytes):,} bytes")
    print(f"   解码参数: {uplink_processor.sample_rate}Hz, {uplink_processor.channels}ch, {uplink_processor.format}")
    print()
    
    # 可选：保存WAV文件用于验证
    wav_output_path = os.path.join(project_root, "outputs", "temp_decoded.wav")
    os.makedirs(os.path.dirname(wav_output_path), exist_ok=True)
    
    with open(wav_output_path, "wb") as f:
        f.write(wav_bytes)
    print(f"💾 临时WAV文件已保存: {wav_output_path}")
    print()
    
    # === 第三步：WAV → Opus (bytes) ===
    print("🔄 步骤3: WAV → Opus重新编码 (下行处理)")
    print("-" * 40)
    
    # 使用high_quality预设进行第二次编码
    downlink_processor_2 = DownlinkProcessor("high_quality")
    opus_bytes_2 = downlink_processor_2.process_audio(wav_output_path, "bytes")
    
    # 确保返回的是bytes类型
    if not isinstance(opus_bytes_2, bytes):
        print(f"❌ 错误：第二次编码返回了非bytes类型: {type(opus_bytes_2)}")
        return
    
    print(f"✅ 第二次Opus编码完成")
    print(f"   输出大小: {len(opus_bytes_2):,} bytes")
    print(f"   编码参数: {downlink_processor_2.sample_rate}Hz, {downlink_processor_2.channels}ch, {downlink_processor_2.bitrate}, {downlink_processor_2.frame_duration}ms")
    
    # 打印第二次Opus字节流内容
    print(f"📋 Opus字节流内容 (前128字节):")
    print(f"   十六进制: {opus_bytes_2[:128].hex()}")
    print(f"   字节数组: {list(opus_bytes_2[:32])}")
    print()
    
    # === 结果对比 ===
    print("📊 处理结果对比")
    print("=" * 60)
    print(f"原始MP3文件大小:     {os.path.getsize(input_file):,} bytes")
    print(f"第一次Opus编码:      {len(opus_bytes_1):,} bytes (balanced预设)")
    print(f"WAV解码文件:         {len(wav_bytes):,} bytes")
    print(f"第二次Opus编码:      {len(opus_bytes_2):,} bytes (high_quality预设)")
    print()
    
    # 计算压缩比
    mp3_size = os.path.getsize(input_file)
    opus1_ratio = (len(opus_bytes_1) / mp3_size) * 100
    opus2_ratio = (len(opus_bytes_2) / mp3_size) * 100
    wav_ratio = (len(wav_bytes) / mp3_size) * 100
    
    print("📈 相对于原始MP3的大小比例:")
    print(f"   Opus(balanced):    {opus1_ratio:.1f}%")
    print(f"   WAV(解码):         {wav_ratio:.1f}%")
    print(f"   Opus(high_quality): {opus2_ratio:.1f}%")
    print()
    
    # 预设对比
    print("⚙️  编码预设对比:")
    print(f"   balanced:    {downlink_processor.bitrate}, {downlink_processor.frame_duration}ms → {len(opus_bytes_1):,} bytes")
    print(f"   high_quality: {downlink_processor_2.bitrate}, {downlink_processor_2.frame_duration}ms → {len(opus_bytes_2):,} bytes")
    print()
    
    # === 额外测试：相同参数编码对比 ===
    print("🔬 相同参数编码对比测试")
    print("=" * 60)
    
    # 使用相同的balanced预设再次编码WAV文件
    print("🔄 使用相同balanced预设重新编码WAV...")
    downlink_processor_3 = DownlinkProcessor("balanced")
    opus_bytes_3 = downlink_processor_3.process_audio(wav_output_path, "bytes")
    
    if isinstance(opus_bytes_3, bytes):
        print(f"✅ 第三次Opus编码完成")
        print(f"   输出大小: {len(opus_bytes_3):,} bytes")
        
        print(f"📋 第三次Opus字节流内容 (前128字节):")
        print(f"   十六进制: {opus_bytes_3[:128].hex()}")
        print(f"   字节数组: {list(opus_bytes_3[:32])}")
        print()
        
        # 对比相同预设的编码结果
        print("🔍 相同预设编码结果对比:")
        print(f"   第一次 (MP3→Opus):  {len(opus_bytes_1):,} bytes")
        print(f"   第三次 (WAV→Opus):  {len(opus_bytes_3):,} bytes")
        print(f"   大小差异: {len(opus_bytes_3) - len(opus_bytes_1):+,} bytes ({((len(opus_bytes_3) - len(opus_bytes_1)) / len(opus_bytes_1) * 100):+.1f}%)")
        
        # 检查字节流是否相同
        if opus_bytes_1 == opus_bytes_3:
            print("   🎯 字节流完全相同!")
        else:
            # 找到第一个不同的字节位置
            diff_pos = next((i for i in range(min(len(opus_bytes_1), len(opus_bytes_3))) 
                           if opus_bytes_1[i] != opus_bytes_3[i]), None)
            if diff_pos is not None:
                print(f"   📍 首个差异位置: 第{diff_pos}字节")
                print(f"      第一次: 0x{opus_bytes_1[diff_pos]:02x} ({opus_bytes_1[diff_pos]})")
                print(f"      第三次: 0x{opus_bytes_3[diff_pos]:02x} ({opus_bytes_3[diff_pos]})")
            else:
                print("   📏 长度不同但前缀相同")
    print()
    
    # 清理临时文件
    if os.path.exists(wav_output_path):
        os.unlink(wav_output_path)
        print(f"\n🗑️  临时文件已清理: {wav_output_path}")
    
    print("\n✨ 音频处理流程演示完成！")

if __name__ == "__main__":
    audio_processing_sample()