"""
文件上传和管理工具 - 直接对接到ComfyUI API方法
"""

import asyncio
import os
import base64
import io
from typing import Dict, Any, Optional
from .base_tools import tools_base

def upload_image(image_base64: str, filename: str, subfolder: str = "", upload_type: str = "input", overwrite: bool = False) -> Dict[str, Any]:
    """
    上传base64格式的图片
    
    Args:
        image_base64: base64编码的图片数据
        filename: 文件名
        subfolder: 子文件夹（可选）
        upload_type: 上传类型（input/output/temp）
        overwrite: 是否覆盖现有文件
    
    Returns:
        上传结果
    """
    try:
        # 解码base64数据
        try:
            # 移除可能的数据URL前缀
            if image_base64.startswith('data:image/'):
                image_base64 = image_base64.split(',')[1]
            
            image_data = base64.b64decode(image_base64)
        except Exception as e:
            return {"error": f"base64解码失败: {e}"}
        
        # 创建模拟的文件对象
        class MockImageFile:
            def __init__(self, data, filename):
                self.filename = filename
                self.file = io.BytesIO(data)
            
            def read(self):
                return self.file.read()
        
        # 创建模拟的POST数据
        mock_post_data = {
            "image": MockImageFile(image_data, filename),
            "subfolder": subfolder,
            "type": upload_type,
            "overwrite": str(overwrite).lower()
        }
        
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(post_data=mock_post_data)
        
        # 直接调用ComfyUI的upload_image方法
        async def async_upload_image():
            try:
                upload_image_method = tools_base.get_server_method("upload_image")
                response = await upload_image_method(mock_request)
                
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
                result = new_loop.run_until_complete(async_upload_image())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_upload_image())
        
        return result
        
    except Exception as e:
        return {"error": f"上传图片失败: {e}"}

def view_image(filename: str, image_type: str = "output", subfolder: str = "", channel: str = "rgba", preview: Optional[str] = None) -> Dict[str, Any]:
    """
    查看图片文件
    
    Args:
        filename: 文件名
        image_type: 图片类型（output/input/temp）
        subfolder: 子文件夹（可选）
        channel: 通道（rgba/rgb/a）
        preview: 预览格式（可选，如"webp;90"）
    
    Returns:
        图片信息或错误信息
    """
    try:
        # 构建查询参数
        query_params = {
            "filename": filename,
            "type": image_type,
            "channel": channel
        }
        
        if subfolder:
            query_params["subfolder"] = subfolder
        
        if preview:
            query_params["preview"] = preview
        
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(query=query_params)
        
        # 直接调用ComfyUI的view_image方法
        async def async_view_image():
            try:
                view_image_method = tools_base.get_server_method("view_image")
                response = await view_image_method(mock_request)
                
                # 检查响应状态
                if hasattr(response, 'status') and response.status != 200:
                    return {"error": f"查看图片失败，状态码: {response.status}"}
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    # 如果是图片数据，返回基本信息
                    return {
                        "status": "success",
                        "content_type": getattr(response, 'content_type', 'unknown'),
                        "content_length": len(response.body) if hasattr(response, 'body') else 0
                    }
                else:
                    return {"status": "success", "data": response}
                    
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_view_image())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_view_image())
        
        return result
        
    except Exception as e:
        return {"error": f"查看图片失败: {e}"} 