"""静态站点生成器 - 将 Jinja2 模板渲染为 HTML 输出到 docs/"""

import json
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from jinja2 import Environment, FileSystemLoader

from utils.post_manager import (
    load_config, scan_posts, get_all_tags
)
from utils.markdown_utils import render_markdown

OUTPUT_DIR = BASE_DIR / "docs"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
CONTENT_DATA = BASE_DIR / "content" / "data"

jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def load_json(name: str) -> dict:
    with open(CONTENT_DATA / f"{name}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def render_page(template_name: str, output_path: Path, context: dict):
    """渲染模板并写入 HTML 文件"""
    template = jinja_env.get_template(template_name)
    html = template.render(**context)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] {output_path.relative_to(OUTPUT_DIR)}")


def build():
    print("\n开始构建静态站点...\n")

    # 清空输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    # 复制静态资源
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")
        print("  [OK] 静态资源已复制")

    # 加载数据
    config = load_config()
    profile = load_json("profile")
    skills = load_json("skills")
    projects_data = load_json("projects")
    timeline = load_json("timeline")
    all_posts = scan_posts()
    all_tags = get_all_tags()

    # 基础上下文
    base_ctx = {
        "site_name": config["site_name"],
        "author": config["author"],
        "description": config["description"],
        "base_path": config.get("base_path", ""),
    }

    # 首页
    ctx = {**base_ctx, "current_path": "/", "profile": profile,
           "skills": skills, "latest_posts": all_posts[:5], "all_tags": all_tags}
    render_page("index.html", OUTPUT_DIR / "index.html", ctx)

    # 关于
    ctx = {**base_ctx, "current_path": "/about", "profile": profile,
           "skills": skills, "page": "about"}
    render_page("about.html", OUTPUT_DIR / "about.html", ctx)

    # 项目
    ctx = {**base_ctx, "current_path": "/projects",
           "projects_data": projects_data, "page": "projects"}
    render_page("projects.html", OUTPUT_DIR / "projects.html", ctx)

    # 动态列表（全量）
    ctx = {**base_ctx, "current_path": "/updates",
           "posts": all_posts, "all_tags": all_tags, "page_name": "updates"}
    render_page("updates.html", OUTPUT_DIR / "updates.html", ctx)

    # 每篇文章详情
    posts_dir = OUTPUT_DIR / "updates"
    posts_dir.mkdir(parents=True, exist_ok=True)
    for post in all_posts:
        post["html_content"] = render_markdown(post["content"])
        ctx = {**base_ctx, "current_path": f"/updates/{post['slug']}",
               "post": post, "all_tags": all_tags, "page_name": "updates"}
        render_page("post.html", posts_dir / f"{post['slug']}.html", ctx)

    # 成长时间线
    ctx = {**base_ctx, "current_path": "/growth",
           "timeline": timeline, "page": "growth"}
    render_page("growth.html", OUTPUT_DIR / "growth.html", ctx)

    # 联系
    ctx = {**base_ctx, "current_path": "/contact",
           "profile": profile, "page": "contact"}
    render_page("contact.html", OUTPUT_DIR / "contact.html", ctx)

    # .nojekyll 文件（禁用 GitHub Pages 的 Jekyll 处理）
    (OUTPUT_DIR / ".nojekyll").touch()

    print(f"\n[DONE] 构建完成! 输出目录: {OUTPUT_DIR}")
    print(f"   共 {len(all_posts)} 篇文章\n")
    print("下一步:")
    print("   1. git add docs/")
    print("   2. git commit -m 'Build static site'")
    print("   3. git push")
    print("   4. GitHub Settings -> Pages -> Source: Deploy from branch -> /docs\n")


if __name__ == "__main__":
    build()
