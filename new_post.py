#!/usr/bin/env python3
"""CLI 工具：快速发布新文章"""

import sys
from pathlib import Path

# 添加项目根目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from utils.post_manager import create_post, get_all_tags


def main():
    print("\n📝 发布新文章\n" + "=" * 40)

    # 标题
    title = input("文章标题: ").strip()
    if not title:
        print("❌ 标题不能为空")
        return

    # 标签
    existing = get_all_tags()
    if existing:
        print(f"\n已有标签: {', '.join(existing)}")
    tags_input = input("标签（逗号分隔）: ").strip()
    tag_list = [t.strip() for t in tags_input.split(",") if t.strip()]

    # 内容
    print("\n请输入 Markdown 内容（输入 END 结束）：")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    content = "\n".join(lines)

    if not content.strip():
        print("❌ 内容不能为空")
        return

    # 确认
    print(f"\n{'='*40}")
    print(f"标题: {title}")
    print(f"标签: {', '.join(tag_list) if tag_list else '(无)'}")
    print(f"内容预览: {content[:100]}...")
    print(f"{'='*40}")

    confirm = input("\n确认发布？[Y/n]: ").strip().lower()
    if confirm and confirm != "y":
        print("已取消")
        return

    slug = create_post(title, content, tag_list)
    print(f"\n✅ 文章已发布！")
    print(f"   访问: http://localhost:8000/updates/{slug}")


if __name__ == "__main__":
    main()
