"""
系统信息工具 - 直接对接到ComfyUI API方法
"""

import asyncio
from typing import Dict, Any, Optional
from .base_tools import tools_base

def get_system_stats() -> Dict[str, Any]:
    """
    获取系统状态信息
    
    Returns:
        系统状态信息
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 直接调用ComfyUI的system_stats方法
        async def async_get_system_stats():
            try:
                system_stats_method = tools_base.get_server_method("system_stats")
                response = await system_stats_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_system_stats())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_system_stats())
        
        return result
        
    except Exception as e:
        return {"error": f"获取系统状态失败: {e}"}

def get_features() -> Dict[str, Any]:
    """
    获取功能特性信息
    
    Returns:
        功能特性信息
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 直接调用ComfyUI的get_features方法
        async def async_get_features():
            try:
                get_features_method = tools_base.get_server_method("get_features")
                response = await get_features_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_features())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_features())
        
        return result
        
    except Exception as e:
        return {"error": f"获取功能特性失败: {e}"}

def get_object_info() -> Dict[str, Any]:
    """
    获取所有节点信息
    
    Returns:
        所有节点信息
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 直接调用ComfyUI的get_object_info方法
        async def async_get_object_info():
            try:
                get_object_info_method = tools_base.get_server_method("get_object_info")
                response = await get_object_info_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_object_info())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_object_info())
        
        return result
        
    except Exception as e:
        return {"error": f"获取节点信息失败: {e}"}

def get_object_info_by_node(node_class: str) -> Dict[str, Any]:
    """
    获取特定节点的信息
    
    Args:
        node_class: 节点类名
    
    Returns:
        特定节点信息
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(match_info={"node_class": node_class})
        
        # 直接调用ComfyUI的get_object_info_node方法
        async def async_get_object_info_node():
            try:
                get_object_info_node_method = tools_base.get_server_method("get_object_info_node")
                response = await get_object_info_node_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_object_info_node())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_object_info_node())
        
        return result
        
    except Exception as e:
        return {"error": f"获取节点信息失败: {e}"}

def get_queue_status() -> Dict[str, Any]:
    """
    获取队列状态信息
    
    Returns:
        队列状态信息
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 直接调用ComfyUI的get_queue方法
        async def async_get_queue():
            try:
                get_queue_method = tools_base.get_server_method("get_queue")
                response = await get_queue_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_queue())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_queue())
        
        return result
        
    except Exception as e:
        return {"error": f"获取队列状态失败: {e}"}

def get_prompt_status() -> Dict[str, Any]:
    """
    获取提示状态信息
    
    Returns:
        提示状态信息
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 直接调用ComfyUI的get_prompt方法
        async def async_get_prompt():
            try:
                get_prompt_method = tools_base.get_server_method("get_prompt")
                response = await get_prompt_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return response_data
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_prompt())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_prompt())
        
        return result
        
    except Exception as e:
        return {"error": f"获取提示状态失败: {e}"} 