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
        # 直接调用ComfyUI的prompt_queue.get_history方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 直接调用prompt_queue的get_history方法
        result = tools_base.prompt_server.prompt_queue.get_history(max_items=max_items)
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
        # 直接调用ComfyUI的prompt_queue.get_history方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 直接调用prompt_queue的get_history方法，传入prompt_id
        result = tools_base.prompt_server.prompt_queue.get_history(prompt_id=prompt_id)
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
        # 直接调用ComfyUI的prompt_queue.wipe_history方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 直接调用prompt_queue的wipe_history方法
        tools_base.prompt_server.prompt_queue.wipe_history()
        return {"status": "success", "message": "历史记录已清除"}
        
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
        # 直接调用ComfyUI的prompt_queue.delete_history_item方法
        if tools_base.prompt_server is None:
            return {"error": "ComfyUI服务器未启动"}
        
        # 直接调用prompt_queue的delete_history_item方法
        tools_base.prompt_server.prompt_queue.delete_history_item(prompt_id)
        return {"status": "success", "message": f"历史记录项 {prompt_id} 已删除"}
        
    except Exception as e:
        return {"error": f"删除历史记录失败: {e}"} 