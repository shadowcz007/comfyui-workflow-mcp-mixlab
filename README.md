# ComfyUI Workflow MCP MixLab

这是一个为 ComfyUI 提供 MCP (Model Context Protocol) 服务器功能的自定义节点包，**直接对接到 ComfyUI 的 API 接口**。

## 🚀 功能特性

- 🚀 基于 FastMCP 的 SSE 传输协议
- 🔧 **直接对接 ComfyUI API 接口**，无需 HTTP 转发
- 🎯 与 ComfyUI 工作流深度集成
- 📡 支持实时状态监控
- 🛠️ **完整的 API 工具化实现**

## 📦 安装

1. 确保你已经安装了 ComfyUI
2. 将此文件夹放置在 `ComfyUI/custom_nodes/` 目录下
3. 安装依赖包：

```bash
cd ComfyUI/custom_nodes/comfyui-workflow-mcp-mixlab
python install_dependencies.py
```

或者手动安装：

```bash
pip install fastmcp>=0.1.0
```

## 🔧 核心功能

### API 工具化实现

本项目实现了 ComfyUI API 接口的完整工具化，**直接调用 ComfyUI 的内部方法**，而不是通过 HTTP 请求转发。这提供了更好的性能和更直接的集成。

#### 可用的工具类别：

1. **🔄 工作流执行相关**
   - `submit_workflow` - 提交工作流执行请求
   - `get_queue_info` - 获取队列信息
   - `clear_queue` - 清除队列中的所有任务
   - `delete_queue_item` - 删除队列中的特定任务
   - `interrupt_processing` - 中断当前处理
   - `free_memory` - 释放内存和模型

2. **📚 历史记录管理**
   - `get_history` - 获取历史记录
   - `get_history_by_id` - 根据ID获取特定的历史记录
   - `clear_history` - 清除所有历史记录
   - `delete_history_item` - 删除特定的历史记录项

3. **📁 文件上传和管理**
   - `list_models` - 获取所有模型类型列表
   - `list_models_by_folder` - 获取特定文件夹的模型列表
   - `list_embeddings` - 获取嵌入模型列表
   - `list_extensions` - 获取扩展列表
   - `view_metadata` - 查看模型元数据
   - `upload_image` - 上传图片文件
   - `view_image` - 查看图片文件

4. **💻 系统信息**
   - `get_system_stats` - 获取系统状态信息
   - `get_features` - 获取功能特性信息
   - `get_object_info` - 获取所有节点信息
   - `get_object_info_by_node` - 获取特定节点的信息
   - `get_queue_status` - 获取队列状态信息
   - `get_prompt_status` - 获取提示状态信息

## 🚀 使用方法

### 自动启动

当 ComfyUI 服务器启动时，MCP 服务器会自动在后台启动，使用 SSE 传输协议在 `http://127.0.0.1:7397` 上运行。

### 手动启动

你也可以手动启动 MCP 服务器：

```python
from server_callbacks import start_mcp_server

# 启动 MCP 服务器
start_mcp_server()
```

## 🔧 工具使用示例

### 基本工具使用

```python
# 获取系统状态
from tools import get_system_stats
stats = get_system_stats()
print(stats)

# 提交工作流
from tools import submit_workflow
workflow_json = '{"3": {"class_type": "KSampler", "inputs": {...}}}'
result = submit_workflow(workflow_json)
print(result)

# 获取模型列表
from tools import list_models
models = list_models()
print(models)
```

### MCP 客户端连接

你可以使用支持 MCP 协议的客户端连接到服务器：

```python
# 示例客户端代码
import requests

# 连接到 MCP 服务器
response = requests.get("http://127.0.0.1:7397")
print(response.text)
```

## 🏗️ 架构设计

### 工具架构

```
tools/
├── __init__.py          # 工具包初始化
├── base_tools.py        # 基础工具类，提供服务器访问
├── workflow_tools.py    # 工作流执行相关工具
├── history_tools.py     # 历史记录管理工具
├── file_tools.py        # 文件上传和管理工具
├── system_tools.py      # 系统信息工具
└── README.md           # 工具使用文档
```

### 核心特性

- **直接对接**: 工具直接调用 ComfyUI 的 API 方法，而不是转发 HTTP 请求
- **异步支持**: 正确处理 ComfyUI 的异步 API 方法
- **错误处理**: 完善的错误处理和异常捕获
- **类型安全**: 使用类型注解确保参数类型正确

## ⚙️ 配置

MCP 服务器默认配置：
- 主机：0.0.0.0
- 端口：7397
- 传输协议：SSE
- CORS：已启用

你可以在 `server_callbacks.py` 中修改这些配置。

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   - 修改 `server_callbacks.py` 中的端口号

2. **依赖包未安装**
   - 运行 `python install_dependencies.py`

3. **权限问题**
   - 确保有足够的权限绑定端口

4. **ComfyUI 服务器未启动**
   - 确保 ComfyUI 服务器已经启动

### 日志

查看 ComfyUI 的控制台输出来获取 MCP 服务器的运行状态和错误信息。

## 🛠️ 开发

### 添加新工具

在相应的工具文件中添加新函数：

```python
# 在 workflow_tools.py 中添加
def your_new_tool(param: str) -> Dict[str, Any]:
    """你的新工具描述"""
    try:
        # 实现逻辑
        return {"result": "success"}
    except Exception as e:
        return {"error": str(e)}
```

然后在 `server_callbacks.py` 中添加对应的 MCP 工具装饰器：

```python
@mcp.tool
def your_new_tool_tool(param: str) -> str:
    """你的新工具描述"""
    result = your_new_tool(param)
    return str(result)
```

### 自定义配置

你可以修改服务器配置来适应你的需求：

```python
mcp.run(transport="sse", host="0.0.0.0", port=9000)
```

## 📄 许可证

本项目遵循 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📚 相关文档

- [ComfyUI API 文档](https://github.com/comfyanonymous/ComfyUI)
- [FastMCP 文档](https://github.com/fastmcp/fastmcp)
- [MCP 协议规范](https://modelcontextprotocol.io/)

