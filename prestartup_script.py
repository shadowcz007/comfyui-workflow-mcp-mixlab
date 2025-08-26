# 在 prestartup_script.py 中获取 ComfyUI 服务器端口并实现启动回调
import sys
import os
import threading
import time
import logging

# 添加 ComfyUI 路径到 sys.path，以便导入 comfy 模块
comfyui_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if comfyui_path not in sys.path:
    sys.path.insert(0, comfyui_path)

try:
    # 导入 comfy.cli_args 模块来访问 args
    from comfy.cli_args import args
    
    # 禁用自动打开浏览器
    args.auto_launch = False
    print("已禁用 ComfyUI 自动打开浏览器功能")
    
    # 修改服务器端口为7396
    args.port = 7396
    print("已修改 ComfyUI 服务器端口为: 7396")
    
    # 获取服务器端口和监听地址
    server_port = args.port
    server_listen = args.listen

    # 保存到环境变量中
    os.environ['COMFYUI_SERVER_PORT'] = str(server_port)
    os.environ['COMFYUI_SERVER_LISTEN'] = server_listen
    
    # 全局标志，防止重复执行回调
    callback_executed_global = False
    
    def install_dependencies():
        """安装所需的依赖包"""
        print("🔧 检查并安装 ComfyUI Workflow MCP MixLab 依赖包...")
        
        try:
            # 检查是否已安装 fastmcp
            try:
                import fastmcp
                print("✅ fastmcp 已安装")
                return True
            except ImportError:
                print("⚠️ fastmcp 未安装，开始安装...")
            
            # 导入依赖安装模块
            try:
                # 确保当前目录在 Python 路径中
                current_dir = os.path.dirname(os.path.abspath(__file__))
                if current_dir not in sys.path:
                    sys.path.insert(0, current_dir)
                
                from install_dependencies import install_dependencies as install_deps
                success = install_deps()
                if success:
                    print("✅ 依赖包安装完成")
                    return True
                else:
                    print("❌ 依赖包安装失败")
                    return False
            except ImportError as e:
                print(f"❌ 无法导入 install_dependencies 模块: {e}")
                return False
                
        except Exception as e:
            print(f"❌ 依赖安装过程中出现错误: {e}")
            return False
     
    
    # 定义服务器启动后的回调函数
    def on_server_started():
        """服务器启动后的回调函数"""
        global callback_executed_global
        
        # 防止重复执行
        if callback_executed_global:
            # print("⚠️ 回调已执行，跳过重复调用")
            return
        
        callback_executed_global = True
        
        print("🎉 ComfyUI 服务器已启动!")
        # print(f"服务器地址: http://{server_listen}:{server_port}")
        
        # 首先安装依赖 
        if not install_dependencies():
            print("⚠️ 依赖安装失败...")
        
        try:
            # 导入自定义回调模块
            try:
                # 尝试直接导入
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                
                # 确保当前目录在 Python 路径中
                if current_dir not in sys.path:
                    sys.path.insert(0, current_dir)
                
                # 尝试导入
                try:
                    import server_callbacks 
                    server_callbacks.execute_all_callbacks()
                except ImportError as e:
                    print(f"⚠️ 无法导入自定义回调模块: {e}")
                 
            except Exception as e:
                print(f"❌ 回调模块处理失败: {e}")
            
            
            # 检查服务器状态
            check_server_health() 
            
        except Exception as e:
            print(f"❌ 服务器启动回调执行失败: {e}")
            logging.error(f"服务器启动回调执行失败: {e}")

    
    def check_server_health():
        """检查服务器健康状态"""
        try:
            # 尝试导入requests，如果不可用则跳过健康检查
            try:
                import requests
            except ImportError:
                print("⚠️ requests库不可用，跳过健康检查")
                return
            
            response = requests.get(f"http://{server_listen}:{server_port}/system_stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                # print("✅ 服务器健康检查通过")
            else:
                print(f"⚠️ 服务器响应异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 服务器健康检查失败: {e}")
    
    def wait_for_server_start():
        """等待服务器启动的监控线程"""
        max_attempts = 60  # 最多等待60秒
        attempt = 0
        callback_executed = False  # 标记回调是否已执行
        
        print(f"📡 开始监控服务器启动状态...")
        print(f"   目标地址: http://{server_listen}:{server_port}")
        
        while attempt < max_attempts and not callback_executed:
            try:
                # 尝试导入requests
                try:
                    import requests
                except ImportError:
                    print("⚠️ requests库不可用，使用简单连接检查")
                    # 使用socket进行简单连接检查
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((server_listen, server_port))
                    sock.close()
                    
                    if result == 0:
                        # print(f"🚀 检测到服务器已启动 (尝试 {attempt + 1}/{max_attempts})")
                        on_server_started()
                        callback_executed = True
                        break
                else:
                    # 使用requests进行HTTP检查
                    response = requests.get(f"http://{server_listen}:{server_port}/system_stats", timeout=2)
                    if response.status_code == 200:
                        # print(f"🚀 检测到服务器已启动 (尝试 {attempt + 1}/{max_attempts})")
                        on_server_started()
                        callback_executed = True
                        break
                        
            except Exception as e:
                # 静默处理连接错误，避免过多日志输出
                pass
            
            attempt += 1
            time.sleep(2)
    
    # 启动监控线程
    monitor_thread = threading.Thread(target=wait_for_server_start, daemon=True)
    monitor_thread.start()
    
except ImportError as e:
    print(f"无法导入 comfy.cli_args: {e}")
except Exception as e:
    print(f"获取服务器配置时出错: {e}")
    logging.error(f"prestartup_script执行失败: {e}")
