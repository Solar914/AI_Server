#!/usr/bin/env python3
"""
AI Server 环境设置脚本
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ 是必需的")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def setup_virtual_env():
    """设置虚拟环境"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    venv_path = os.path.join(project_root, "AI_Server")
    
    if not os.path.exists(venv_path):
        print("🔧 创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], cwd=project_root)
        print("✅ 虚拟环境创建完成")
    else:
        print("✅ 虚拟环境已存在")

def install_dependencies():
    """安装依赖"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 确定pip路径
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(project_root, "AI_Server", "Scripts", "pip.exe")
    else:  # Unix/Linux/MacOS
        pip_path = os.path.join(project_root, "AI_Server", "bin", "pip")
    
    requirements_path = os.path.join(project_root, "requirements.txt")
    
    if os.path.exists(pip_path) and os.path.exists(requirements_path):
        print("📦 安装依赖包...")
        subprocess.run([pip_path, "install", "-r", requirements_path])
        print("✅ 依赖安装完成")
    else:
        print("❌ 找不到pip或requirements.txt")

def check_env_file():
    """检查.env文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    env_path = os.path.join(project_root, ".env")
    env_example_path = os.path.join(project_root, ".env.example")
    
    if os.path.exists(env_path):
        print("✅ .env文件已存在")
    elif os.path.exists(env_example_path):
        print("⚠️  请复制.env.example为.env并填入你的API密钥")
        print("   Windows: copy .env.example .env")
        print("   Linux/Mac: cp .env.example .env")
    else:
        print("❌ 找不到.env配置文件")

def main():
    """主函数"""
    print("🛠️  AI Server 环境设置")
    print("=" * 40)
    
    if not check_python_version():
        return
    
    setup_virtual_env()
    install_dependencies()
    check_env_file()
    
    print("\n🎉 环境设置完成！")
    print("📝 下一步:")
    print("   1. 编辑.env文件，添加你的API密钥")
    print("   2. 运行: python scripts/start.py")

if __name__ == "__main__":
    main()