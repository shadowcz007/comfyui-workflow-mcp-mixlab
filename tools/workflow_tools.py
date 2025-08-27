"""
工作流执行相关工具 - 直接对接到ComfyUI API方法
"""

import json
import uuid
import asyncio
from typing import Dict, Any, Optional
from .base_tools import tools_base

def submit_workflow(workflow_json: str, client_id: Optional[str] = None, prompt_id: Optional[str] = None) -> Dict[str, Any]:
    """
    提交工作流执行请求
    
    Args:
        workflow_json: 工作流JSON字符串
        client_id: 客户端ID（可选）
        prompt_id: 提示ID（可选）
    
    Returns:
        包含prompt_id和number的响应字典
    """
    try:
        # 解析工作流JSON
        workflow_data = json.loads(workflow_json)
        
        # 准备请求数据
        request_data = {
            "prompt": workflow_data
        }
        
        if client_id:
            request_data["client_id"] = client_id
        
        if prompt_id:
            request_data["prompt_id"] = prompt_id
        
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(json_data=request_data)
        
        # 直接调用ComfyUI的post_prompt方法
        # 注意：这里需要异步调用，但我们用同步方式包装
        async def async_submit():
            try:
                # 获取post_prompt方法
                post_prompt_method = tools_base.get_server_method("post_prompt")
                response = await post_prompt_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数 - 使用线程安全的方式
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_running_loop()
            # 如果已经有事件循环在运行，使用线程池
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: asyncio.run(async_submit()))
                result = future.result(timeout=30)  # 30秒超时
        except RuntimeError:
            # 如果没有事件循环在运行，直接运行
            result = asyncio.run(async_submit())
        
        return result
        
    except json.JSONDecodeError as e:
        return {"error": f"无效的JSON格式: {e}"}
    except Exception as e:
        return {"error": f"提交工作流失败: {e}"}

def get_queue_info() -> Dict[str, Any]:
    """
    获取队列信息
    
    Returns:
        队列状态信息
    """
    try:
        # 直接调用ComfyUI的get_queue_info方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 直接调用PromptServer的get_queue_info方法
        queue_info = tools_base.prompt_server.get_queue_info()
        return queue_info
    except Exception as e:
        return {"error": f"获取队列信息失败: {e}"}

def clear_queue() -> Dict[str, str]:
    """
    清除队列中的所有任务
    
    Returns:
        操作结果
    """
    try:
        # 直接调用ComfyUI的prompt_queue.wipe_queue方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 直接调用prompt_queue的wipe_queue方法
        tools_base.prompt_server.prompt_queue.wipe_queue()
        return {"status": "success", "message": "队列已清除"}
        
    except Exception as e:
        return {"error": f"清除队列失败: {e}"}

def delete_queue_item(prompt_id: str) -> Dict[str, str]:
    """
    删除队列中的特定任务
    
    Args:
        prompt_id: 要删除的任务ID
    
    Returns:
        操作结果
    """
    try:
        # 直接调用ComfyUI的prompt_queue.delete_queue_item方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 创建删除函数
        delete_func = lambda a: a[1] == prompt_id
        
        # 直接调用prompt_queue的delete_queue_item方法
        result = tools_base.prompt_server.prompt_queue.delete_queue_item(delete_func)
        if result:
            return {"status": "success", "message": f"任务 {prompt_id} 已删除"}
        else:
            return {"error": f"任务 {prompt_id} 不存在或删除失败"}
        
    except Exception as e:
        return {"error": f"删除任务失败: {e}"}

def interrupt_processing() -> Dict[str, str]:
    """
    中断当前处理
    
    Returns:
        操作结果
    """
    try:
        # 直接调用ComfyUI的nodes.interrupt_processing方法
        import nodes
        nodes.interrupt_processing()
        return {"status": "success", "message": "处理已中断"}
        
    except Exception as e:
        return {"error": f"中断处理失败: {e}"}

def free_memory(unload_models: bool = False, free_memory_param: bool = False) -> Dict[str, str]:
    """
    释放内存和模型
    
    Args:
        unload_models: 是否卸载模型
        free_memory_param: 是否释放内存
    
    Returns:
        操作结果
    """
    try:
        # 直接调用ComfyUI的内存释放功能
        import nodes
        
        if unload_models:
            # 卸载模型
            nodes.unload_all_models()
        
        if free_memory_param:
            # 释放内存
            import gc
            gc.collect()
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        return {"status": "success", "message": "内存释放操作已执行"}
        
    except Exception as e:
        return {"error": f"释放内存失败: {e}"} 