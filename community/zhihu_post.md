# 我用AI帮你写Git提交信息，每天节省1小时

## 前言
作为程序员，你有没有过这样的经历：
- 写完代码后，面对`git diff`不知道怎么写提交信息
- 随便写个"fix bug"或"update"，后来自己都看不懂
- 团队要求Conventional Commits格式，但记不住规范
- 英文提交信息写得像机翻，自己都尴尬

我也有同样的烦恼，直到我开发了 **AI Commit Helper**。

## 什么是AI Commit Helper？
一个基于DeepSeek AI的Git提交信息自动生成工具。你写代码，AI帮你写提交信息。

## 核心功能
### 🤖 智能理解代码
工具会分析你的`git diff`，理解代码变更的意图：
- 是新功能还是修复bug？
- 改了哪些核心逻辑？
- 影响的模块是什么？

### 📝 多种格式支持
- **Conventional Commits**: `feat(auth): add JWT token validation`
- **中文格式**: `功能(认证): 添加JWT令牌验证`
- **Emoji风格**: `✨ 添加JWT令牌验证`

### 🔄 批量生成
一次生成3-5个不同风格的提交信息，选你最满意的。

### 🎯 历史学习
基于项目之前的提交历史，保持风格一致。

## 安装使用
```bash
# 安装
pip install ai-commit-helper

# 使用（最简单的方式）
aicommit
```

## 真实案例
**修改前：**
```bash
$ git diff
# ... 一堆认证相关的代码修改 ...
$ git commit -m "fix auth"  # 太随意了
```

**使用AI Commit Helper后：**
```bash
$ aicommit
fix(auth): 修复JWT令牌过期时间验证问题
- 添加令牌过期时间验证，防止安全漏洞
- 更新错误信息，便于调试
- 添加令牌验证单元测试
```

## 为什么选择这个工具？
### 1. 完全开源
- MIT许可证，随意使用
- 代码公开透明，无后门
- 社区共同改进

### 2. 保护隐私
- 你的代码diff只发送给DeepSeek API
- 不会被存储或用于其他用途
- 可完全离线使用（模拟模式）

### 3. 多平台支持
- 命令行工具（主力）
- VS Code扩展（开发中）
- Web界面（本地运行）
- API接口（集成到其他工具）

## 技术实现
工具使用Python开发，核心代码不到500行：
- 调用DeepSeek Chat API
- 解析git diff输出
- 格式化提交信息
- 支持自定义模板

## 免费吗？
**完全免费！**
- 工具本身免费开源
- DeepSeek API有免费额度
- 后续会支持其他AI模型

## 如何参与？
1. **使用反馈**：遇到问题或有好建议？
2. **贡献代码**：欢迎PR，项目结构清晰
3. **分享推广**：让更多开发者知道
4. **赞助支持**：GitHub Sponsors支持持续开发

## 适合人群
- 个人开发者：节省时间，规范提交
- 团队项目：统一提交格式，便于维护
- 开源项目：提升项目专业性
- 学生/学习者：学习规范的提交信息写法

## 立即尝试
```bash
pip install ai-commit-helper
cd your-project
git add .
aicommit
```

## 最后的话
这个工具是我为了解决自己的痛点而开发的。用了它之后：
- 提交信息更专业，代码库更清晰
- Code Review时同事不再吐槽我的提交信息
- 自己回看历史时，能快速理解每个提交的意图
- 每天节省至少30-60分钟

如果你也受够了写提交信息，不妨试试。

**项目地址：** https://github.com/fscyc/ai-commit-helper

**问题反馈：** GitHub Issues

**赞助支持：** GitHub Sponsors（支持支付宝）

---

*注：需要DeepSeek API密钥（有免费额度）。工具会发送代码diff到DeepSeek API进行分析，但不会存储你的代码。*