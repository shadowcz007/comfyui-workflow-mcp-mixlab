# ComfyUI API 工具化实现

这个目录包含了将 ComfyUI API 接口直接对接到 MCP 工具的完整实现。

## 架构设计

### 基础架构
- `base_tools.py` - 提供对 ComfyUI 服务器实例的访问
- `workflow_tools.py` - 工作流执行相关工具
- `history_tools.py` - 历史记录管理工具
- `file_tools.py` - 文件上传和管理工具
- `system_tools.py` - 系统信息工具

### 核心特性
- **直接对接**: 工具直接调用 ComfyUI 的 API 方法，而不是转发 HTTP 请求
- **异步支持**: 正确处理 ComfyUI 的异步 API 方法
- **错误处理**: 完善的错误处理和异常捕获
- **类型安全**: 使用类型注解确保参数类型正确

## 可用工具

### 🔄 工作流执行相关工具

#### `submit_workflow`
提交工作流执行请求
```python
submit_workflow(workflow_json: str, client_id: str = None, prompt_id: str = None)
```

#### `get_queue_info`
获取队列信息
```python
get_queue_info()
```

#### `clear_queue`
清除队列中的所有任务
```python
clear_queue()
```

#### `delete_queue_item`
删除队列中的特定任务
```python
delete_queue_item(prompt_id: str)
```

#### `interrupt_processing`
中断当前处理
```python
interrupt_processing()
```

#### `free_memory`
释放内存和模型
```python
free_memory(unload_models: bool = False, free_memory: bool = False)
```

### 📚 历史记录管理工具

#### `get_history`
获取历史记录
```python
get_history(max_items: int = None)
```

#### `get_history_by_id`
根据ID获取特定的历史记录
```python
get_history_by_id(prompt_id: str)
```

#### `clear_history`
清除所有历史记录
```python
clear_history()
```

#### `delete_history_item`
删除特定的历史记录项
```python
delete_history_item(prompt_id: str)
```

### 📁 文件上传和管理工具

#### `list_models`
获取所有模型类型列表
```python
list_models()
```

#### `list_models_by_folder`
获取特定文件夹的模型列表
```python
list_models_by_folder(folder: str)
```

#### `list_embeddings`
获取嵌入模型列表
```python
list_embeddings()
```

#### `list_extensions`
获取扩展列表
```python
list_extensions()
```

#### `view_metadata`
查看模型元数据
```python
view_metadata(folder_name: str, filename: str)
```

#### `upload_image`
上传图片文件
```python
upload_image(image_path: str, subfolder: str = "", upload_type: str = "input", overwrite: bool = False)
```

#### `view_image`
查看图片文件
```python
view_image(filename: str, image_type: str = "output", subfolder: str = "", channel: str = "rgba", preview: str = None)
```

### 💻 系统信息工具

#### `get_system_stats`
获取系统状态信息
```python
get_system_stats()
```

#### `get_features`
获取功能特性信息
```python
get_features()
```

#### `get_object_info`
获取所有节点信息
```python
get_object_info()
```

#### `get_object_info_by_node`
获取特定节点的信息
```python
get_object_info_by_node(node_class: str)
```

#### `get_queue_status`
获取队列状态信息
```python
get_queue_status()
```

#### `get_prompt_status`
获取提示状态信息
```python
get_prompt_status()
```

## 使用示例

### 基本使用
```python
from tools import submit_workflow, get_system_stats

# 提交工作流
workflow_json = '{"3": {"class_type": "KSampler", "inputs": {...}}}'
result = submit_workflow(workflow_json)
print(result)

# 获取系统状态
stats = get_system_stats()
print(stats)
```

### 在 MCP 服务器中使用
```python
from fastmcp import FastMCP
from tools import submit_workflow

mcp = FastMCP("ComfyUI Tools")

@mcp.tool
def submit_workflow_tool(workflow_json: str) -> str:
    """提交工作流执行请求"""
    result = submit_workflow(workflow_json)
    return str(result)

mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

## 技术实现细节

### 异步处理
由于 ComfyUI 的 API 方法大多是异步的，我们使用了以下模式来处理：

```python
async def async_method():
    # 异步调用 ComfyUI API
    response = await comfyui_method(mock_request)
    return response

# 在同步环境中运行异步函数
loop = asyncio.get_event_loop()
if loop.is_running():
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        result = new_loop.run_until_complete(async_method())
    finally:
        new_loop.close()
else:
    result = loop.run_until_complete(async_method())
```

### 模拟请求对象
为了直接调用 ComfyUI 的 API 方法，我们创建了模拟的请求对象：

```python
def create_mock_request(self, **kwargs):
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
```

## 错误处理

所有工具都包含完善的错误处理：

```python
try:
    # 执行操作
    result = some_operation()
    return result
except Exception as e:
    return {"error": f"操作失败: {e}"}
```

## 扩展开发

要添加新的工具，请遵循以下步骤：

1. 在相应的工具文件中添加新函数
2. 确保函数有正确的类型注解和文档字符串
3. 在 `__init__.py` 中导出新函数
4. 在 `server_callbacks.py` 中添加对应的 MCP 工具装饰器

## 注意事项

1. **服务器实例**: 确保 ComfyUI 服务器已经启动
2. **异步处理**: 正确处理异步 API 调用
3. **错误处理**: 始终包含适当的错误处理
4. **类型安全**: 使用类型注解确保参数正确
5. **文档**: 为每个工具提供清晰的文档字符串 