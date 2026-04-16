# AI Commit Helper - VS Code Extension

AI-powered Git commit message generator for Visual Studio Code.

## Features

- Generate AI-powered commit messages from staged changes
- Support for multiple formats (Conventional Commits, Chinese, Emoji)
- Web UI integration
- Easy configuration

## Requirements

- Python 3.7+ with `ai-commit-helper` installed
- DeepSeek API key (optional, has free tier)

## Installation

### 1. Install the Python package
```bash
pip install ai-commit-helper
```

### 2. Configure your API key
```bash
# Create config directory
mkdir -p ~/.aicommit

# Create config file
cat > ~/.aicommit/config.yaml << EOF
deepseek:
  api_key: "your-deepseek-api-key"
EOF
```

### 3. Install this extension
- Download from VS Code Marketplace
- Or install from VSIX file

## Usage

1. **Command Palette**: Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "AI Commit Helper" and select a command:
   - **Generate commit message**: Generate from staged changes
   - **Generate from unstaged changes**: Generate from unstaged changes
   - **Open Web UI**: Open the web interface (port 8000)

## Configuration

Open VS Code settings (`Ctrl+,`) and search for "AI Commit Helper":

- **API Key**: Your DeepSeek API key (optional, uses config file by default)
- **Format**: Default commit message format (conventional, zh, emoji)
- **Auto Stage**: Automatically stage changes before generating

## Development

### Build from source
```bash
cd vscode-extension
npm install
npm run compile
```

### Package for distribution
```bash
npm install -g @vscode/vsce
vsce package
```

## Links

- [GitHub Repository](https://github.com/fscyc/ai-commit-helper)
- [PyPI Package](https://pypi.org/project/ai-commit-helper/)
- [npm Package](https://www.npmjs.com/package/ai-commit-helper)

## License

MIT