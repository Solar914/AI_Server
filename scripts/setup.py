#!/usr/bin/env python3
"""简化的环境检查工具"""

import sys

def main():
    """检查基本环境要求"""
    # 检查Python版本
    if sys.version_info < (3, 11):
        print(f"❌ 需要Python 3.11+，当前版本: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # 检查关键依赖
    required = ['torch', 'edge_tts', 'funasr', 'soundfile', 'pydub']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ {pkg}")
        except ImportError:
            missing.append(pkg)
            print(f"❌ {pkg}")
    
    if missing:
        print(f"\n❌ 缺少依赖: {', '.join(missing)}")
        print("💡 安装命令: pip install -r requirements.txt")
        return False
    
    print("✅ 环境检查通过")
    return True

if __name__ == "__main__":
    main()