"""
历史记录管理工具 - 直接对接到ComfyUI API方法
"""

import asyncio
from typing import Dict, Any, Optional
from .base_tools import tools_base

def get_history(max_items: Optional[int] = None) -> Dict[str, Any]:
    """
    获取历史记录
    
    Args:
        max_items: 最大返回项目数（可选）
    
    Returns:
        历史记录数据
    """
    try:
        # 创建模拟请求对象
        query_params = {}
        if max_items is not None:
            query_params["max_items"] = str(max_items)
        
        mock_request = tools_base.create_mock_request(query=query_params)
        
        # 直接调用ComfyUI的get_history方法
        async def async_get_history():
            try:
                get_history_method = tools_base.get_server_method("get_history")
                response = await get_history_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
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
            # 如果已经有事件循环在运行，使用 asyncio.create_task 或直接调用同步版本
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: asyncio.run(async_get_history()))
                result = future.result(timeout=30)  # 30秒超时
        except RuntimeError:
            # 如果没有事件循环在运行，直接运行
            result = asyncio.run(async_get_history())
        
        return result
        
    except Exception as e:
        return {"error": f"获取历史记录失败: {e}"}

def get_history_by_id(prompt_id: str) -> Dict[str, Any]:
    """
    根据ID获取特定的历史记录
    
    Args:
        prompt_id: 提示ID
    
    Returns:
        特定历史记录数据
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(match_info={"prompt_id": prompt_id})
        
        # 直接调用ComfyUI的get_history_prompt_id方法
        async def async_get_history_by_id():
            try:
                get_history_method = tools_base.get_server_method("get_history_prompt_id")
                response = await get_history_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
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
                future = executor.submit(lambda: asyncio.run(async_get_history_by_id()))
                result = future.result(timeout=30)  # 30秒超时
        except RuntimeError:
            # 如果没有事件循环在运行，直接运行
            result = asyncio.run(async_get_history_by_id())
        
        return result
        
    except Exception as e:
        return {"error": f"获取历史记录失败: {e}"}

def clear_history() -> Dict[str, str]:
    """
    清除所有历史记录
    
    Returns:
        操作结果
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(json_data={"clear": True})
        
        # 直接调用ComfyUI的post_history方法
        async def async_clear_history():
            try:
                post_history_method = tools_base.get_server_method("post_history")
                response = await post_history_method(mock_request)
                return {"status": "success", "message": "历史记录已清除"}
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数 - 使用线程安全的方式
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_running_loop()
            # 如果已经有事件循环在运行，使用线程池
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: asyncio.run(async_clear_history()))
                result = future.result(timeout=30)  # 30秒超时
        except RuntimeError:
            # 如果没有事件循环在运行，直接运行
            result = asyncio.run(async_clear_history())
        
        return result
        
    except Exception as e:
        return {"error": f"清除历史记录失败: {e}"}

def delete_history_item(prompt_id: str) -> Dict[str, str]:
    """
    删除特定的历史记录项
    
    Args:
        prompt_id: 要删除的提示ID
    
    Returns:
        操作结果
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(json_data={"delete": [prompt_id]})
        
        # 直接调用ComfyUI的post_history方法
        async def async_delete_history():
            try:
                post_history_method = tools_base.get_server_method("post_history")
                response = await post_history_method(mock_request)
                return {"status": "success", "message": f"历史记录项 {prompt_id} 已删除"}
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数 - 使用线程安全的方式
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_running_loop()
            # 如果已经有事件循环在运行，使用线程池
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: asyncio.run(async_delete_history()))
                result = future.result(timeout=30)  # 30秒超时
        except RuntimeError:
            # 如果没有事件循环在运行，直接运行
            result = asyncio.run(async_delete_history())
        
        return result
        
    except Exception as e:
        return {"error": f"删除历史记录失败: {e}"} 