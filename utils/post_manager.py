"""文章管理模块：扫描、解析、创建、分页"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).parent.parent
POSTS_DIR = BASE_DIR / "content" / "posts"
CONFIG_PATH = BASE_DIR / "content" / "config.json"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 YAML-like frontmatter 和正文"""
    fm = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            for line in parts[1].strip().split("\n"):
                line = line.strip()
                if ":" in line:
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key == "tags":
                        value = [t.strip() for t in value.strip("[]").split(",") if t.strip()]
                    fm[key] = value
    return fm, body


def parse_filename_date(filename: str) -> Optional[datetime]:
    """从文件名提取日期，如 2026-06-21-hello-world.md"""
    match = re.match(r"(\d{4}-\d{2}-\d{2})-.+\.md$", filename)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    return None


def scan_posts() -> list[dict]:
    """扫描所有文章，返回按日期倒序的列表"""
    posts = []
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        return posts

    for f in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        slug = f.stem
        # 尝试从文件名提取日期
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", slug)
        if date_match:
            date_str = date_match.group(1)
            slug = date_match.group(2)
        else:
            date_str = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")

        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()

        fm, body = parse_frontmatter(content)
        posts.append({
            "slug": slug,
            "filename": f.name,
            "title": fm.get("title", slug.replace("-", " ").title()),
            "date": fm.get("date", date_str),
            "tags": fm.get("tags", []),
            "summary": fm.get("summary", body[:200].replace("\n", " ")),
            "content": body,
        })

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def get_post(slug: str) -> Optional[dict]:
    """获取单篇文章"""
    posts = scan_posts()
    for p in posts:
        if p["slug"] == slug:
            return p
    return None


def create_post(title: str, content: str, tags: list[str] = None) -> str:
    """创建新文章，返回 slug"""
    slug = title.lower().replace(" ", "-")
    # 移除特殊字符
    slug = re.sub(r"[^a-zA-Z0-9一-鿿\-]", "", slug)
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{slug}.md"
    tags_str = ", ".join(tags) if tags else ""

    frontmatter = f"""---
title: "{title}"
date: "{today}"
tags: [{tags_str}]
summary: "{content[:200].replace(chr(10), ' ')}"
---

{content}
"""

    with open(POSTS_DIR / filename, "w", encoding="utf-8") as f:
        f.write(frontmatter)

    return slug


def get_posts_page(page: int = 1, per_page: int = 10, tag: str = None) -> tuple[list[dict], int]:
    """分页获取文章"""
    all_posts = scan_posts()
    if tag:
        all_posts = [p for p in all_posts if tag in p.get("tags", [])]

    total = len(all_posts)
    start = (page - 1) * per_page
    end = start + per_page
    return all_posts[start:end], total


def get_all_tags() -> list[str]:
    """获取所有标签"""
    posts = scan_posts()
    tags = set()
    for p in posts:
        for t in p.get("tags", []):
            tags.add(t)
    return sorted(tags)
