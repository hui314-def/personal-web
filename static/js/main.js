// ===== 暗色模式切换 =====
const darkToggle = document.getElementById('darkToggle');
const html = document.documentElement;

// 从 localStorage 读取暗色模式偏好
if (localStorage.getItem('darkMode') === 'true' ||
    (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    html.classList.add('dark');
}

darkToggle?.addEventListener('click', () => {
    html.classList.toggle('dark');
    localStorage.setItem('darkMode', html.classList.contains('dark'));
});

// ===== 移动端菜单 =====
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

mobileMenuBtn?.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

// 点击页面其他位置关闭移动菜单
document.addEventListener('click', (e) => {
    if (!mobileMenu?.contains(e.target) && !mobileMenuBtn?.contains(e.target)) {
        mobileMenu?.classList.add('hidden');
    }
});

// ===== 技能条动画（进入视口时触发） =====
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const bar = entry.target;
            const target = bar.getAttribute('data-width');
            bar.style.width = target + '%';
            observer.unobserve(bar);
        }
    });
}, { threshold: 0.3 });

document.querySelectorAll('.skill-bar').forEach(bar => observer.observe(bar));

// ===== 管理后台：Tab键支持缩进（Markdown编辑区） =====
const editorContent = document.getElementById('editorContent');
editorContent?.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = editorContent.selectionStart;
        const end = editorContent.selectionEnd;
        editorContent.value = editorContent.value.substring(0, start) + '    ' + editorContent.value.substring(end);
        editorContent.selectionStart = editorContent.selectionEnd = start + 4;
    }
});

// ===== 平滑滚动导航高亮 =====
const sections = document.querySelectorAll('[data-section]');
window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const top = section.offsetTop - 100;
        if (window.scrollY >= top) {
            current = section.getAttribute('data-section');
        }
    });
});

// ===== 标签筛选（静态站点动态列表） =====
function filterPosts(tag) {
    document.querySelectorAll('.post-item').forEach(item => {
        if (tag === 'all' || item.getAttribute('data-tags').split(',').includes(tag)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.getAttribute('data-tag') === tag) {
            btn.classList.add('bg-primary-600', 'text-white');
        } else {
            btn.classList.remove('bg-primary-600', 'text-white');
        }
    });
}
