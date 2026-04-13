"""
提交信息格式管理
"""

import re
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


# 格式定义
FORMATS = {
    "conventional": {
        "name": "Conventional Commits",
        "description": "标准的Conventional Commits格式",
        "pattern": r"^(?P<type>\w+)(?:\((?P<scope>[\w\-\.]+)\))?:\s+(?P<description>.+)$",
        "types": [
            "feat", "fix", "docs", "style", "refactor", 
            "test", "chore", "perf", "ci", "build", "revert"
        ],
        "emoji_map": {
            "feat": "✨",
            "fix": "🐛", 
            "docs": "📝",
            "style": "💄",
            "refactor": "♻️",
            "test": "✅",
            "chore": "🔧",
            "perf": "⚡",
            "ci": "👷",
            "build": "📦",
            "revert": "⏪",
        }
    },
    "zh": {
        "name": "中文格式",
        "description": "中文提交信息格式",
        "pattern": r"^(?P<type>[\u4e00-\u9fff]+)(?:\((?P<scope>[\w\u4e00-\u9fff\-\.]+)\))?:\s+(?P<description>.+)$",
        "types": ["功能", "修复", "文档", "样式", "重构", "测试", "杂项", "性能", "构建"],
        "emoji_map": {
            "功能": "✨",
            "修复": "🐛",
            "文档": "📝", 
            "样式": "💄",
            "重构": "♻️",
            "测试": "✅",
            "杂项": "🔧",
            "性能": "⚡",
            "构建": "📦",
        }
    },
    "emoji": {
        "name": "Emoji格式",
        "description": "使用emoji的提交信息格式",
        "pattern": r"^:(?P<emoji>\w+):\s+(?P<description>.+)$",
        "emoji_list": [
            "✨", "🐛", "📝", "💄", "♻️", "✅", "🔧", "⚡", "👷", "📦", "⏪",
            "🚀", "🎨", "🔥", "🚑", "🎉", "🔒", "🔖", "🚨", "💚", "📌"
        ],
        "type_map": {
            "✨": "feat",
            "🐛": "fix",
            "📝": "docs",
            "💄": "style", 
            "♻️": "refactor",
            "✅": "test",
            "🔧": "chore",
            "⚡": "perf",
            "👷": "ci",
            "📦": "build",
            "⏪": "revert",
        }
    }
}


class FormatValidator:
    """格式验证器"""
    
    def __init__(self, format_type: str = "conventional"):
        self.format_type = format_type
        self.format_def = FORMATS.get(format_type, FORMATS["conventional"])
    
    def validate(self, message: str) -> Tuple[bool, Optional[str]]:
        """验证提交信息是否符合格式要求
        
        Args:
            message: 提交信息
            
        Returns:
            (是否有效, 错误信息)
        """
        if not message or not message.strip():
            return False, "提交信息不能为空"
        
        # 提取第一行（标题）
        lines = message.strip().split('\n')
        title = lines[0].strip()
        
        # 检查格式
        if self.format_type == "emoji":
            return self._validate_emoji(title)
        else:
            return self._validate_conventional(title)
    
    def _validate_conventional(self, title: str) -> Tuple[bool, Optional[str]]:
        """验证conventional格式"""
        pattern = self.format_def["pattern"]
        match = re.match(pattern, title)
        
        if not match:
            return False, f"标题格式不正确，应为：type(scope): description"
        
        type_name = match.group("type")
        valid_types = self.format_def.get("types", [])
        
        if valid_types and type_name not in valid_types:
            return False, f"类型 '{type_name}' 无效，有效类型：{', '.join(valid_types)}"
        
        # 检查描述长度
        description = match.group("description")
        if len(description) < 5:
            return False, "描述太短，应至少5个字符"
        if len(description) > 100:
            return False, "描述太长，应不超过100个字符"
        
        return True, None
    
    def _validate_emoji(self, title: str) -> Tuple[bool, Optional[str]]:
        """验证emoji格式"""
        pattern = self.format_def["pattern"]
        match = re.match(pattern, title)
        
        if not match:
            return False, f"标题格式不正确，应为：:emoji: description"
        
        emoji = match.group("emoji")
        emoji_list = self.format_def.get("emoji_list", [])
        
        # 检查emoji是否在列表中（转换为实际emoji字符）
        if emoji_list and f":{emoji}:" not in emoji_list:
            # 如果emoji参数是文字（如"sparkles"），检查映射
            if emoji in ["sparkles", "bug", "memo", "lipstick", "recycle", "white_check_mark", "wrench", "zap", "construction_worker", "package", "rewind"]:
                pass  # 常见emoji文字别名
            else:
                return False, f"emoji ':{}:' 无效，有效emoji：{', '.join(emoji_list)}"
        
        description = match.group("description")
        if len(description) < 5:
            return False, "描述太短，应至少5个字符"
        if len(description) > 100:
            return False, "描述太长，应不超过100个字符"
        
        return True, None
    
    def parse(self, message: str) -> Optional[Dict[str, str]]:
        """解析提交信息
        
        Args:
            message: 提交信息
            
        Returns:
            解析后的字典，包含type, scope, description等字段
        """
        lines = message.strip().split('\n')
        title = lines[0].strip()
        
        if self.format_type == "emoji":
            return self._parse_emoji(title, lines[1:] if len(lines) > 1 else [])
        else:
            return self._parse_conventional(title, lines[1:] if len(lines) > 1 else [])
    
    def _parse_conventional(self, title: str, body_lines: List[str]) -> Dict[str, str]:
        """解析conventional格式"""
        pattern = self.format_def["pattern"]
        match = re.match(pattern, title)
        
        if not match:
            return {}
        
        result = {
            "type": match.group("type"),
            "scope": match.group("scope") or "",
            "description": match.group("description"),
            "body": "\n".join(body_lines).strip(),
            "format": self.format_type,
        }
        
        # 添加emoji
        emoji_map = self.format_def.get("emoji_map", {})
        if result["type"] in emoji_map:
            result["emoji"] = emoji_map[result["type"]]
        
        return result
    
    def _parse_emoji(self, title: str, body_lines: List[str]) -> Dict[str, str]:
        """解析emoji格式"""
        pattern = self.format_def["pattern"]
        match = re.match(pattern, title)
        
        if not match:
            return {}
        
        emoji = match.group("emoji")
        type_map = self.format_def.get("type_map", {})
        
        # 将emoji文字转换为实际emoji
        emoji_text = f":{emoji}:"
        actual_emoji = None
        for e in self.format_def.get("emoji_list", []):
            if emoji_text in e or emoji in e:
                actual_emoji = e
                break
        
        if not actual_emoji:
            actual_emoji = emoji_text
        
        result = {
            "emoji": actual_emoji,
            "description": match.group("description"),
            "body": "\n".join(body_lines).strip(),
            "format": self.format_type,
        }
        
        # 映射到类型
        if actual_emoji in type_map:
            result["type"] = type_map[actual_emoji]
        
        return result
    
    def convert(self, message: str, target_format: str) -> Optional[str]:
        """转换格式
        
        Args:
            message: 原始提交信息
            target_format: 目标格式
            
        Returns:
            转换后的提交信息
        """
        # 先解析原始消息
        parsed = self.parse(message)
        if not parsed:
            return None
        
        # 获取目标格式定义
        target_def = FORMATS.get(target_format, FORMATS["conventional"])
        
        # 根据目标格式构建消息
        if target_format == "emoji":
            return self._build_emoji_message(parsed, target_def)
        else:
            return self._build_conventional_message(parsed, target_def)
    
    def _build_conventional_message(self, parsed: Dict, target_def: Dict) -> str:
        """构建conventional格式消息"""
        type_name = parsed.get("type", "chore")
        scope = parsed.get("scope", "")
        description = parsed.get("description", "")
        body = parsed.get("body", "")
        
        # 如果是从emoji转换，需要映射类型
        if parsed.get("format") == "emoji":
            # 反向查找emoji对应的类型
            emoji = parsed.get("emoji", "")
            for t, e in target_def.get("emoji_map", {}).items():
                if e == emoji:
                    type_name = t
                    break
        
        # 构建标题
        if scope:
            title = f"{type_name}({scope}): {description}"
        else:
            title = f"{type_name}: {description}"
        
        # 添加正文
        result = title
        if body:
            result += f"\n\n{body}"
        
        return result
    
    def _build_emoji_message(self, parsed: Dict, target_def: Dict) -> str:
        """构建emoji格式消息"""
        emoji = parsed.get("emoji", "✨")
        description = parsed.get("description", "")
        body = parsed.get("body", "")
        
        # 如果是从conventional转换，需要映射emoji
        if parsed.get("format") != "emoji":
            type_name = parsed.get("type", "chore")
            emoji_map = target_def.get("emoji_map", FORMATS["conventional"]["emoji_map"])
            emoji = emoji_map.get(type_name, "✨")
        
        # 构建标题
        title = f"{emoji} {description}"
        
        # 添加正文
        result = title
        if body:
            result += f"\n\n{body}"
        
        return result


def get_formats() -> List[str]:
    """获取所有支持的格式"""
    return list(FORMATS.keys())


def get_format_info(format_type: str) -> Dict:
    """获取格式详细信息"""
    return FORMATS.get(format_type, FORMATS["conventional"])


def format_message(message: str, format_type: str, target_format: Optional[str] = None) -> str:
    """格式化提交信息
    
    Args:
        message: 原始提交信息
        format_type: 原始格式
        target_format: 目标格式，如果为None则保持原格式
        
    Returns:
        格式化后的提交信息
    """
    if target_format is None or target_format == format_type:
        return message
    
    validator = FormatValidator(format_type)
    return validator.convert(message, target_format) or message


def validate_message(message: str, format_type: str = "conventional") -> Tuple[bool, Optional[str]]:
    """验证提交信息
    
    Args:
        message: 提交信息
        format_type: 格式类型
        
    Returns:
        (是否有效, 错误信息)
    """
    validator = FormatValidator(format_type)
    return validator.validate(message)