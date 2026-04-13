"""
核心提交信息生成逻辑
"""

import logging
from typing import Optional, Dict, Any, List
import json
import time

logger = logging.getLogger(__name__)


class CommitMessageGenerator:
    """提交信息生成器"""
    
    def __init__(self, config=None):
        """初始化生成器
        
        Args:
            config: 配置对象，包含API密钥等设置
        """
        self.config = config or {}
        self._setup_api_client()
    
    def _setup_api_client(self):
        """设置API客户端"""
        # 这里根据配置初始化DeepSeek API客户端
        self.api_key = self.config.get("deepseek", {}).get("api_key")
        self.model = self.config.get("deepseek", {}).get("model", "deepseek-chat")
        self.base_url = self.config.get("deepseek", {}).get("base_url", "https://api.deepseek.com")
        
        # 如果没有API密钥，使用模拟模式
        self.mock_mode = not self.api_key
        
        if not self.mock_mode:
            try:
                # 这里应该导入真实的DeepSeek客户端
                # 为了简化，我们先使用requests
                import requests
                self._requests = requests
            except ImportError:
                logger.warning("requests未安装，使用模拟模式")
                self.mock_mode = True
    
    def generate(self, code_diff: str, **kwargs) -> Dict[str, Any]:
        """生成提交信息
        
        Args:
            code_diff: git diff输出
            **kwargs: 额外参数，如format, history等
            
        Returns:
            包含生成结果的字典
        """
        format_type = kwargs.get("format", "conventional")
        history = kwargs.get("history")
        temperature = kwargs.get("temperature", 0.7)
        max_length = kwargs.get("max_length", 100)
        
        logger.info(f"开始生成提交信息，格式: {format_type}")
        
        # 构建提示词
        prompt = self._build_prompt(code_diff, format_type, history)
        
        # 调用AI生成
        if self.mock_mode:
            response = self._mock_generate(prompt, format_type)
        else:
            response = self._call_deepseek_api(prompt, temperature, max_length)
        
        # 解析和格式化结果
        result = self._parse_response(response, format_type)
        
        return {
            "message": result,
            "format": format_type,
            "prompt": prompt,
            "success": True,
        }
    
    def _build_prompt(self, code_diff: str, format_type: str, history: Optional[List[str]] = None) -> str:
        """构建提示词"""
        
        format_instructions = {
            "conventional": """
请按照Conventional Commits格式生成Git提交信息：
格式：type(scope): description

空一行后写body（可选），再空一行后写footer（可选）。

常用type：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整（不影响功能）
- refactor: 重构代码
- test: 测试相关
- chore: 构建过程或辅助工具变动""",
            "zh": """
请生成中文的Git提交信息：
格式：类型(范围): 描述

常用类型：
- 功能: 新功能
- 修复: 修复bug
- 文档: 文档更新
- 样式: 代码格式调整
- 重构: 重构代码
- 测试: 测试相关
- 杂项: 构建过程或辅助工具变动""",
            "emoji": """
请生成带emoji的Git提交信息：
格式：:emoji: 描述

常用emoji：
- ✨ : 新功能
- 🐛 : 修复bug
- 📝 : 文档更新
- 💄 : 代码格式调整
- ♻️ : 重构代码
- ✅ : 测试相关
- 🔧 : 构建过程或辅助工具变动""",
        }
        
        instructions = format_instructions.get(format_type, format_instructions["conventional"])
        
        history_context = ""
        if history and len(history) > 0:
            history_context = "\n\n项目历史提交信息（参考）：\n" + "\n".join(f"- {msg}" for msg in history[:5])
        
        prompt = f"""{instructions}

基于以下代码变更生成提交信息：
```
{code_diff}
```{history_context}

请只输出最终的提交信息，不要包含其他解释。"""
        
        return prompt
    
    def _mock_generate(self, prompt: str, format_type: str) -> str:
        """模拟生成（用于测试或API不可用时）"""
        
        # 根据格式类型返回不同的模拟结果
        mock_responses = {
            "conventional": "feat(core): add commit message generation\n\nImplement AI-powered commit message generator using DeepSeek API.\n\nThis feature helps developers write better commit messages automatically.",
            "zh": "功能(核心): 添加提交信息生成功能\n\n实现基于DeepSeek API的AI提交信息生成器。\n\n此功能帮助开发者自动编写更好的提交信息。",
            "emoji": "✨ 添加提交信息生成功能\n\n实现基于DeepSeek API的AI提交信息生成器。\n\n此功能帮助开发者自动编写更好的提交信息。",
        }
        
        # 模拟API延迟
        time.sleep(0.5)
        
        return mock_responses.get(format_type, mock_responses["conventional"])
    
    def _call_deepseek_api(self, prompt: str, temperature: float, max_length: int) -> str:
        """调用DeepSeek API"""
        
        if self.mock_mode:
            return self._mock_generate(prompt, "conventional")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_length,
            }
            
            response = self._requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"调用DeepSeek API失败: {e}")
            # 失败时回退到模拟模式
            return self._mock_generate(prompt, "conventional")
    
    def _parse_response(self, response: str, format_type: str) -> str:
        """解析API响应，确保格式正确"""
        
        # 清理响应，移除可能的多余内容
        lines = response.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('```') and not line.lower().startswith('here'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)


def generate_commit_message(code_diff: str, **kwargs) -> Dict[str, Any]:
    """生成提交信息的主函数
    
    Args:
        code_diff: git diff输出
        **kwargs: 额外参数
        
    Returns:
        生成结果
    """
    config = kwargs.pop("config", {})
    generator = CommitMessageGenerator(config)
    return generator.generate(code_diff, **kwargs)