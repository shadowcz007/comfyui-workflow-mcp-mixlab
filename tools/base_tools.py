"""
基础工具类 - 提供对ComfyUI服务器实例的访问
"""

import sys
import os
import logging
from typing import Optional, Dict, Any

class ComfyUIToolsBase:
    """ComfyUI工具基础类，提供对服务器实例的访问"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._prompt_server = None
    
    @property
    def prompt_server(self):
        """获取ComfyUI的PromptServer实例"""
        if self._prompt_server is None:
            try:
                # 尝试从ComfyUI获取服务器实例
                import server
                if hasattr(server, 'PromptServer') and hasattr(server.PromptServer, 'instance'):
                    self._prompt_server = server.PromptServer.instance
                else:
                    self.logger.warning("无法获取ComfyUI服务器实例")
            except ImportError as e:
                self.logger.error(f"无法导入ComfyUI服务器模块: {e}")
        return self._prompt_server
    
    def get_server_method(self, method_name: str):
        """获取服务器方法"""
        if self.prompt_server is None:
            raise RuntimeError("ComfyUI服务器未启动或无法访问")
        
        if hasattr(self.prompt_server, method_name):
            return getattr(self.prompt_server, method_name)
        else:
            raise AttributeError(f"服务器方法 '{method_name}' 不存在")
    
    def call_server_method(self, method_name: str, *args, **kwargs):
        """调用服务器方法"""
        method = self.get_server_method(method_name)
        return method(*args, **kwargs)
    
    def create_mock_request(self, **kwargs):
        """创建模拟的请求对象，用于调用API方法"""
        class MockRequest:
            def __init__(self, **kwargs):
                self.rel_url = type('obj', (object,), {
                    'query': kwargs.get('query', {}),
                    'match_info': kwargs.get('match_info', {})
                })
                self.headers = kwargs.get('headers', {})
                self._json_data = kwargs.get('json_data', {})
                self._post_data = kwargs.get('post_data', {})
            
            async def json(self):
                return self._json_data
            
            async def post(self):
                return self._post_data
        
        return MockRequest(**kwargs)

# 全局工具基础实例
tools_base = ComfyUIToolsBase() 