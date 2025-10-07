#!/usr/bin/env python3
"""
AI Server 环境检查和设置脚本
"""

import os
import subprocess
import sys

def check_environment():
    """检查项目环境状态"""
    print("🔍 AI Server 环境检查")
    print("=" * 40)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 检查Python版本
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ 是必需的")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    
    # 检查虚拟环境
    venv_path = os.path.join(project_root, "AI_Server")
    if os.path.exists(venv_path):
        print("✅ 虚拟环境已存在")
    else:
        print("❌ 虚拟环境不存在")
        return False
    
    # 检查.env文件
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        print("✅ .env文件已存在")
        
        # 检查是否配置了API密钥
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'ZHIPU_API_KEY=' in content and 'your_api_key_here' not in content:
                    print("✅ API密钥已配置")
                else:
                    print("⚠️  请在.env文件中配置ZHIPU_API_KEY")
        except UnicodeDecodeError:
            print("⚠️  .env文件编码问题，请检查文件格式")
    else:
        print("❌ .env文件不存在，请复制.env.example")
        return False
    
    # 检查主要依赖
    try:
        import zai
        print("✅ zai-sdk 已安装")
    except ImportError:
        print("❌ zai-sdk 未安装")
        return False
    
    try:
        import edge_tts
        print("✅ edge-tts 已安装")
    except ImportError:
        print("❌ edge-tts 未安装")
        return False
    
    print("\n🎉 环境检查完成！")
    return True

def install_missing_dependencies():
    """安装缺失的依赖"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 确定pip路径
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(project_root, "AI_Server", "Scripts", "pip.exe")
    else:  # Unix/Linux/MacOS
        pip_path = os.path.join(project_root, "AI_Server", "bin", "pip")
    
    requirements_path = os.path.join(project_root, "requirements.txt")
    
    if os.path.exists(pip_path) and os.path.exists(requirements_path):
        print("\n📦 重新安装依赖包...")
        subprocess.run([pip_path, "install", "-r", requirements_path])
        print("✅ 依赖安装完成")
    else:
        print("❌ 找不到pip或requirements.txt")

def main():
    """主函数"""
    if check_environment():
        print("💡 环境状态良好，可以直接运行: python run.py")
    else:
        print("\n❓ 是否尝试修复环境？(y/N): ", end="")
        choice = input().strip().lower()
        if choice in ['y', 'yes']:
            install_missing_dependencies()
            print("\n🔄 请重新运行检查: python scripts/setup.py")
        else:
            print("💡 请手动修复上述问题后再运行项目")

if __name__ == "__main__":
    main()