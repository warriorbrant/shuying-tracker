# Site-wide UI string translations, used via the `tr()` Jinja global (see
# app.py). Keyed by the original Chinese text itself rather than an invented
# key name — `tr("添加")` returns "Add" when the visitor's language is English,
# and just returns "添加" unchanged for everything else (Chinese visitors, or
# any string that hasn't been added here yet). This is deliberately separate
# from CHANGELOG_STRINGS (app.py), which is an older, page-scoped dict used
# only by the changelog/public-home pages — that one is left as-is.
#
# Only user-facing UI chrome belongs here: nav, buttons, form labels, hints,
# empty states, headings. User-generated content (book notes, novel chapters,
# moments) is never machine-translated — it stays exactly as written.

TR = {
    # --- base.html / nav (shown on every page) ---
    "📚🎬 知行合一AI实验室": "📚🎬 Unity of Knowledge & Action AI Lab",
    "知行合一AI实验室": "Unity of Knowledge & Action AI Lab",
    "+ 添加": "+ Add",
    "+ 截图导入": "+ Import Screenshot",
    "🔍 搜索": "🔍 Search",
    "📊 性能指标": "📊 Metrics",
    "🛡️ 账号管理": "🛡️ Accounts",
    "📖 小说": "📖 Novels",
    "更新日志": "Changelog",
    "退出登录": "Log out",
    "登录": "Log in",

    # --- login.html / register.html / reset_password.html ---
    "登录 · 知行合一AI实验室": "Log In · Unity of Knowledge & Action AI Lab",
    "注册 · 知行合一AI实验室": "Register · Unity of Knowledge & Action AI Lab",
    "重置密码 · 知行合一AI实验室": "Reset Password · Unity of Knowledge & Action AI Lab",
    "用户名": "Username",
    "密码": "Password",
    "新密码": "New password",
    "设置新密码": "Set new password",
    "注册": "Register",
    "还没有账号？去注册 →": "No account yet? Register →",
    "已经有账号？去登录 →": "Already have an account? Log in →",
    "← 返回公开主页": "← Back to public home",
    "← 返回登录": "← Back to login",
    "→ 去登录": "→ Log in",
    "密码重置好了。": "Password reset.",
    "这个重置链接无效或者已经用过/过期了，找管理员再要一个新的。":
        "This reset link is invalid, already used, or expired — ask an admin for a new one.",
    "用户名或密码不对，再试一次": "Wrong username or password, try again",
    "用户名和密码都要填": "Username and password are both required",
    "密码至少要 6 位": "Password must be at least 6 characters",
    "这个用户名已经有人用了": "That username is already taken",
    "账号不存在": "Account not found",

    # --- public_home.html ---
    "这是我用 AI 从零搭建的个人 AI 应用实验室，书影/生活追踪只是目前跑在里面的第一个功能。完整内容登录后才能看到，这里是公开的开发更新日志。":
        "A personal AI-app lab I built from scratch with AI. Book/show tracking is just the first "
        "feature running in it so far. Full content needs a login — this is the public dev changelog.",
    "这个网站是怎么做出来的": "How this site gets built",
    "🤖 AI 开发模式（这个网站的实际流程）": "🤖 AI development mode (how this site actually works)",
    "跟 Claude<br>对话提需求": "Chat with Claude<br>about what to build",
    "Claude Code<br>写代码": "Claude Code<br>writes the code",
    "推送到<br>GitHub": "Push to<br>GitHub",
    "Railway<br>自动部署": "Railway<br>auto-deploys",
    "网站更新<br>上线": "Update<br>goes live",
    "⏱ 一个想法到上线：几分钟到几小时": "⏱ Idea to live: minutes to hours",
    "🧑‍💻 传统开发模式（对比）": "🧑‍💻 Traditional dev mode (for comparison)",
    "写需求<br>文档": "Write a spec<br>doc",
    "工程师<br>手写代码": "Engineer<br>hand-writes code",
    "写测试<br>跑测试": "Write tests<br>run tests",
    "Code<br>Review": "Code<br>Review",
    "CI/CD<br>自动部署": "CI/CD<br>auto-deploy",
    "上线": "Ship",
    "⏱ 同样一个想法到上线：通常数天到数周": "⏱ Same idea to live: usually days to weeks",
    "全程不用手写一行代码，我只负责提需求和验收；每次改动的细节都记录在下面的更新日志里。":
        "Not a single line hand-written by me — I just describe what I want and review the result; "
        "every change is logged in detail below.",
    "源代码在 GitHub →": "Source on GitHub →",
    "网站的技术架构": "Technical architecture",
    "网站技术架构图": "Site architecture diagram",
    "🖥️📱 浏览器 / 手机 PWA": "🖥️📱 Browser / mobile PWA",
    "🌍 Railway 边缘 CDN": "🌍 Railway edge CDN",
    "全球多节点，图片/静态资源边缘缓存": "Global edge nodes, caches images/static assets",
    "未命中 / 动态请求 → 转发源站": "Cache miss / dynamic request → forwarded to origin",
    "🐳 源站容器 · Railway（新加坡）": "🐳 Origin container · Railway (Singapore)",
    "gunicorn：1 进程 + 4 线程，共享内存态数据": "gunicorn: 1 process + 4 threads, shared in-memory state",
    "⚙️ Flask 应用（app.py）": "⚙️ Flask app (app.py)",
    "🔐 路由 + 登录鉴权": "🔐 Routing + login auth",
    "🧩 Jinja2 服务端渲染": "🧩 Jinja2 server-side rendering",
    "🖼️ Pillow 图片 / ffmpeg 视频处理": "🖼️ Pillow images / ffmpeg video processing",
    "🗜️ Gzip / Brotli 压缩": "🗜️ Gzip / Brotli compression",
    "📊 请求耗时统计": "📊 Request latency stats",
    "💾 持久化存储": "💾 Persistent storage",
    "• tracker.db（书影 / 动态 / 小说 数据）": "• tracker.db (book/show, moments, novel data)",
    "• uploads/（动态上传的照片）": "• uploads/ (photos uploaded in moments)",
    "• novel_media/（小说封面 / 立绘 / 视频）": "• novel_media/ (novel covers / character art / videos)",
    "• cover_cache/（豆瓣封面缓存）": "• cover_cache/ (Douban cover cache)",
    "🔌 外部服务": "🔌 External services",
    "运行时对外请求": "Outbound requests at runtime",
    "• 豆瓣网页抓取 + 封面代理": "• Douban page scraping + cover proxy",
    "• Claude API（AI 截图识别，可选）": "• Claude API (AI screenshot recognition, optional)",
    "服务端是一个 Flask + SQLite 的单体应用，没有独立前端构建，页面都是服务端用 Jinja2 直接渲染出来的；"
    "用 gunicorn（1 进程 4 线程）跑在 Railway 新加坡区域的一个 Docker 容器里。图片用 Pillow 处理（生成分享图、"
    "压缩上传图片），视频用 ffmpeg 压缩并抽封面帧。数据库、用户照片、小说封面/立绘/视频、豆瓣封面缓存都存在 "
    "Railway 的持久化 Volume 里，图片和静态资源通过边缘 CDN 缓存；豆瓣书影信息靠抓取网页拿到，AI 截图识别接的"
    "是 Anthropic 的 Claude API。":
        "The backend is a Flask + SQLite monolith with no separate frontend build — pages are "
        "server-rendered directly with Jinja2, run with gunicorn (1 process, 4 threads) in a Docker "
        "container in Railway's Singapore region. Images go through Pillow (share cards, upload "
        "compression), video through ffmpeg (compression, thumbnail extraction). The database, user "
        "photos, novel covers/character art/videos, and the Douban cover cache all live on a Railway "
        "persistent volume; images and static assets are cached at the CDN edge. Douban book/show info "
        "comes from scraping their pages; AI screenshot recognition calls Anthropic's Claude API.",
    "加载中…": "Loading…",

    # --- fixed enums (item/novel status, moment types) ---
    "想看": "Want to",
    "进行中": "In progress",
    "已完成": "Done",
    "放弃": "Dropped",
    "连载中": "Ongoing",
    "已完结": "Completed",
    "暂停": "Paused",
    "股票": "Stock",
    "运动": "Exercise",
    "照片": "Photo",
    "想法": "Thought",
    "网站更新": "Site update",

    # --- novels_list.html / novel_detail.html / novel_chapter.html (public) ---
    "小说": "Novels",
    "+ 新建小说": "+ New Novel",
    "不需要登录也能看，角色概念图和 AI 生成的相关视频都放在小说详情页里。":
        "No login needed to read — character art and AI-generated videos are on each novel's detail page.",
    "还没有小说，": "No novels yet, ",
    "写第一篇": "write the first one",
    "敬请期待": "stay tuned",
    "。": ".",
    "共 ": "",
    " 字 · 更新于 ": " words · updated ",

    "🔒 已锁定": "🔒 Locked",
    "共 {n} 字": "{n} words",
    "最后更新 {d}": "Last updated {d}",
    "📤 一键生成分享图": "📤 Generate share image",
    "先预览": "Preview first",
    "编辑小说": "Edit novel",
    "导出 Word": "Export Word",
    "导出 PDF": "Export PDF",
    "目录（共 {n} 章）": "Contents ({n} chapters)",
    "未分卷": "Unassigned",
    "还没有章节。": "No chapters yet.",
    "人物角色": "Characters",
    "相关视频": "Videos",
    "在新窗口打开视频 →": "Open video in new tab →",
    "参考书目": "References",
    "第 {n} 卷 · {title}": "Volume {n} · {title}",
    "第 {n} 章 · {title}": "Chapter {n} · {title}",
    "{n} 字 · {d}": "{n} words · {d}",

    # --- novel_chapter.html (public read view) ---
    "目录": "Contents",
    "📤 生成本章分享图": "📤 Generate share image",
    "▶ 朗读本章": "▶ Read aloud",
    "⏹ 停止": "⏹ Stop",
    "语速": "Speed",
    "自动连播下一章": "Auto-play next chapter",
    "🔒 本章已锁定，登录后可查看完整正文": "🔒 This chapter is locked — log in to read the full text",
    "登录查看完整内容": "Log in to see the full content",
    "本章视频": "Videos in this chapter",
    "← 上一章": "← Previous chapter",
    "下一章 →": "Next chapter →",
    "编辑这一章": "Edit this chapter",
    "▶ 继续": "▶ Resume",
    "⏸ 暂停": "⏸ Pause",

    # --- index.html / _feed_items.html / _log_items.html ---
    "{d}：{m} 分钟": "{d}: {m} min",
    "过去一年打卡 {d} 天，累计用时 {h} 小时": "{d} active days in the past year, {h} hours total",
    "查看今天 →": "View today →",
    "动态": "Moments",
    "全部": "All",
    "📚 书": "📚 Books",
    "🎬 剧": "🎬 Shows",
    "全部状态": "All statuses",
    "还没有记录，点右上角「添加书」「添加剧」「记录动态」开始吧。":
        "Nothing yet — tap “Add” in the top right to add a book, a show, or log a moment.",
    "用时 {m} 分钟": "{m} min spent",
    "书": "Book",
    "剧": "Show",
    "进度：{p} {u}": "Progress: {p} {u}",
    "加入了待看清单（{s}），还没有进度记录": "Added to the list ({s}), no progress logged yet",

    # --- _log_items.html ---
    "⏱ {m} 分钟": "⏱ {m} min",
    "删除这条记录？": "Delete this entry?",
    "删除": "Delete",

    # --- item_detail.html ---
    "{p} / {t} {u}（{pct}%）": "{p} / {t} {u} ({pct}%)",
    "⏱ 总用时 {m} 分钟": "⏱ {m} min total",
    "📝 {n} 条记录": "📝 {n} entries",
    "总评 / 感想": "Overall review",
    "编辑条目": "Edit",
    "📤 一键生成分享图": "📤 Generate share image",
    "先预览": "Preview first",
    "确定删除《{title}》及其所有记录吗？此操作不可撤销。": "Delete “{title}” and all its logs? This can't be undone.",
    "删除条目": "Delete",
    "生成的图片可直接上传到小红书发笔记（小红书暂不支持网页一键跳转发布）。":
        "The generated image can be uploaded directly to Xiaohongshu (no one-click web publish yet).",
    "添加今日进度": "Log today's progress",
    "日期": "Date",
    "用时（分钟）": "Time spent (min)",
    "进度到第几{u}": "Progress ({u})",
    "页": "page",
    "备注 / 感想": "Notes",
    "今天读到/看到哪里，有什么想法…": "Where you got to today, any thoughts…",
    "保存记录": "Save",
    "历史记录": "History",
    "还没有记录。": "No entries yet.",

    # --- add_form.html ---
    "添加": "Add",
    "类型": "Type",
    "书影": "Books & shows",
    "从豆瓣链接自动填充（豆瓣读书 / 豆瓣电影·剧集）": "Auto-fill from a Douban link (Douban Books / Movies·Shows)",
    "粘贴豆瓣页面链接，例如 https://book.douban.com/subject/xxxxx/":
        "Paste a Douban page link, e.g. https://book.douban.com/subject/xxxxx/",
    "自动填充": "Auto-fill",
    "标题": "Title",
    "作者 / 导演·出品方": "Author / Director·Studio",
    "封面图片链接（可选）": "Cover image URL (optional)",
    "豆瓣链接（可选，用自动填充会自动带上）": "Douban link (optional, filled in automatically by auto-fill)",
    "总量（总页数 / 总集数）": "Total (pages / episodes)",
    "单位": "Unit",
    "页 / 集": "page / ep",
    "状态": "Status",
    "评分（1-5，可选）": "Rating (1-5, optional)",
    "保存": "Save",
    "取消": "Cancel",
    "标题（可选，如股票代码、运动类型）": "Title (optional — stock ticker, workout type, etc.)",
    "例如：贵州茅台 / 跑步 / 今日随笔": "e.g. AAPL / Running / Today's thoughts",
    "内容 / 评论": "Content",
    "写点什么：涨跌情况、时长距离、拍到了什么、当下的想法…":
        "Write something: price moves, time/distance, what you photographed, what's on your mind…",
    "用时（分钟，可选）": "Time spent (min, optional)",
    "配图（可选）": "Photo (optional)",
    "请先粘贴豆瓣链接": "Paste a Douban link first",
    "正在抓取…": "Fetching…",
    "抓取失败，请手动填写": "Fetch failed, please fill in manually",
    "已自动填充，请检查并按需修改后保存": "Auto-filled — check it over and adjust before saving",
    "抓取失败，请检查网络或手动填写": "Fetch failed — check your connection or fill in manually",

    # --- item_form.html ---
    "编辑": "Edit",
    "编辑条目": "Edit Entry",
    "添加新条目": "Add New Entry",

    # --- moment_form.html ---
    "记录动态": "Log a Moment",
    "记录今天的动态": "Log Today's Moment",

    # --- day.html ---
    "← 前一天": "← Previous day",
    "后一天 →": "Next day →",
    "今天": "Today",
    "📌 {n} 项记录": "📌 {n} entries",
    "⏱ 共 {m} 分钟": "⏱ {m} min total",
    "📤 一键生成今日分享图": "📤 Generate share image",
    "+ 记录今天的动态": "+ Log a moment",
    "📚🎬 书影进度": "📚🎬 Book/show progress",
    "新添加 · {s}": "New · {s}",
    "📝 今日动态": "📝 Today's moments",
    "这一天还没有添加动态。": "No moments logged this day yet.",
    "删除这条动态？": "Delete this moment?",

    # --- search.html ---
    "搜索": "Search",
    "搜书名、作者、评论、想法…": "Search titles, authors, reviews, thoughts…",
    "输入点什么开始搜索：书名、作者、每日感想、动态内容都能搜到。":
        "Type something to search — titles, authors, daily notes, and moments are all searchable.",
    "没有找到匹配「{q}」的内容。": "Nothing matches “{q}”.",
}
