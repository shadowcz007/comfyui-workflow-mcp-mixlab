"""
ComfyUI 服务器启动回调模块
这个模块包含在 ComfyUI 服务器启动后执行的自定义回调函数
"""

import os
import logging
import threading
from typing import Optional

def start_mcp_server():
    """
    启动 MCP 服务器，使用 SSE 传输协议，并配置 CORS 支持
    """
    try:
        from fastmcp import FastMCP
        from starlette.middleware.cors import CORSMiddleware
        from starlette.middleware import Middleware
        
        # 创建 FastMCP 实例
        mcp = FastMCP("ComfyUI Workflow MCP 🚀")
        
        # 导入所有工具
        from tools import (
            # 工作流执行相关工具
            submit_workflow, get_queue_info, clear_queue, delete_queue_item, 
            interrupt_processing, free_memory,
            
            # 历史记录管理工具
            get_history, get_history_by_id, clear_history, delete_history_item,
            
            # 文件上传和管理工具
            upload_image, view_image,
            
            # 系统信息工具
            get_system_stats, get_features, get_object_info, get_object_info_by_node,
            get_queue_status, get_prompt_status
        )
        
        # 工作流执行相关工具
        @mcp.tool
        def submit_workflow_tool(workflow_json: str, client_id: str = None, prompt_id: str = None) -> str:
            """提交工作流执行请求"""
            result = submit_workflow(workflow_json, client_id, prompt_id)
            return str(result)
        
        @mcp.tool
        def get_queue_info_tool() -> str:
            """获取队列信息"""
            result = get_queue_info()
            return str(result)
        
        @mcp.tool
        def clear_queue_tool() -> str:
            """清除队列中的所有任务"""
            result = clear_queue()
            return str(result)
        
        @mcp.tool
        def delete_queue_item_tool(prompt_id: str) -> str:
            """删除队列中的特定任务"""
            result = delete_queue_item(prompt_id)
            return str(result)
        
        @mcp.tool
        def interrupt_processing_tool() -> str:
            """中断当前处理"""
            result = interrupt_processing()
            return str(result)
        
        @mcp.tool
        def free_memory_tool(unload_models: bool = False, free_memory_param: bool = False) -> str:
            """释放内存和模型"""
            result = free_memory(unload_models, free_memory_param)
            return str(result)
        
        # 历史记录管理工具
        @mcp.tool
        def get_history_tool(max_items: int = None) -> str:
            """获取历史记录"""
            result = get_history(max_items)
            return str(result)
        
        @mcp.tool
        def get_history_by_id_tool(prompt_id: str) -> str:
            """根据ID获取特定的历史记录"""
            result = get_history_by_id(prompt_id)
            return str(result)
        
        @mcp.tool
        def clear_history_tool() -> str:
            """清除所有历史记录"""
            result = clear_history()
            return str(result)
        
        @mcp.tool
        def delete_history_item_tool(prompt_id: str) -> str:
            """删除特定的历史记录项"""
            result = delete_history_item(prompt_id)
            return str(result)
        
        @mcp.tool
        def upload_image_tool(image_path: str, subfolder: str = "", upload_type: str = "input", overwrite: bool = False) -> str:
            """上传图片文件"""
            result = upload_image(image_path, subfolder, upload_type, overwrite)
            return str(result)
        
        @mcp.tool
        def view_image_tool(filename: str, image_type: str = "output", subfolder: str = "", channel: str = "rgba", preview: str = None) -> str:
            """查看图片文件"""
            result = view_image(filename, image_type, subfolder, channel, preview)
            return str(result)
        
        # 系统信息工具
        @mcp.tool
        def get_system_stats_tool() -> str:
            """获取系统状态信息"""
            result = get_system_stats()
            return str(result)
        
        @mcp.tool
        def get_features_tool() -> str:
            """获取功能特性信息"""
            result = get_features()
            return str(result)
        
        @mcp.tool
        def get_object_info_tool() -> str:
            """获取所有节点信息"""
            result = get_object_info()
            return str(result)
        
        @mcp.tool
        def get_object_info_by_node_tool(node_class: str) -> str:
            """获取特定节点的信息"""
            result = get_object_info_by_node(node_class)
            return str(result)
        
        @mcp.tool
        def get_queue_status_tool() -> str:
            """获取队列状态信息"""
            result = get_queue_status()
            return str(result)
        
        @mcp.tool
        def get_prompt_status_tool() -> str:
            """获取提示状态信息"""
            result = get_prompt_status()
            return str(result)
        
        # 在后台线程中启动 MCP 服务器
        def run_mcp_server():
            try:
                # 配置 CORS 中间件
                cors_middleware = [
                    Middleware(
                        CORSMiddleware,
                        allow_origins=["*"],  # 允许所有来源，生产环境中应该配置具体的域名
                        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],  # MCP streamable HTTP 方法
                        allow_headers=["*"],  # 允许所有请求头
                        expose_headers=["Mcp-Session-Id"],  # 暴露 MCP 会话 ID 头
                        allow_credentials=True,  # 允许携带凭证
                    )
                ]
                
                # 启动服务器，传入 CORS 中间件
                mcp.run(
                    transport="sse", 
                    host="0.0.0.0", 
                    port=7397,
                    middleware=cors_middleware
                )
            except Exception as e:
                print(f"❌ MCP 服务器启动失败: {e}")
                logging.error(f"MCP 服务器启动失败: {e}")
        
        # 启动 MCP 服务器线程
        mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
        mcp_thread.start()
        
        print("✅ MCP 服务器已启动 (SSE 模式 + CORS 支持) - http://127.0.0.1:7397")
        print("🌐 CORS 已启用，支持跨域请求")
        print("🔧 已集成 ComfyUI API 工具:")
        print("   - 工作流执行: submit_workflow, get_queue_info, clear_queue, delete_queue_item, interrupt_processing, free_memory")
        print("   - 历史记录管理: get_history, get_history_by_id, clear_history, delete_history_item")
        print("   - 文件管理: upload_image, view_image")
        print("   - 系统信息: get_system_stats, get_features, get_object_info, get_queue_status, get_prompt_status")
        return True
        
    except ImportError:
        print("❌ 未找到 fastmcp 库，请安装: pip install fastmcp")
        logging.error("未找到 fastmcp 库")
        return False
    except Exception as e:
        print(f"❌ MCP 服务器启动失败: {e}")
        logging.error(f"MCP 服务器启动失败: {e}")
        return False

def execute_all_callbacks():
    """
    执行所有自定义回调函数
    这个函数会在 ComfyUI 服务器启动后被调用
    """
    print("🚀 开始启动mcp服务...")
    
    try:
        # 启动 MCP 服务器
        mcp_started = start_mcp_server()
        
        if mcp_started:
            print("✅ MCP 服务器启动成功")
        else:
            print("⚠️ MCP 服务器启动失败")
        
    except Exception as e:
        print(f"❌ 自定义回调执行失败: {e}")
        logging.error(f"自定义回调执行失败: {e}")

# 如果直接运行此文件，执行测试
if __name__ == "__main__":
    print("🧪 测试自定义回调模块...")
    execute_all_callbacks() 