# 陈俊辉 | 个人成长站

基于 **FastAPI + Jinja2 + Tailwind CSS** 的个人成长网站，支持动态发布博客文章，可部署到 GitHub Pages。

## ✨ 功能

- 🏠 **首页** - Hero区域 + 个人简介 + 最新动态
- 👤 **关于** - 详细信息、技能进度条、教育背景、兴趣爱好
- 💻 **项目** - 精选项目、工具项目、ML项目展示
- 📰 **动态** - Markdown博客系统，标签筛选
- 🌱 **成长** - 过去→现在→未来成长时间线
- 📬 **联系** - 联系方式卡片，一键复制
- 🔐 **管理后台** - 密码保护，Web表单发布文章
- 🌙 **暗色模式** - 支持亮/暗主题切换

## 🚀 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动网站

```bash
python main.py
```

浏览器打开 **http://localhost:8000**

### 3. 发布新文章

**方式一：Web管理后台（推荐）**
1. 访问 http://localhost:8000/admin
2. 输入用户名 `admin`，密码 `admin123`
3. 填写标题和Markdown内容，点击发布

**方式二：命令行**
```bash
python new_post.py
```

## 🌐 部署到 GitHub Pages

### 一键部署流程

```bash
# 1. 本地写完文章后，生成静态文件
python build.py

# 2. 提交并推送
git add docs/
git commit -m "Update site"
git push
```

### GitHub 仓库设置

1. 打开仓库 → **Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: `main`（或 `uat`）
4. **Folder**: `/docs`
5. 保存，等待部署完成

### 配置 base_path

编辑 `content/config.json`：

| 仓库类型 | base_path 配置 |
|----------|---------------|
| 用户站点 (`hui314-def.github.io`) | `"base_path": ""` |
| 项目站点 (其他仓库) | `"base_path": "/仓库名"` |

例如仓库叫 `personal-website`，则设置 `"base_path": "/personal-website"`

## 📁 项目结构

```
personal-website/
├── main.py              # FastAPI 入口（本地开发）
├── build.py             # 静态站点生成器
├── new_post.py           # CLI 发布工具
├── requirements.txt      # Python 依赖
├── static/               # 静态资源 (CSS/JS/图片)
├── templates/            # Jinja2 页面模板
├── content/
│   ├── posts/            # Markdown 文章
│   ├── data/             # JSON 数据文件
│   └── config.json       # 站点配置
├── docs/                 # 生成的静态站点（用于GitHub Pages）
└── utils/                # 工具模块
```

## ⚙️ 配置

编辑 `content/config.json` 修改站点配置：

```json
{
    "site_name": "陈俊辉 | 个人成长站",
    "admin_password": "你的密码",
    "posts_per_page": 10,
    "base_path": ""
}
```

## 📝 文章格式

文章使用 Markdown + YAML frontmatter：

```markdown
---
title: "文章标题"
date: "2026-06-21"
tags: [标签1, 标签2]
summary: "文章摘要"
---

## 内容标题

Markdown 正文内容...
```

## 👨‍💻 作者

陈俊辉 - 广州大学 人工智能专业 2024级

- GitHub: [@hui314-def](https://github.com/hui314-def)
- 邮箱: 2083180893@qq.com
