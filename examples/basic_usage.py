#!/usr/bin/env python3
"""
AI Commit Helper 基础使用示例
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_commit_helper import generate_commit_message

def example_basic():
    """基础使用示例"""
    
    # 模拟一个git diff输出
    code_diff = """
diff --git a/src/main.py b/src/main.py
index a1b2c3d..e4f5g6h 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,5 +1,10 @@
 def hello():
-    print("Hello")
+    print("Hello, World!")
+    
+def add(a, b):
+    return a + b

 if __name__ == "__main__":
     hello()
+    result = add(1, 2)
+    print(f"1 + 2 = {result}")
"""
    
    print("示例1: 使用默认格式生成提交信息")
    print("=" * 50)
    
    result = generate_commit_message(code_diff, format="conventional")
    
    if result.get("success"):
        print(f"生成的提交信息:\n{result['message']}")
    else:
        print(f"生成失败: {result}")
    
    print("\n" + "=" * 50)

def example_multiple_formats():
    """多格式示例"""
    
    code_diff = """
diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,5 @@
 # My Project
 
-This is my project.
+This is my awesome project.
+
+## Features
"""
    
    formats = ["conventional", "zh", "emoji"]
    
    for fmt in formats:
        print(f"\n使用 {fmt} 格式:")
        print("-" * 30)
        
        result = generate_commit_message(code_diff, format=fmt)
        
        if result.get("success"):
            print(result['message'])
        else:
            print(f"生成失败")

def example_with_config():
    """使用配置示例"""
    
    code_diff = """
diff --git a/config.yaml b/config.yaml
new file mode 100644
index 0000000..e69de29
"""
    
    # 自定义配置
    config = {
        "deepseek": {
            "api_key": "",  # 如果没有API密钥，会使用模拟模式
            "model": "deepseek-chat",
        },
        "generation": {
            "temperature": 0.8,
            "max_length": 150,
        }
    }
    
    print("\n示例3: 使用自定义配置")
    print("=" * 50)
    
    result = generate_commit_message(
        code_diff,
        format="conventional",
        config=config,
        temperature=0.8
    )
    
    if result.get("success"):
        print(f"生成的提交信息:\n{result['message']}")
    else:
        print(f"生成失败: {result}")

if __name__ == "__main__":
    print("AI Commit Helper 使用示例")
    print("=" * 60)
    
    example_basic()
    example_multiple_formats()
    example_with_config()
    
    print("\n" + "=" * 60)
    print("示例完成！")