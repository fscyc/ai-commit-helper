#!/usr/bin/env python3
"""
测试安装和基本功能
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """测试导入"""
    print("测试导入模块...")
    
    try:
        import ai_commit_helper
        print(f"✓ 成功导入 ai_commit_helper (版本: {ai_commit_helper.__version__})")
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False
    
    try:
        from ai_commit_helper import generate_commit_message
        print("✓ 成功导入 generate_commit_message")
    except ImportError as e:
        print(f"✗ 导入 generate_commit_message 失败: {e}")
        return False
    
    try:
        from ai_commit_helper import Config
        print("✓ 成功导入 Config")
    except ImportError as e:
        print(f"✗ 导入 Config 失败: {e}")
        return False
    
    return True

def test_core_functionality():
    """测试核心功能"""
    print("\n测试核心功能...")
    
    from ai_commit_helper import generate_commit_message
    
    # 测试代码
    code_diff = """
diff --git a/test.py b/test.py
index 0000000..1111111
--- a/test.py
+++ b/test.py
@@ -0,0 +1,5 @@
+def hello():
+    print("Hello, World!")
+
+if __name__ == "__main__":
+    hello()
"""
    
    # 测试不同格式
    formats = ["conventional", "zh", "emoji"]
    all_passed = True
    
    for fmt in formats:
        print(f"\n测试 {fmt} 格式...")
        try:
            result = generate_commit_message(code_diff, format=fmt)
            
            if result.get("success"):
                print(f"✓ 生成成功")
                print(f"  消息: {result['message'][:50]}...")
            else:
                print(f"✗ 生成失败")
                all_passed = False
                
        except Exception as e:
            print(f"✗ 测试失败: {e}")
            all_passed = False
    
    return all_passed

def test_config():
    """测试配置"""
    print("\n测试配置管理...")
    
    from ai_commit_helper import Config
    
    try:
        config = Config()
        print("✓ 配置对象创建成功")
        
        # 测试获取配置
        default_format = config.get("generation.default_format")
        print(f"✓ 默认格式: {default_format}")
        
        # 测试设置配置
        config.set("generation.default_format", "zh")
        new_format = config.get("generation.default_format")
        assert new_format == "zh"
        print("✓ 配置设置成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def test_cli():
    """测试CLI"""
    print("\n测试命令行接口...")
    
    try:
        from ai_commit_helper.cli import main
        
        # 这里我们不能直接调用main()，因为它会使用sys.argv
        # 我们只测试导入
        print("✓ CLI模块导入成功")
        
        # 测试帮助信息
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "ai_commit_helper.cli", "--help"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ CLI帮助信息正常")
            return True
        else:
            print(f"✗ CLI帮助信息失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ CLI测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("AI Commit Helper 测试套件")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("核心功能", test_core_functionality),
        ("配置管理", test_config),
        ("命令行接口", test_cli),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*30}")
        print(f"测试: {test_name}")
        print(f"{'='*30}")
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            results.append((test_name, False))
    
    # 显示结果摘要
    print("\n" + "=" * 60)
    print("测试结果摘要:")
    print("=" * 60)
    
    all_passed = True
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name:20} {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())