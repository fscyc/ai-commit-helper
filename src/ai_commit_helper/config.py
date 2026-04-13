"""
配置管理
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class Config:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        "deepseek": {
            "api_key": "",
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com",
            "timeout": 30,
        },
        "generation": {
            "default_format": "conventional",
            "max_length": 100,
            "temperature": 0.7,
            "include_emoji": True,
            "max_retries": 3,
        },
        "output": {
            "color": True,
            "verbose": False,
            "save_to_file": False,
            "file_path": "~/.aicommit/history.json",
        },
        "templates": {
            "conventional": "{{type}}({{scope}}): {{description}}\n\n{{body}}\n\n{{footer}}",
            "zh": "{{type}}({{scope}}): {{description}}\n\n{{body}}",
            "emoji": ":{{emoji}}: {{description}}\n\n{{body}}",
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """初始化配置
        
        Args:
            config_file: 配置文件路径，默认为 ~/.aicommit/config.yaml
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        # 确定配置文件路径
        if config_file is None:
            config_file = self._get_default_config_path()
        
        self.config_file = Path(config_file).expanduser()
        
        # 加载配置
        self.load()
        
        # 合并环境变量
        self._merge_env_vars()
    
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        config_dir = Path.home() / ".aicommit"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yaml")
    
    def load(self) -> bool:
        """从文件加载配置"""
        
        if not self.config_file.exists():
            logger.debug(f"配置文件不存在: {self.config_file}")
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f) or {}
            
            # 深度合并配置
            self._deep_merge(self.config, file_config)
            logger.info(f"从 {self.config_file} 加载配置")
            return True
            
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return False
    
    def save(self) -> bool:
        """保存配置到文件"""
        
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"配置已保存到 {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            return False
    
    def _deep_merge(self, target: Dict, source: Dict) -> None:
        """深度合并字典"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def _merge_env_vars(self) -> None:
        """合并环境变量"""
        
        # DeepSeek API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            self.config["deepseek"]["api_key"] = api_key
        
        # 模型设置
        model = os.getenv("DEEPSEEK_MODEL")
        if model:
            self.config["deepseek"]["model"] = model
        
        # 基础URL
        base_url = os.getenv("DEEPSEEK_BASE_URL")
        if base_url:
            self.config["deepseek"]["base_url"] = base_url
        
        # 默认格式
        default_format = os.getenv("AICOMMIT_DEFAULT_FORMAT")
        if default_format:
            self.config["generation"]["default_format"] = default_format
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，支持点分隔符，如 "deepseek.api_key"
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值
        
        Args:
            key: 配置键，支持点分隔符
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        # 导航到最后一个键的父级
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """批量更新配置
        
        Args:
            updates: 更新字典
        """
        for key, value in updates.items():
            self.set(key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """返回配置字典的副本"""
        import copy
        return copy.deepcopy(self.config)
    
    def validate(self) -> bool:
        """验证配置是否有效"""
        
        # 检查DeepSeek API密钥（如果不为mock模式）
        api_key = self.get("deepseek.api_key")
        if not api_key:
            logger.warning("DeepSeek API密钥未设置，将使用模拟模式")
        
        # 检查模型名称
        model = self.get("deepseek.model")
        if not model:
            logger.error("模型名称未设置")
            return False
        
        return True
    
    def get_deepseek_config(self) -> Dict[str, Any]:
        """获取DeepSeek API配置"""
        return self.get("deepseek", {})
    
    def get_generation_config(self) -> Dict[str, Any]:
        """获取生成配置"""
        return self.get("generation", {})
    
    def get_template(self, format_type: str) -> str:
        """获取指定格式的模板"""
        templates = self.get("templates", {})
        return templates.get(format_type, templates.get("conventional"))


def load_config(config_file: Optional[str] = None) -> Config:
    """加载配置的便捷函数"""
    return Config(config_file)