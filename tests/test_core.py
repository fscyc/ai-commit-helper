"""
核心功能测试
"""

import pytest
from ai_commit_helper.core import generate_commit_message, CommitMessageGenerator


class TestCommitMessageGenerator:
    """提交信息生成器测试"""
    
    def test_init(self):
        """测试初始化"""
        generator = CommitMessageGenerator()
        assert generator is not None
        assert hasattr(generator, 'config')
        assert hasattr(generator, 'mock_mode')
    
    def test_mock_generation(self):
        """测试模拟生成"""
        generator = CommitMessageGenerator()
        
        # 使用模拟模式生成
        code_diff = "diff --git a/test.py b/test.py"
        result = generator.generate(code_diff, format="conventional")
        
        assert result.get("success") == True
        assert "message" in result
        assert "format" in result
        assert result["format"] == "conventional"
        
        # 检查消息内容
        message = result["message"]
        assert message
        assert isinstance(message, str)
        assert len(message) > 0
    
    def test_different_formats(self):
        """测试不同格式"""
        generator = CommitMessageGenerator()
        code_diff = "test diff"
        
        formats = ["conventional", "zh", "emoji"]
        
        for fmt in formats:
            result = generator.generate(code_diff, format=fmt)
            assert result.get("success") == True
            assert result["format"] == fmt
    
    def test_build_prompt(self):
        """测试提示词构建"""
        generator = CommitMessageGenerator()
        
        code_diff = "test code diff"
        prompt = generator._build_prompt(code_diff, "conventional")
        
        assert isinstance(prompt, str)
        assert "基于以下代码变更生成提交信息" in prompt
        assert code_diff in prompt
        assert "Conventional Commits格式" in prompt
    
    def test_parse_response(self):
        """测试响应解析"""
        generator = CommitMessageGenerator()
        
        # 测试清理响应
        response = "```\nfeat(core): add feature\n\nThis is a new feature.\n```"
        parsed = generator._parse_response(response, "conventional")
        
        assert "```" not in parsed
        assert "feat(core): add feature" in parsed


class TestGenerateCommitMessage:
    """生成提交消息函数测试"""
    
    def test_basic_generation(self):
        """基础生成测试"""
        code_diff = "diff --git a/file.txt b/file.txt"
        result = generate_commit_message(code_diff)
        
        assert isinstance(result, dict)
        assert result.get("success") == True
        assert "message" in result
    
    def test_with_config(self):
        """测试带配置的生成"""
        config = {
            "deepseek": {
                "api_key": "",
                "model": "deepseek-chat",
            }
        }
        
        code_diff = "test diff"
        result = generate_commit_message(code_diff, config=config)
        
        assert result.get("success") == True
    
    def test_with_parameters(self):
        """测试带参数的生成"""
        code_diff = "test diff"
        result = generate_commit_message(
            code_diff,
            format="zh",
            temperature=0.5,
            max_length=50
        )
        
        assert result.get("success") == True
        assert result["format"] == "zh"
    
    @pytest.mark.parametrize("format_type", ["conventional", "zh", "emoji"])
    def test_all_formats(self, format_type):
        """参数化测试所有格式"""
        code_diff = "test diff"
        result = generate_commit_message(code_diff, format=format_type)
        
        assert result.get("success") == True
        assert result["format"] == format_type


def test_error_handling():
    """测试错误处理"""
    generator = CommitMessageGenerator()
    
    # 测试空输入
    result = generator.generate("", format="conventional")
    assert result.get("success") == True  # 即使空输入，模拟模式也会返回结果
    
    # 测试无效格式（应该回退到默认格式）
    result = generator.generate("test diff", format="invalid_format")
    assert result.get("success") == True
    assert result["format"] == "invalid_format"  # 格式会保持原样传递


if __name__ == "__main__":
    # 运行简单测试
    print("运行核心功能测试...")
    
    test_generator = TestCommitMessageGenerator()
    test_generator.test_init()
    test_generator.test_mock_generation()
    test_generator.test_different_formats()
    
    test_func = TestGenerateCommitMessage()
    test_func.test_basic_generation()
    test_func.test_with_config()
    
    print("所有测试通过！")