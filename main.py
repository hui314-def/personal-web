"""个人成长网站 - FastAPI 主应用"""

import json
import sys
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jinja2 import Environment, FileSystemLoader
import secrets

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.post_manager import (
    load_config, scan_posts, get_post, create_post,
    get_posts_page, get_all_tags
)
from utils.markdown_utils import render_markdown
app = FastAPI(title="陈俊辉 | 个人成长站")

# 静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 模板 - 直接使用 Jinja2 避免 Starlette 封装版本的兼容性问题
jinja_env = Environment(loader=FileSystemLoader(BASE_DIR / "templates"), autoescape=True)


def render_template(name: str, context: dict) -> HTMLResponse:
    """使用 Jinja2 直接渲染模板"""
    template = jinja_env.get_template(name)
    content = template.render(**context)
    return HTMLResponse(content=content)

# HTTP Basic Auth
security = HTTPBasic()


def load_json(name: str) -> dict:
    path = BASE_DIR / "content" / "data" / f"{name}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_admin(credentials: HTTPBasicCredentials = Depends(security)):
    config = load_config()
    correct = config.get("admin_password", "admin123")
    is_ok = secrets.compare_digest(credentials.username, "admin") and \
            secrets.compare_digest(credentials.password, correct)
    if not is_ok:
        raise HTTPException(status_code=401, detail="Unauthorized",
                            headers={"WWW-Authenticate": "Basic"})
    return True


def get_global_context(request: Request) -> dict:
    config = load_config()
    return {
        "request": request,
        "site_name": config["site_name"],
        "author": config["author"],
        "description": config["description"],
        "current_path": request.url.path,
        "base_path": config.get("base_path", ""),
    }


# ==================== 页面路由 ====================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    profile = load_json("profile")
    skills = load_json("skills")
    posts, _ = get_posts_page(page=1, per_page=5)
    all_tags = get_all_tags()
    ctx = get_global_context(request)
    ctx.update({"profile": profile, "skills": skills, "latest_posts": posts, "all_tags": all_tags})
    return render_template("index.html", ctx)


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    profile = load_json("profile")
    skills = load_json("skills")
    ctx = get_global_context(request)
    ctx.update({"profile": profile, "skills": skills, "page": "about"})
    return render_template("about.html", ctx)


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    projects_data = load_json("projects")
    ctx = get_global_context(request)
    ctx.update({"projects_data": projects_data, "page": "projects"})
    return render_template("projects.html", ctx)


@app.get("/updates", response_class=HTMLResponse)
async def updates(request: Request, page: int = 1, tag: str = None):
    config = load_config()
    per_page = config.get("posts_per_page", 10)
    posts, total = get_posts_page(page=page, per_page=per_page, tag=tag)
    total_pages = max(1, (total + per_page - 1) // per_page)
    all_tags = get_all_tags()
    ctx = get_global_context(request)
    ctx.update({
        "posts": posts, "page_num": page, "total_pages": total_pages,
        "total": total, "current_tag": tag, "all_tags": all_tags, "page_name": "updates"
    })
    return render_template("updates.html", ctx)


@app.get("/updates/{slug}", response_class=HTMLResponse)
async def post_detail(request: Request, slug: str):
    post = get_post(slug)
    if not post:
        raise HTTPException(status_code=404, detail="文章未找到")
    post["html_content"] = render_markdown(post["content"])
    all_tags = get_all_tags()
    ctx = get_global_context(request)
    ctx.update({"post": post, "all_tags": all_tags, "page_name": "updates"})
    return render_template("post.html", ctx)


@app.get("/growth", response_class=HTMLResponse)
async def growth(request: Request):
    timeline = load_json("timeline")
    ctx = get_global_context(request)
    ctx.update({"timeline": timeline, "page": "growth"})
    return render_template("growth.html", ctx)


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    profile = load_json("profile")
    ctx = get_global_context(request)
    ctx.update({"profile": profile, "page": "contact"})
    return render_template("contact.html", ctx)


# ==================== 管理后台 ====================

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, _: bool = Depends(check_admin)):
    all_tags = get_all_tags()
    ctx = get_global_context(request)
    ctx.update({"all_tags": all_tags, "page": "admin"})
    return render_template("admin.html", ctx)


@app.post("/admin/publish", response_class=HTMLResponse)
async def admin_publish(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(""),
    _: bool = Depends(check_admin),
):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    slug = create_post(title, content, tag_list)
    return RedirectResponse(url=f"/updates/{slug}", status_code=303)


# ==================== 启动入口 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
