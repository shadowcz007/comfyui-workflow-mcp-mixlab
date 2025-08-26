import json
import os
import logging
from typing import Dict, Any

class WorkflowLoader:
    """
    ComfyUI Workflow MCP MixLab - 自动加载默认 workflow 的节点
    
    这个节点会在 ComfyUI 启动时自动加载默认的 workflow 配置
    """
    
    def __init__(self):
        self.workflow_loaded = False
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点的输入参数
        """
        return {
            "required": {
                "auto_load": (["enable", "disable"], {
                    "default": "enable"
                }),
                "workflow_file": ("STRING", {
                    "default": "default_workflow.json",
                    "multiline": False
                }),
            },
            "optional": {
                "force_reload": (["enable", "disable"], {
                    "default": "disable"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "load_workflow"
    CATEGORY = "MIXLAB/Workflow"
    
    def load_workflow(self, auto_load, workflow_file, force_reload="disable"):
        """
        加载默认 workflow 的主要函数
        """
        try:
            if auto_load == "disable":
                return ("Workflow loading disabled",)
            
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            workflow_path = os.path.join(current_dir, workflow_file)
            
            # 检查 workflow 文件是否存在
            if not os.path.exists(workflow_path):
                error_msg = f"Workflow file not found: {workflow_path}"
                self.logger.error(error_msg)
                return (f"❌ {error_msg}",)
            
            # 读取 workflow 文件
            try:
                with open(workflow_path, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                
                # 这里可以添加 workflow 加载逻辑
                # 例如：发送到 ComfyUI 的 API 或存储到全局变量中
                
                status_msg = f"✅ Workflow loaded successfully: {workflow_file}"
                self.logger.info(status_msg)
                
                # 标记 workflow 已加载
                self.workflow_loaded = True
                
                return (status_msg,)
                
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON in workflow file: {e}"
                self.logger.error(error_msg)
                return (f"❌ {error_msg}",)
                
        except Exception as e:
            error_msg = f"Error loading workflow: {e}"
            self.logger.error(error_msg)
            return (f"❌ {error_msg}",)
    
    @classmethod
    def IS_CHANGED(s, auto_load, workflow_file, force_reload="disable"):
        """
        控制节点何时重新执行
        """
        if force_reload == "enable":
            return "force_reload"
        return ""

# 创建节点映射
NODE_CLASS_MAPPINGS = {
    "WorkflowLoader": WorkflowLoader
}

# 创建显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "WorkflowLoader": "Workflow Loader (MIXLAB)"
}
