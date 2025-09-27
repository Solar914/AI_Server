# 🔑 API Key 配置指南

## 当前配置状态

✅ **API Key 已配置完成！**

您的智谱AI API密钥已经设置在 `.env` 文件中：
```
ZHIPU_API_KEY=你的实际API密钥
```

## 🚀 直接运行

现在您可以直接运行程序，无需额外配置：

```bash
python main.py
```

## 🔧 如何修改 API Key

### 方法一：编辑 .env 文件

1. 打开项目根目录下的 `.env` 文件
2. 修改以下内容：
   ```
   ZHIPU_API_KEY=你的新API密钥
   ```
3. 保存文件

### 方法二：重新创建 .env 文件

如果没有 `.env` 文件，可以：

1. 复制示例文件：
   ```bash
   copy .env.example .env
   ```

2. 编辑 `.env` 文件，将 `你的API密钥在这里` 替换为实际的API密钥

## 🔍 验证配置

运行以下命令验证API key是否正确配置：

```bash
python -c "from main import get_api_key; print('API Key配置正确:', len(get_api_key()) > 0)"
```

## 📁 文件位置

```
AI_Server/
├── .env                 ← 实际的API密钥配置（已配置）
├── .env.example         ← 配置示例文件
├── main.py             ← 主程序（会自动读取.env）
└── ...其他文件
```

## ⚠️ 安全提醒

- `.env` 文件已添加到 `.gitignore`，不会被提交到代码仓库
- API密钥请妥善保管，不要分享给他人