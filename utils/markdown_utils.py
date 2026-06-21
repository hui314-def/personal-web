"""Markdown 渲染工具"""

import re


def render_markdown(text: str) -> str:
    """简易 Markdown → HTML 渲染（无需额外依赖）"""
    html = text

    # 代码块（```...```）
    def replace_code_block(m):
        code = m.group(1)
        lang = ""
        if "\n" in code and code[0].isalpha():
            first_line_end = code.find("\n")
            first_line = code[:first_line_end]
            if all(c.isalnum() or c in "-#+" for c in first_line):
                lang = first_line
                code = code[first_line_end + 1:]
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lang_class = f' class="language-{lang}"' if lang else ""
        return f'<pre><code{lang_class}>{escaped}</code></pre>'

    html = re.sub(r"```(\w*\n?.*?)```", replace_code_block, html, flags=re.DOTALL)

    # 行内代码
    html = re.sub(r"`([^`]+)`", r'<code class="inline-code">\1</code>', html)

    # 标题
    html = re.sub(r"^#### (.+)$", r"<h4>\1</h4>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", html)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # 链接
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" class="content-link" target="_blank">\1</a>', html)

    # 图片
    html = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" class="content-image">', html)

    # 水平线
    html = re.sub(r"^---$", "<hr>", html, flags=re.MULTILINE)

    # 无序列表
    html = re.sub(r"^- (.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = re.sub(r"(<li>.*</li>\n?)+", r"<ul>\n\g<0></ul>", html)

    # 有序列表
    html = re.sub(r"^\d+\. (.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)

    # 引用块
    html = re.sub(r"^> (.+)$", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE)
    html = re.sub(r"</blockquote>\n<blockquote>", "\n", html)

    # 段落（连续的非空行）
    paragraphs = html.split("\n\n")
    result = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<") and not p.startswith("<code"):
            result.append(p)
        else:
            # 不包裹已经在块级标签中的内容
            if not any(p.startswith(tag) for tag in ["<h", "<ul", "<ol", "<li", "<pre", "<blockquote", "<hr", "<img"]):
                p = f"<p>{p.replace(chr(10), '<br>')}</p>"
            result.append(p)

    return "\n".join(result)
