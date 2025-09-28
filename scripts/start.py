#!/usr/bin/env python3
"""
AI Server 启动脚本
"""

import os
import sys

def main():
    """启动AI Server"""
    print("🚀 启动 AI Server...")
    
    # 确保在项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # 添加项目根目录到Python路径
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # 导入并运行主程序
    from src.main import main as run_main
    run_main()

if __name__ == "__main__":
    main()