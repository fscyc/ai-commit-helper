"""
命令行接口
"""

import argparse
import sys
import os
import subprocess
from pathlib import Path
from typing import Optional, List
import logging

from .core import generate_commit_message
from .config import Config
from .formats import get_formats, validate_message, format_message

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_git_diff(staged: bool = True, file_path: Optional[str] = None) -> str:
    """获取git diff输出
    
    Args:
        staged: 是否获取暂存区的diff
        file_path: 指定文件路径
        
    Returns:
        git diff输出
    """
    try:
        cmd = ["git", "diff"]
        
        if staged:
            cmd.append("--cached")
        
        if file_path:
            cmd.append(file_path)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            logger.error(f"git diff失败: {result.stderr}")
            return ""
        
        diff_output = result.stdout.strip()
        
        if not diff_output:
            if staged:
                logger.warning("暂存区没有变更，尝试获取未暂存的变更")
                return get_git_diff(staged=False, file_path=file_path)
            else:
                logger.error("没有找到代码变更")
                return ""
        
        return diff_output
        
    except FileNotFoundError:
        logger.error("git未安装或不在PATH中")
        return ""
    except Exception as e:
        logger.error(f"获取git diff失败: {e}")
        return ""


def get_git_history(limit: int = 10) -> List[str]:
    """获取git历史提交信息
    
    Args:
        limit: 获取的数量限制
        
    Returns:
        提交信息列表
    """
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{limit}"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            return []
        
        # 提取提交信息（去掉hash部分）
        lines = result.stdout.strip().split('\n')
        messages = []
        
        for line in lines:
            if line:
                # 去掉开头的commit hash
                parts = line.split(' ', 1)
                if len(parts) > 1:
                    messages.append(parts[1].strip())
        
        return messages
        
    except Exception:
        return []


def display_result(result: dict, color: bool = True):
    """显示生成结果
    
    Args:
        result: 生成结果字典
        color: 是否使用颜色
    """
    if not result.get("success", False):
        print("生成失败")
        return
    
    message = result.get("message", "")
    format_type = result.get("format", "conventional")
    
    if color:
        # 简单的颜色输出
        try:
            from colorama import init, Fore, Style
            init()
            
            print(f"\n{Fore.GREEN}生成的提交信息 ({format_type}):{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
            
        except ImportError:
            # 如果没有colorama，使用普通输出
            print(f"\n生成的提交信息 ({format_type}):")
            print("-" * 50)
            print(message)
            print("-" * 50)
    else:
        print(f"\n生成的提交信息 ({format_type}):")
        print("-" * 50)
        print(message)
        print("-" * 50)
    
    # 显示验证结果
    from .formats import validate_message
    is_valid, error = validate_message(message, format_type)
    
    if is_valid:
        if color:
            try:
                from colorama import Fore, Style
                print(f"{Fore.GREEN}✓ 格式验证通过{Style.RESET_ALL}")
            except ImportError:
                print("✓ 格式验证通过")
    else:
        if color:
            try:
                from colorama import Fore, Style
                print(f"{Fore.RED}✗ 格式验证失败: {error}{Style.RESET_ALL}")
            except ImportError:
                print(f"✗ 格式验证失败: {error}")
        else:
            print(f"✗ 格式验证失败: {error}")


def interactive_mode(config: Config):
    """交互式模式"""
    print("进入交互式模式 (输入 'quit' 退出)")
    
    while True:
        try:
            print("\n" + "=" * 50)
            print("1. 生成当前git变更的提交信息")
            print("2. 输入自定义代码变更")
            print("3. 切换格式")
            print("4. 查看支持的格式")
            print("5. 验证提交信息")
            print("6. 格式转换")
            print("7. 退出")
            print("=" * 50)
            
            choice = input("\n请选择操作 (1-7): ").strip()
            
            if choice == "1":
                # 生成当前git变更
                diff = get_git_diff()
                if not diff:
                    print("没有找到git变更")
                    continue
                
                format_type = config.get("generation.default_format", "conventional")
                history = get_git_history(5)
                
                print("正在生成...")
                result = generate_commit_message(
                    diff,
                    format=format_type,
                    history=history,
                    config=config.to_dict()
                )
                
                display_result(result, config.get("output.color", True))
                
                # 询问是否使用
                use = input("\n是否使用这个提交信息？ (y/n): ").strip().lower()
                if use == 'y':
                    # 这里可以实际执行git commit
                    commit_cmd = f'git commit -m "{result["message"].split(chr(10))[0]}"'
                    print(f"可以运行: {commit_cmd}")
            
            elif choice == "2":
                # 输入自定义代码变更
                print("\n请输入代码变更 (git diff格式):")
                print("(输入END结束输入)")
                
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                
                diff = '\n'.join(lines)
                if not diff.strip():
                    print("输入为空")
                    continue
                
                format_type = config.get("generation.default_format", "conventional")
                
                print("正在生成...")
                result = generate_commit_message(
                    diff,
                    format=format_type,
                    config=config.to_dict()
                )
                
                display_result(result, config.get("output.color", True))
            
            elif choice == "3":
                # 切换格式
                formats = get_formats()
                print("\n支持的格式:")
                for i, fmt in enumerate(formats, 1):
                    print(f"{i}. {fmt}")
                
                fmt_choice = input(f"\n选择格式 (1-{len(formats)}): ").strip()
                try:
                    idx = int(fmt_choice) - 1
                    if 0 <= idx < len(formats):
                        config.set("generation.default_format", formats[idx])
                        print(f"已切换为 {formats[idx]} 格式")
                    else:
                        print("无效的选择")
                except ValueError:
                    print("请输入数字")
            
            elif choice == "4":
                # 查看支持的格式
                formats = get_formats()
                print("\n支持的格式:")
                for fmt in formats:
                    print(f"- {fmt}")
            
            elif choice == "5":
                # 验证提交信息
                print("\n请输入要验证的提交信息:")
                print("(输入END结束输入)")
                
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                
                message = '\n'.join(lines)
                if not message.strip():
                    print("输入为空")
                    continue
                
                format_type = config.get("generation.default_format", "conventional")
                from .formats import validate_message
                is_valid, error = validate_message(message, format_type)
                
                if is_valid:
                    print("✓ 格式验证通过")
                else:
                    print(f"✗ 格式验证失败: {error}")
            
            elif choice == "6":
                # 格式转换
                print("\n请输入要转换的提交信息:")
                print("(输入END结束输入)")
                
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                
                message = '\n'.join(lines)
                if not message.strip():
                    print("输入为空")
                    continue
                
                formats = get_formats()
                print("\n支持的格式:")
                for i, fmt in enumerate(formats, 1):
                    print(f"{i}. {fmt}")
                
                fmt_choice = input(f"\n选择目标格式 (1-{len(formats)}): ").strip()
                try:
                    idx = int(fmt_choice) - 1
                    if 0 <= idx < len(formats):
                        target_format = formats[idx]
                        converted = format_message(message, "conventional", target_format)
                        print(f"\n转换后的提交信息 ({target_format}):")
                        print("-" * 50)
                        print(converted)
                        print("-" * 50)
                    else:
                        print("无效的选择")
                except ValueError:
                    print("请输入数字")
            
            elif choice == "7" or choice.lower() == "quit":
                print("退出交互式模式")
                break
            
            else:
                print("无效的选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n\n退出交互式模式")
            break
        except Exception as e:
            logger.error(f"交互式模式错误: {e}")
            print(f"发生错误: {e}")


def serve_mode(config: Config, port: int = 8000, host: str = "127.0.0.1"):
    """启动Web服务器模式"""
    try:
        import uvicorn
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        
        app = FastAPI(title="AI Commit Helper API", version="0.1.0")
        
        class GenerateRequest(BaseModel):
            code_diff: str
            format: str = "conventional"
            history: Optional[List[str]] = None
        
        @app.get("/")
        async def root():
            return {"message": "AI Commit Helper API", "version": "0.1.0"}
        
        @app.get("/formats")
        async def get_formats_list():
            return {"formats": get_formats()}
        
        @app.post("/generate")
        async def generate(request: GenerateRequest):
            try:
                result = generate_commit_message(
                    request.code_diff,
                    format=request.format,
                    history=request.history,
                    config=config.to_dict()
                )
                
                if not result.get("success", False):
                    raise HTTPException(status_code=500, detail="生成失败")
                
                return result
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/batch")
        async def batch_generate(requests: List[GenerateRequest]):
            results = []
            for req in requests:
                try:
                    result = generate_commit_message(
                        req.code_diff,
                        format=req.format,
                        history=req.history,
                        config=config.to_dict()
                    )
                    results.append(result)
                except Exception as e:
                    results.append({"success": False, "error": str(e)})
            
            return {"results": results}
        
        print(f"启动Web服务器: http://{host}:{port}")
        print("接口文档: http://{host}:{port}/docs")
        
        uvicorn.run(app, host=host, port=port)
        
    except ImportError as e:
        logger.error(f"启动Web服务器需要额外依赖: {e}")
        print("安装Web服务器依赖: pip install fastapi uvicorn")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AI Commit Message Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 生成当前暂存区变更的提交信息
  %(prog)s --format zh        # 使用中文格式
  %(prog)s --file main.py     # 生成指定文件的提交信息
  %(prog)s --interactive      # 进入交互式模式
  %(prog)s serve --port 8000  # 启动Web服务器
        """
    )
    
    # 通用选项
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="详细输出"
    )
    
    parser.add_argument(
        "--config",
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="禁用颜色输出"
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # generate命令
    gen_parser = subparsers.add_parser("generate", help="生成提交信息")
    gen_parser.add_argument(
        "--format",
        choices=get_formats(),
        default="conventional",
        help="输出格式"
    )
    gen_parser.add_argument(
        "--file",
        help="指定文件路径"
    )
    gen_parser.add_argument(
        "--staged",
        action="store_true",
        default=True,
        help="使用暂存区变更（默认）"
    )
    gen_parser.add_argument(
        "--no-staged",
        dest="staged",
        action="store_false",
        help="使用工作区变更"
    )
    gen_parser.add_argument(
        "--history",
        type=int,
        default=5,
        help="参考的历史提交数量"
    )
    gen_parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="生成温度"
    )
    gen_parser.add_argument(
        "--batch",
        type=int,
        default=1,
        help="批量生成数量"
    )
    
    # interactive命令
    subparsers.add_parser("interactive", help="交互式模式")
    
    # serve命令
    serve_parser = subparsers.add_parser("serve", help="启动Web服务器")
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="端口号"
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="主机地址"
    )
    
    # config命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument(
        "--show",
        action="store_true",
        help="显示当前配置"
    )
    config_parser.add_argument(
        "--set",
        nargs=2,
        metavar=("KEY", "VALUE"),
        action="append",
        help="设置配置值"
    )
    config_parser.add_argument(
        "--get",
        help="获取配置值"
    )
    
    # formats命令
    formats_parser = subparsers.add_parser("formats", help="格式管理")
    formats_parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有格式"
    )
    formats_parser.add_argument(
        "--info",
        help="显示格式详细信息"
    )
    
    # validate命令
    validate_parser = subparsers.add_parser("validate", help="验证提交信息")
    validate_parser.add_argument(
        "message",
        nargs="?",
        help="要验证的提交信息"
    )
    validate_parser.add_argument(
        "--format",
        choices=get_formats(),
        default="conventional",
        help="格式类型"
    )
    validate_parser.add_argument(
        "--file",
        help="从文件读取提交信息"
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    
    # 加载配置
    config = Config(args.config)
    
    # 设置颜色输出
    if args.no_color:
        config.set("output.color", False)
    
    # 处理命令
    if args.command == "generate" or args.command is None:
        # 生成模式
        diff = get_git_diff(args.staged, args.file)
        if not diff:
            logger.error("没有找到代码变更")
            sys.exit(1)
        
        history = get_git_history(args.history) if args.history > 0 else None
        
        print("正在生成提交信息...")
        
        results = []
        for i in range(args.batch):
            result = generate_commit_message(
                diff,
                format=args.format,
                history=history,
                temperature=args.temperature,
                config=config.to_dict()
            )
            results.append(result)
        
        for i, result in enumerate(results):
            if args.batch > 1:
                print(f"\n第 {i+1} 个结果:")
            display_result(result, not args.no_color)
    
    elif args.command == "interactive":
        # 交互式模式
        interactive_mode(config)
    
    elif args.command == "serve":
        # Web服务器模式
        serve_mode(config, args.port, args.host)
    
    elif args.command == "config":
        # 配置管理
        if args.show:
            import yaml
            print(yaml.dump(config.to_dict(), default_flow_style=False, allow_unicode=True))
        
        elif args.set:
            for key, value in args.set:
                config.set(key, value)
            config.save()
            print("配置已更新")
        
        elif args.get:
            value = config.get(args.get)
            print(f"{args.get} = {value}")
        
        else:
            # 显示帮助
            parser.parse_args(["config", "--help"])
    
    elif args.command == "formats":
        # 格式管理
        if args.list:
            formats = get_formats()
            print("支持的格式:")
            for fmt in formats:
                print(f"- {fmt}")
        
        elif args.info:
            from .formats import get_format_info
            info = get_format_info(args.info)
            import json
            print(json.dumps(info, indent=2, ensure_ascii=False))
        
        else:
            # 显示帮助
            parser.parse_args(["formats", "--help"])
    
    elif args.command == "validate":
        # 验证模式
        message = args.message
        
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    message = f.read()
            except Exception as e:
                logger.error(f"读取文件失败: {e}")
                sys.exit(1)
        
        if not message:
            # 从stdin读取
            if not sys.stdin.isatty():
                message = sys.stdin.read().strip()
            else:
                logger.error("需要提供提交信息")
                sys.exit(1)
        
        from .formats import validate_message
        is_valid, error = validate_message(message, args.format)
        
        if is_valid:
            print("✓ 格式验证通过")
            sys.exit(0)
        else:
            print(f"✗ 格式验证失败: {error}")
            sys.exit(1)
    
    else:
        # 显示帮助
        parser.print_help()


if __name__ == "__main__":
    main()