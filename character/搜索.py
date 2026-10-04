import os
import re
from pathlib import Path
from typing import List, Tuple, Optional


def search_in_js_files(directory: str, search_string: str,
                       case_sensitive: bool = True,
                       file_pattern: str = "*.js") -> List[Tuple[str, int, str]]:
    """
    在指定目录的所有JS文件中搜索指定字符串

    Args:
        directory: 要搜索的目录路径
        search_string: 要搜索的字符串
        case_sensitive: 是否区分大小写
        file_pattern: 文件匹配模式，默认为"*.js"

    Returns:
        包含(文件路径, 行号, 行内容)的列表
    """
    results = []
    directory_path = Path(directory)

    if not directory_path.exists():
        print(f"错误: 目录 '{directory}' 不存在")
        return results

    if not directory_path.is_dir():
        print(f"错误: '{directory}' 不是一个目录")
        return results

    # 搜索标志
    flags = 0 if case_sensitive else re.IGNORECASE

    # 遍历目录下的所有JS文件
    for file_path in directory_path.rglob(file_pattern):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    # 使用正则表达式搜索
                    if re.search(re.escape(search_string), line, flags):
                        results.append((str(file_path), line_num, line.strip()))
        except (IOError, PermissionError, UnicodeDecodeError) as e:
            print(f"警告: 无法读取文件 '{file_path}': {e}")
            continue

    return results


def print_results(results: List[Tuple[str, int, str]], search_string: str):
    """格式化打印搜索结果"""
    if not results:
        print(f"未找到包含 '{search_string}' 的JS文件")
        return

    print(f"\n找到 {len(results)} 处包含 '{search_string}' 的位置:")
    print("-" * 80)

    for file_path, line_num, line_content in results:
        print(f"文件: {file_path}")
        print(f"行号: {line_num}")
        print(f"内容: {line_content}")
        print("-" * 80)


def search_with_context(results: List[Tuple[str, int, str]],
                        search_string: str,
                        context_lines: int = 2):
    """显示搜索结果及上下文"""
    if not results:
        print(f"未找到包含 '{search_string}' 的JS文件")
        return

    print(f"\n找到 {len(results)} 处包含 '{search_string}' 的位置 (上下文行数: {context_lines}):")
    print("=" * 80)

    for file_path, line_num, line_content in results:
        print(f"文件: {file_path}")
        print(f"行号: {line_num}")
        print(f"匹配行: {line_content}")

        # 显示上下文
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                start = max(0, line_num - context_lines - 1)
                end = min(len(lines), line_num + context_lines)

                print("上下文:")
                for i in range(start, end):
                    prefix = ">>> " if i == line_num - 1 else "    "
                    print(f"{prefix}{i + 1:4d}: {lines[i].rstrip()}")
        except:
            pass

        print("=" * 80)


def main():
    """主函数 - 交互式搜索"""
    print("JS文件内容搜索工具")
    print("=" * 50)

    # 获取用户输入
    directory = input("请输入要搜索的目录路径: ").strip()
    if not directory:
        directory = "."  # 默认为当前目录

    search_string = input("请输入要搜索的字符串: ").strip()
    if not search_string:
        print("错误: 搜索字符串不能为空")
        return

    # 选择搜索模式
    print("\n搜索选项:")
    print("1. 简单搜索 (仅显示匹配行)")
    print("2. 上下文搜索 (显示匹配行及其上下文)")
    choice = input("请选择搜索模式 (1/2): ").strip()

    case_sensitive = input("是否区分大小写? (y/n, 默认y): ").strip().lower() != 'n'

    # 执行搜索
    results = search_in_js_files(directory, search_string, case_sensitive)

    # 显示结果
    if choice == '2':
        try:
            context_lines = int(input("请输入上下文行数 (默认2): ").strip() or "2")
        except ValueError:
            context_lines = 2
        search_with_context(results, search_string, context_lines)
    else:
        print_results(results, search_string)


def search_js_files(directory: str, search_string: str,
                    case_sensitive: bool = True,
                    context: int = 0) -> None:
    """
    命令行调用接口

    Args:
        directory: 要搜索的目录
        search_string: 搜索字符串
        case_sensitive: 是否区分大小写
        context: 上下文行数，0表示只显示匹配行
    """
    results = search_in_js_files(directory, search_string, case_sensitive)

    if context > 0:
        search_with_context(results, search_string, context)
    else:
        print_results(results, search_string)


# 使用示例
if __name__ == "__main__":
    # 交互式使用
    main()

    # 或者直接调用函数（取消注释下面的代码）
    # search_js_files("./", "console.log", context=2)