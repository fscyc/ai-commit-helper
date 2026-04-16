#!/usr/bin/env python3
"""
使用真实DeepSeek API测试项目
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_commit_helper import generate_commit_message

def test_with_real_api():
    """使用真实API测试"""
    
    # 使用真实DeepSeek API密钥的配置
    config = {
        "deepseek": {
            "api_key": "sk-674703edec754e16823acb8a9f771e15",
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com",
            "timeout": 30
        },
        "generation": {
            "temperature": 0.7,
            "max_length": 100,
        }
    }
    
    # 测试代码变更
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
    
    print("=" * 60)
    print("使用真实DeepSeek API测试AI Commit Helper")
    print("=" * 60)
    
    formats = ["conventional", "zh", "emoji"]
    
    for fmt in formats:
        print(f"\n测试 {fmt} 格式:")
        print("-" * 30)
        
        try:
            result = generate_commit_message(
                code_diff,
                format=fmt,
                config=config,
                temperature=0.7
            )
            
            if result.get("success"):
                print(f"✓ 生成成功")
                print(f"消息: {result['message']}")
                
                # 检查是否为模拟模式
                if "feat(core): add commit message generation" in result['message']:
                    print("⚠️  注意：可能仍在模拟模式，检查API密钥")
            else:
                print(f"✗ 生成失败: {result}")
                
        except Exception as e:
            print(f"✗ 生成异常: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_with_real_api()