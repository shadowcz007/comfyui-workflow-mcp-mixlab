"""
文件上传和管理工具 - 直接对接到ComfyUI API方法
"""

import asyncio
import os
from typing import Dict, Any, Optional
from .base_tools import tools_base

def list_models() -> Dict[str, Any]:
    """
    获取所有模型类型列表
    
    Returns:
        模型类型列表
    """
    try:
        # 直接调用ComfyUI的list_model_types方法
        # 这个方法在server.py中是同步的，所以可以直接调用
        list_model_types_method = tools_base.get_server_method("list_model_types")
        
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 调用方法
        result = list_model_types_method(mock_request)
        
        # 从响应中提取数据
        if hasattr(result, 'body'):
            import json
            response_data = json.loads(result.body.decode('utf-8'))
        else:
            response_data = result
        
        return {"models": response_data}
        
    except Exception as e:
        return {"error": f"获取模型列表失败: {e}"}

def list_models_by_folder(folder: str) -> Dict[str, Any]:
    """
    获取特定文件夹的模型列表
    
    Args:
        folder: 模型文件夹名称
    
    Returns:
        模型文件列表
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(match_info={"folder": folder})
        
        # 直接调用ComfyUI的get_models方法
        async def async_get_models():
            try:
                get_models_method = tools_base.get_server_method("get_models")
                response = await get_models_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return {"models": response_data}
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_models())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_models())
        
        return result
        
    except Exception as e:
        return {"error": f"获取模型列表失败: {e}"}

def list_embeddings() -> Dict[str, Any]:
    """
    获取嵌入模型列表
    
    Returns:
        嵌入模型列表
    """
    try:
        # 直接调用ComfyUI的get_embeddings方法
        get_embeddings_method = tools_base.get_server_method("get_embeddings")
        
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 调用方法
        result = get_embeddings_method(mock_request)
        
        # 从响应中提取数据
        if hasattr(result, 'body'):
            import json
            response_data = json.loads(result.body.decode('utf-8'))
        else:
            response_data = result
        
        return {"embeddings": response_data}
        
    except Exception as e:
        return {"error": f"获取嵌入模型列表失败: {e}"}

def list_extensions() -> Dict[str, Any]:
    """
    获取扩展列表
    
    Returns:
        扩展列表
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request()
        
        # 直接调用ComfyUI的get_extensions方法
        async def async_get_extensions():
            try:
                get_extensions_method = tools_base.get_server_method("get_extensions")
                response = await get_extensions_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return {"extensions": response_data}
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_get_extensions())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_get_extensions())
        
        return result
        
    except Exception as e:
        return {"error": f"获取扩展列表失败: {e}"}

def view_metadata(folder_name: str, filename: str) -> Dict[str, Any]:
    """
    查看模型元数据
    
    Args:
        folder_name: 文件夹名称
        filename: 文件名
    
    Returns:
        模型元数据
    """
    try:
        # 创建模拟请求对象
        mock_request = tools_base.create_mock_request(
            match_info={"folder_name": folder_name},
            query={"filename": filename}
        )
        
        # 直接调用ComfyUI的view_metadata方法
        async def async_view_metadata():
            try:
                view_metadata_method = tools_base.get_server_method("view_metadata")
                response = await view_metadata_method(mock_request)
                
                # 从响应中提取数据
                if hasattr(response, 'body'):
                    import json
                    response_data = json.loads(response.body.decode('utf-8'))
                else:
                    response_data = response
                
                return {"metadata": response_data}
            except Exception as e:
                return {"error": str(e)}
        
        # 运行异步函数
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(async_view_metadata())
            finally:
                new_loop.close()
        else:
            result = loop.run_until_complete(async_view_metadata())
        
        return result
        
    except Exception as e:
        return {"error": f"获取模型元数据失败: {e}"}

def upload_image(image_path: str, subfolder: str = "", upload_type: str = "input", overwrite: bool = False) -> Dict[str, Any]:
    """
    上传图片文件
    
    Args:
        image_path: 图片文件路径
        subfolder: 子文件夹（可选）
        upload_type: 上传类型（input/output/temp）
        overwrite: 是否覆盖现有文件
    
    Returns:
        上传结果
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return {"error": f"文件不存在: {image_path}"}
        
        # 创建模拟的文件对象
        class MockImageFile:
            def __init__(self, filepath):
                self.filepath = filepath
                self.filename = os.path.basename(filepath)
                self.file = open(filepath, 'rb')
            
            def read(self):
                return self.file.read()
        
        # 创建模拟的POST数据
        mock_post_data = {
            "image": MockImageFile(image_path),
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