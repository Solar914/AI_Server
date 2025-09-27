# API Key 配置说明

## 修改内容

本次修改将原来硬编码在 `chatglm.py` 中的 API key 改为由用户提供，提高了安全性和灵活性。

## 主要变更

### 1. ChatGLM 类修改 (`ai_core/llm/chatglm.py`)

- ✅ 移除了构造函数和 `get_instance` 方法中的默认 API key
- ✅ 现在 API key 成为必填参数
- ✅ 添加了 API key 验证，确保不能为空
- ✅ 修复了API响应解析的问题

### 2. Main 程序修改 (`main.py`)

- ✅ 添加了 `get_api_key()` 函数，支持从 .env 文件和用户输入获取
- ✅ 更新了所有 ChatGLM 实例创建的地方，传入 API key
- ✅ 添加了 python-dotenv 支持，可从 .env 文件读取配置

### 3. 新增文件

- ✅ `.env.example` - API key 配置示例文件
- ✅ `.env` - 实际的环境变量文件（包含在 .gitignore 中）

### 4. 依赖更新

- ✅ 更新 `requirements.txt`，添加了 `python-dotenv`

## 使用方式

### 方法一：.env 文件（推荐）

1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 文件中设置：
   ```
   ZHIPU_API_KEY=你的API密钥
   ```

### 方法二：运行时输入

如果没有设置 .env 文件，程序会提示用户输入 API key。

## 安全性改进

- ✅ API key 不再硬编码在源代码中
- ✅ .env 文件已添加到 .gitignore，避免意外提交
- ✅ API key 显示时只显示前10位，保护隐私
- ✅ 提供了示例配置文件，便于用户设置

## 测试验证

所有功能已通过测试：
- ✅ .env 文件读取正常
- ✅ 用户输入功能正常
- ✅ ChatGLM API 调用正常
- ✅ EdgeTTS 语音合成正常
- ✅ 完整的演示流程正常

现在你的 API key 已经安全地从硬编码中移除，可以通过 .env 文件或运行时输入的方式灵活配置！