# 快速开始指南

AI Commit Helper 是一个基于 AI 的 Git 提交信息生成工具，帮助开发者自动生成专业、规范的提交信息。

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install ai-commit-helper
```

### 从源码安装

```bash
git clone https://github.com/fscyc/ai-commit-helper.git
cd ai-commit-helper
pip install -e .
```

## 基本使用

### 命令行工具

安装后，你可以使用 `aicommit` 命令：

```bash
# 生成当前暂存区变更的提交信息
aicommit

# 使用中文格式
aicommit --format zh

# 生成指定文件的提交信息
aicommit --file path/to/file.py

# 批量生成多个提交信息
aicommit --batch 3

# 进入交互式模式
aicommit interactive
```

### Python API

```python
from ai_commit_helper import generate_commit_message

# 生成提交信息
code_diff = """diff --git a/main.py b/main.py
index a1b2c3d..e4f5g6h 100644
--- a/main.py
+++ b/main.py
@@ -1,5 +1,8 @@
 def hello():
-    print("Hello")
+    print("Hello, World!")
"""

result = generate_commit_message(code_diff, format="conventional")

if result["success"]:
    print(result["message"])
```

## 配置

### 设置 DeepSeek API 密钥

为了使用真实的 AI 生成功能，你需要设置 DeepSeek API 密钥：

1. 创建配置文件 `~/.aicommit/config.yaml`：

```yaml
deepseek:
  api_key: "sk-your-deepseek-api-key"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
```

2. 或通过环境变量设置：

```bash
export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"
export DEEPSEEK_MODEL="deepseek-chat"
```

### 配置文件示例

完整的配置文件示例：

```yaml
# DeepSeek API 配置
deepseek:
  api_key: "sk-your-api-key"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
  timeout: 30

# 生成选项
generation:
  default_format: "conventional"
  max_length: 100
  temperature: 0.7
  include_emoji: true
  max_retries: 3

# 输出选项
output:
  color: true
  verbose: false
  save_to_file: false
  file_path: "~/.aicommit/history.json"
```

## 支持的格式

### 1. Conventional Commits（默认）

标准的 Conventional Commits 格式：

```
feat(core): add new feature

This is a detailed description of the feature.

BREAKING CHANGE: API changed
```

### 2. 中文格式

中文提交信息格式：

```
功能(核心): 添加新功能

这是功能的详细描述。
```

### 3. Emoji 格式

使用 emoji 的格式：

```
✨ 添加新功能

这是功能的详细描述。
```

## 高级功能

### 批量生成

一次生成多个备选提交信息：

```bash
aicommit --batch 5
```

### 历史学习

参考项目历史提交信息来优化生成：

```bash
# 参考最近5个提交
aicommit --history 5
```

### Web 服务器

启动一个 Web 服务器提供 API 接口：

```bash
aicommit serve --port 8000
```

然后可以访问：
- API 文档: http://localhost:8000/docs
- 生成接口: POST http://localhost:8000/generate

### 格式验证

验证提交信息是否符合规范：

```bash
# 验证提交信息
aicommit validate "feat(core): add feature"

# 从文件验证
aicommit validate --file commit_message.txt
```

### 格式转换

将提交信息从一种格式转换为另一种格式：

```python
from ai_commit_helper.formats import format_message

# 从 conventional 转换为 emoji 格式
converted = format_message(
    "feat(core): add feature",
    format_type="conventional",
    target_format="emoji"
)
print(converted)  # ✨ 添加功能
```

## VS Code 扩展

我们还提供了 VS Code 扩展，可以在编辑器中直接使用：

1. 在 VS Code 中搜索扩展 "AI Commit Helper"
2. 点击安装
3. 在 Git 面板中，点击 "Generate Commit Message" 按钮

## 常见问题

### Q: 没有 DeepSeek API 密钥可以使用吗？
A: 可以，工具会自动使用模拟模式生成示例提交信息。

### Q: 如何自定义提交信息模板？
A: 在配置文件的 `templates` 部分自定义模板：

```yaml
templates:
  conventional: |
    {{type}}({{scope}}): {{description}}
    
    {{body}}
    
    {{footer}}
```

### Q: 支持哪些 Git 客户端？
A: 支持所有标准 Git 客户端，包括命令行、VS Code、GitKraken 等。

### Q: 如何贡献代码？
A: 欢迎提交 Pull Request！请查看 [贡献指南](../CONTRIBUTING.md)。

## 下一步

- 查看 [完整文档](./index.md)
- 阅读 [API 参考](./api.md)
- 加入 [GitHub Discussions](https://github.com/fscyc/ai-commit-helper/discussions)