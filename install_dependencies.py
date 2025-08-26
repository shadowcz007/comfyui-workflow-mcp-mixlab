#!/usr/bin/env python3
"""
安装 ComfyUI Workflow MCP MixLab 依赖包
"""

import subprocess
import sys
import os
import importlib.util

def get_comfyui_python():
    # 如果都找不到，使用当前Python
    return sys.executable

def is_installed(package, package_overwrite=None, auto_install=True):
    """检查包是否已安装，如果未安装则自动安装"""
    python = get_comfyui_python()
    is_has = False
    spec = None
    
    try:
        spec = importlib.util.find_spec(package)
        is_has = spec is not None
    except ModuleNotFoundError:
        pass

    package = package_overwrite or package

    if spec is None:
        if auto_install == True:
            print(f"Installing {package}...")
            # 清华源 -i https://pypi.tuna.tsinghua.edu.cn/simple
            command = f'"{python}" -m pip install {package}'

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ)

            is_has = True

            if result.returncode != 0:
                print(f"Couldn't install\nCommand: {command}\nError code: {result.returncode}")
                is_has = False
    else:
        print(package + '## OK')

    return is_has

def install_dependencies():
    """安装所需的依赖包"""
    print("🔧 开始安装 ComfyUI Workflow MCP MixLab 依赖包...")
    
    # 获取ComfyUI的Python环境
    python = get_comfyui_python()
    print(f"使用Python环境: {python}")
    
    try:
        # 读取 requirements.txt
        requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        
        if not os.path.exists(requirements_file):
            print("❌ 未找到 requirements.txt 文件")
            return False
        
        # 读取依赖包列表
        with open(requirements_file, 'r', encoding='utf-8') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # 逐个检查并安装包
        all_installed = True
        for package in packages:
            if not is_installed(package):
                all_installed = False
        
        if all_installed:
            print("✅ 所有依赖包安装成功")
            return True
        else:
            print("❌ 部分依赖包安装失败")
            return False
            
    except Exception as e:
        print(f"❌ 安装过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    install_dependencies() 