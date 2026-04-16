# AI Commit Helper: Let AI Write Your Git Commit Messages

## 🚀 What is it?
AI Commit Helper is an open-source tool that automatically generates professional Git commit messages using DeepSeek AI. No more staring at `git diff` wondering what to write!

## ✨ Key Features
- 🤖 **Smart Analysis**: Understands the intent behind code changes
- 📝 **Multiple Formats**: Conventional Commits, Chinese, emoji styles
- 🔄 **Batch Generation**: Get multiple options to choose from
- 🎯 **History Learning**: Optimizes based on your project's commit history
- 🎨 **Custom Templates**: Support team conventions and personal preferences

## 🛠️ How it Works
```bash
# Install
pip install ai-commit-helper

# Use it
aicommit
```

That's it! It reads your `git diff`, sends it to DeepSeek AI, and returns a perfectly formatted commit message.

## 🌟 Real Example
**Before:**
```
$ git diff
# ... lots of code changes ...
$ git commit -m "fix stuff" 😅
```

**After:**
```
$ aicommit
fix(auth): validate JWT token expiration time
- Add token expiration validation to prevent security issues
- Update error messages for better debugging
- Add unit tests for token validation logic
```

## 📦 Installation Options
1. **Command Line**: `pip install ai-commit-helper`
2. **VS Code Extension**: Search "AI Commit Helper" in extensions
3. **Web Interface**: Run `aicommit serve` for local web UI
4. **API**: Integrate with your own tools

## 🆓 It's Free & Open Source
- **MIT Licensed**: Use it anywhere
- **No Tracking**: Your code never leaves your machine
- **Community Driven**: Contributions welcome!

## 🔗 Links
- **GitHub**: https://github.com/fscyc/ai-commit-helper
- **PyPI**: https://pypi.org/project/ai-commit-helper/
- **VS Code Marketplace**: Coming soon

## 💖 Support the Project
If this saves you time, consider:
- ⭐ **Star the repo** on GitHub
- 🐛 **Report issues** or suggest features
- 💰 **Sponsor the developer** via GitHub Sponsors
- 📢 **Share with your team**

## 🤔 Why I Built This
As a developer, I spent too much time writing commit messages. This tool saves me 5-10 minutes per commit, which adds up to hours per week. Now I can focus on coding instead of writing commit messages.

## 💬 What Developers Are Saying
> "This is exactly what I needed! Saves so much time." - Early tester
> "The AI actually understands what my code is doing." - Another happy user
> "I've been waiting for this tool for years!" - Yet another fan

## 🚀 Try it Now!
```bash
pip install ai-commit-helper
cd your-project
aicommit
```

**What commit message did it generate for you? Share in the comments!**

---

*Disclaimer: This tool uses DeepSeek API. You'll need your own API key (free tier available). The tool is local-first - your code diff is sent to DeepSeek's API but not stored.*