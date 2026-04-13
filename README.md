# AI Commit Message Generator

基于AI的Git提交信息生成工具，帮助开发者自动生成专业、规范的提交信息。

## ✨ 功能特性

- 🤖 **智能分析**：理解代码变更的意图和上下文
- 📝 **多种格式**：支持Conventional Commits、中文、emoji风格等多种格式
- 🔄 **批量处理**：一次生成多个提交信息
- 🎯 **历史学习**：基于项目历史优化生成结果
- 🎨 **自定义模板**：支持团队规范和个性化配置
- 🌐 **多平台**：命令行、VS Code扩展、Web界面、API接口

## 🚀 快速开始

### 安装

```bash
# 从PyPI安装
pip install ai-commit-helper

# 或从源码安装
git clone https://github.com/fscyc/ai-commit-helper.git
cd ai-commit-helper
pip install -e .
```

### 基本使用

```bash
# 生成当前暂存区的提交信息
aicommit

# 生成指定文件的提交信息
aicommit --file path/to/file.py

# 使用中文格式
aicommit --format zh

# 使用emoji风格
aicommit --format emoji

# 批量生成多个提交信息
aicommit --batch 5
```

### VS Code扩展

1. 在VS Code扩展商店搜索 "AI Commit Helper"
2. 点击安装
3. 在Git面板中，点击 "Generate Commit Message" 按钮

### Web界面

访问：https://ai-commit-helper.fscyc.github.io

## 🛠️ 开发

### 项目结构

```
ai-commit-helper/
├── src/                    # 核心Python代码
├── web/                    # Web界面代码
├── vscode-extension/       # VS Code扩展
├── tests/                  # 单元测试和集成测试
├── docs/                   # 文档
├── examples/               # 使用示例
├── configs/                # 配置文件
└── scripts/                # 构建和部署脚本
```

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/fscyc/ai-commit-helper.git
cd ai-commit-helper

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 运行测试

```bash
pytest tests/
```

## 🔧 配置

创建配置文件 `~/.aicommit/config.yaml`：

```yaml
# DeepSeek API配置
deepseek:
  api_key: "your-api-key"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"

# 生成选项
generation:
  default_format: "conventional"
  max_length: 100
  temperature: 0.7
  include_emoji: true

# 模板配置
templates:
  conventional: |
    {{type}}({{scope}}): {{description}}
    
    {{body}}
    
    {{footer}}
  zh: |
    {{type}}({{scope}}): {{description}}
    
    {{body}}
```

## 📖 API文档

### Python API

```python
from ai_commit_helper import generate_commit_message

# 生成提交信息
result = generate_commit_message(
    code_diff="...git diff output...",
    format="conventional",
    history=None
)
print(result.message)
```

### REST API

启动本地服务器：

```bash
aicommit serve --port 8000
```

API端点：
- `POST /generate` - 生成提交信息
- `GET /formats` - 获取支持的格式列表
- `POST /batch` - 批量生成

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 💖 赞助

如果这个工具对你有帮助，请考虑赞助支持：

[![GitHub Sponsors](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/fscyc)

## 📞 联系

- GitHub Issues: [问题反馈](https://github.com/fscyc/ai-commit-helper/issues)
- 邮箱: 5888161@qq.com