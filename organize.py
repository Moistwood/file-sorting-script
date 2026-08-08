"""
文件分类整理器
把文件夹里乱七八糟的文件按类型自动归类
用法: python organize.py <文件夹路径>
"""

import os
import shutil
import json
import argparse

# 默认分类规则 
rules = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".heic"],
    "文档": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".epub"],
    "视频": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"],
    "音频": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso"],
    "代码": [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yaml", ".java", ".cpp", ".go", ".rs"],
    "字体": [".ttf", ".otf", ".woff", ".woff2"],
    "安装包": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".apk"],
}


def load_rules(rules_file):
    #如果用户给了自定义规则文件则运行，否则用默认的#
    if rules_file is None:
        return rules

    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            custom = json.load(f)
        print(f"已加载自定义规则: {rules_file}")
        return custom
    except FileNotFoundError:
        print(f"规则文件没找到: {rules_file}，用默认规则")
        return rules
    except json.JSONDecodeError:
        print(f"规则文件格式有问题，用默认规则")
        return rules


def get_category(filename, rules_dict):
    #根据文件名判断分类#
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    for category, exts in rules_dict.items():
        if ext in exts:
            return category

    return "其他"


def handle_duplicate(folder, filename):
    #处理重名文件#
    target = os.path.join(folder, filename)

    if not os.path.exists(target):
        return filename

    name, ext = os.path.splitext(filename)
    num = 1
    while os.path.exists(os.path.join(folder, f"{name}_{num}{ext}")):
        num += 1

    return f"{name}_{num}{ext}"


def organize(folder, rules_dict, dry_run=False):
    #核心逻辑：遍历文件、分类、移动#
    if not os.path.exists(folder):
        print(f"文件夹不存在: {folder}")
        return
    if not os.path.isdir(folder):
        print(f"这不是个文件夹: {folder}")
        return

    items = os.listdir(folder)
    files = [f for f in items if os.path.isfile(os.path.join(folder, f))]

    if not files:
        print("文件夹里没有文件")
        return

    print(f"{'[预览模式] ' if dry_run else ''}共找到 {len(files)} 个文件\n")

    moved = 0
    skipped = 0
    failed = 0

    for filename in files:
        category = get_category(filename, rules_dict)
        dest_folder = os.path.join(folder, category)

        # 已经在目标文件夹里的就跳过#
        src_path = os.path.join(folder, filename)
        if os.path.dirname(src_path) == dest_folder:
            skipped += 1
            continue

        # 处理重名#
        final_name = handle_duplicate(dest_folder, filename)
        dest_path = os.path.join(dest_folder, final_name)

        # 移动
        try:
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(src_path, dest_path)
            tag = f" -> 重命名为 {final_name}" if final_name != filename else ""
            print(f"  已移动: {filename} -> {category}/{final_name}{tag}")
            moved += 1
        except Exception as e:
            print(f"  失败: {filename} - {e}")
            failed += 1

    print(f"\n结果: 移动 {moved} 个, 跳过 {skipped} 个, 失败 {failed} 个")

    if dry_run:
        print("这是预览模式，去掉 --dry-run 才会真的移动文件")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="把文件按类型自动分类到不同文件夹")
    parser.add_argument("folder", nargs="?", default=".", help="要整理的文件夹路径，默认当前目录")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，只显示会怎么移动但不真的动")
    parser.add_argument("--rules", help="自定义规则文件（JSON 格式）")

    args = parser.parse_args()

    my_rules = load_rules(args.rules)

    print("当前规则:")
    for cat, exts in my_rules.items():
        print(f"  {cat}: {len(exts)} 种后缀")
    print()

    organize(args.folder, my_rules, args.dry_run)
