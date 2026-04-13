"""
AI Commit Message Generator
基于AI的Git提交信息生成工具
"""

__version__ = "0.1.0"
__author__ = "fscyc"
__email__ = "5888161@qq.com"

from .core import generate_commit_message
from .config import Config
from .formats import get_formats, format_message
from .cli import main

__all__ = [
    "generate_commit_message",
    "Config",
    "get_formats",
    "format_message",
    "main",
]