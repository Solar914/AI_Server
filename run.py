#!/usr/bin/env python3
"""
AI Server 项目启动器
为了保持向后兼容性，这个文件将调用src/main.py
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入并运行主程序
from src.main import main

if __name__ == "__main__":
    main()