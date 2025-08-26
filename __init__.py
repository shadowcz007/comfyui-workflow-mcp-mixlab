# ComfyUI Workflow MCP MixLab
# 自动加载默认workflow的自定义节点项目

__version__ = "1.0.0"
__author__ = "MIXLAB"
__description__ = "ComfyUI启动时自动加载默认workflow"

# 导入节点映射
try:
    from .workflow_loader_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    try:
        from workflow_loader_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    except ImportError:
        # 如果都失败，创建空的映射
        NODE_CLASS_MAPPINGS = {}
        NODE_DISPLAY_NAME_MAPPINGS = {}

# 尝试导入回调模块（可选）
try:
    from . import server_callbacks
    __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "server_callbacks"]
except ImportError:
    try:
        import server_callbacks
        __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "server_callbacks"]
    except ImportError:
        __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 