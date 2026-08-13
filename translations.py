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
    "🧭 知行合一AI实验室": "🧭 Unity of Knowledge & Action AI Lab",
    "知行合一AI实验室": "Unity of Knowledge & Action AI Lab",
    "+ 添加": "+ Add",
    "+ 截图导入": "+ Import Screenshot",
    "🔍 搜索": "🔍 Search",
    "📊 性能指标": "📊 Metrics",
    "🛡️ 账号管理": "🛡️ Accounts",
    "📖 小说": "📖 Novels",
    "📈 交易": "📈 Trading",
    "💰 消费": "💰 Spending",
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
    "这是我用 AI 从零搭建的个人 AI 应用实验室，探索AI应用的边界。完整内容登录后才能看到，这里是公开的开发更新日志。":
        "A personal AI-app lab I built from scratch with AI, exploring the boundaries of what AI "
        "applications can do. Full content needs a login — this is the public dev changelog.",
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
    "📤 生成分享图": "📤 Generate share image",
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

    # --- novel_form.html ---
    "编辑小说": "Edit Novel",
    "新建小说": "New Novel",
    "书名": "Title",
    "简介": "Summary",
    "封面图片（可选）": "Cover image (optional)",
    "🔒 锁定整本小说（未登录访客所有章节都看不了）": "🔒 Lock the whole novel (no chapter visible to logged-out visitors)",
    "查看小说页": "View novel page",
    "确定删除《{title}》及其所有章节、人物、视频吗？此操作不可撤销。":
        "Delete “{title}” and all its chapters, characters, and videos? This can't be undone.",
    "删除小说": "Delete novel",
    "分卷（共 {n} 卷）": "Volumes ({n})",
    "确定删除《{title}》这一卷吗？卷里的章节不会被删除，只是变成未分卷。":
        "Delete the volume “{title}”? Its chapters won't be deleted, just unassigned.",
    "新的一卷叫什么，例如「第一卷 风起」": "Name the new volume, e.g. “Volume 1: Winds Rise”",
    "新增卷": "New Volume",
    "章节（共 {n} 章 · 共 {w} 字）": "Chapters ({n} · {w} words)",
    "+ 新增章节": "+ New Chapter",
    "确定删除这一章吗？": "Delete this chapter?",
    "🔒 锁定选中章节": "🔒 Lock selected",
    "🔓 解锁选中章节": "🔓 Unlock selected",
    "移到未分卷": "Move to unassigned",
    "移到 第 {n} 卷 · {title}": "Move to Volume {n} · {title}",
    "批量移卷": "Move",
    "勾选章节前面的框，再点上面的按钮批量锁定/解锁，或者选一卷批量移过去。":
        "Check the boxes next to chapters, then use the buttons above to lock/unlock in bulk, or pick a volume to move them into.",
    "替换 / 编辑": "Replace / Edit",
    "确定删除这个角色吗？": "Delete this character?",
    "角色名": "Character name",
    "概念图（可选，AI 生成或自己画的都行）": "Concept art (optional — AI-generated or hand-drawn, either works)",
    "角色简介（可选）": "Description (optional)",
    "添加角色": "Add Character",
    "时长约 {s} 秒": "~{s}s",
    "确定删除这个视频吗？": "Delete this video?",
    "视频标题（可选）": "Video title (optional)",
    "来源": "Source",
    "上传文件（最长 5 分钟，会自动压缩）": "Upload a file (up to 5 min, auto-compressed)",
    "粘贴链接（B站 / YouTube）": "Paste a link (Bilibili / YouTube)",
    "视频文件": "Video file",
    "视频链接": "Video link",
    "https://www.bilibili.com/video/BV... 或 https://youtu.be/...":
        "https://www.bilibili.com/video/BV... or https://youtu.be/...",
    "添加视频": "Add Video",
    "「在分享图中显示」勾选的会出现在小说分享图里，建议选 5-10 本；已选 {n} 本":
        "Checking “show in share image” includes it in the novel's share card — 5-10 is a good range; {n} selected so far",
    "（超过 10 本时分享图只取前 10 本）": " (only the first 10 are used if you pick more than 10)",
    "豆瓣 →": "Douban →",
    "在分享图中显示": "Show in share image",
    "确定从参考书目移除吗？（不会删除这本书本身）": "Remove from references? (the book itself won't be deleted)",
    "移除": "Remove",
    "搜索书名添加（从已经添加过的书里找）": "Search to add (from books you've already added)",
    "输入书名或作者…": "Type a title or author…",
    "没有想要的书？": "Don't see the book you want? ",
    "先去添加一本 →": "Add one first →",
    "（添加完回到这里搜索）": " (then come back and search here)",
    "没有匹配的书（可能已经加过了）": "No matching books (may already be added)",

    # --- novel_chapter_form.html ---
    "编辑章节": "Edit Chapter",
    "新增章节": "New Chapter",
    "章节标题": "Chapter title",
    "正文": "Content",
    "所属卷（可选）": "Volume (optional)",
    "不属于任何卷": "No volume",
    "🔒 锁定本章（未登录访客看不了这一章）": "🔒 Lock this chapter (not visible to logged-out visitors)",
    "本章出场人物（搜索添加）": "Characters in this chapter (search to add)",
    "移除": "Remove",
    "输入人物名，或点一下看全部…": "Type a character name, or click to see all…",
    "本章视频（搜索添加）": "Videos in this chapter (search to add)",
    "视频 #{n}": "Video #{n}",
    "输入视频标题，或点一下看全部…": "Type a video title, or click to see all…",
    "没有可添加的了": "Nothing left to add",

    # --- novel_character_form.html ---
    "编辑角色": "Edit Character",
    "替换图片或改名后，所有已经关联这个角色的章节会自动同步显示最新的样子，不用逐章重新设置。":
        "Replace the image or rename it and every chapter already linked to this character updates automatically — no need to redo it chapter by chapter.",
    "替换概念图（可选，留空保持原图）": "Replace concept art (optional, leave blank to keep the current one)",

    # --- admin_users.html ---
    "账号管理": "Accounts",
    "给 {u} 的一次性重置链接（24 小时内有效，用一次就失效），复制发给对方：":
        "One-time reset link for {u} (valid 24h, single use) — copy it and send it to them:",
    "已有账号（共 {n} 个）": "Accounts ({n})",
    "· 🛡️ 管理员": " · 🛡️ Admin",
    "· {d} 创建": " · created {d}",
    "新密码（至少6位）": "New password (min 6 chars)",
    "直接重置": "Reset directly",
    "生成重置链接": "Generate reset link",
    "新增账号": "Add Account",
    "用户名": "Username",
    "密码": "Password",
    "设为管理员（能管理账号、绕过所有人的锁定内容）": "Make admin (can manage accounts, bypass everyone's locked content)",
    "自助注册": "Self-Registration",
    "允许任何人自己注册账号": "Allow anyone to register their own account",
    "默认关闭，新账号只能在上面手动加；打开之后 /register 页面才能用。":
        "Off by default — new accounts can only be added manually above; turning this on makes /register usable.",
    "数据备份": "Data Backup",
    "下载整个网站数据目录的原样打包（数据库文件 + 所有上传的图片/视频），不区分账号，是最完整的一份快照。文件可能比较大，下载需要一点时间。":
        "Download a raw copy of the whole data directory (database file + every uploaded/generated "
        "image and video), not scoped to any account — the most complete snapshot available. The file "
        "can be large, so it may take a moment.",
    "⬇️ 下载完整备份": "⬇️ Download Full Backup",
    "{u} 的密码已经重置": "{u}'s password has been reset",

    # --- admin_metrics.html ---
    "性能指标 - 知行合一AI实验室": "Metrics - Unity of Knowledge & Action AI Lab",
    "性能指标": "Metrics",
    "延迟和吞吐量数据只存在内存里，服务重启会清零，不做历史存档。":
        "Latency and throughput data lives in memory only — it resets on every restart, no history is kept.",
    "命中 CDN 边缘缓存的静态资源不会打到这里的源站，这里看到的是实际到达服务器的请求。":
        "Static assets served from the CDN edge never reach the origin — what you see here is requests that actually hit the server.",
    "最近 60 秒": "Last 60s",
    "请求数": "Requests",
    "平均延迟": "Avg latency",
    "最近 5 分钟": "Last 5 min",
    "状态码分布（最近 5 分钟）": "Status codes (last 5 min)",
    "按接口统计（最近 5 分钟，按请求量排序）": "By endpoint (last 5 min, sorted by volume)",
    "接口": "Endpoint",
    "运行时长：": "Uptime: ",
    " · 每 3 秒自动刷新": " · auto-refreshes every 3s",
    "{h}小时{m}分钟": "{h}h {m}m",
    "{m}分{s}秒": "{m}m {s}s",
    "{s}秒": "{s}s",

    # --- moment_scan.html ---
    "截图识别导入": "Screenshot Import",
    "从朋友圈截图批量导入": "Bulk Import from Screenshots",
    "在手机上把你自己发的朋友圈截图（文字+图片都行），传到电脑上传上来。":
        "Take a screenshot of your own posts (text or images both work) and upload them from your computer.",
    "AI 会自动识别文字、判断类型、草拟内容，你确认修改后再保存，不会跳过审核直接入库。":
        "AI reads the text, guesses the type, and drafts the content — you review and edit before saving, nothing is saved without your confirmation.",
    "还没有配置 AI 识图功能。请在项目目录下新建一个 <code>.env</code> 文件（可以参考 <code>.env.example</code>），":
        "AI screenshot recognition isn't configured yet. Create a <code>.env</code> file in the project directory (see <code>.env.example</code>), ",
    "填入一行 <code>ANTHROPIC_API_KEY=你的key</code>，保存后重启服务即可生效。":
        "add a line <code>ANTHROPIC_API_KEY=your_key</code>, save, and restart the server.",
    "选择截图（可多选）": "Choose screenshots (multiple allowed)",
    "开始识别": "Start Recognition",
    "改为手动添加": "Add manually instead",
    "还没有配置 ANTHROPIC_API_KEY，请先在 .env 文件里填好再重试。": "ANTHROPIC_API_KEY isn't configured yet — set it in .env and try again.",
    "请至少选择一张截图。": "Select at least one screenshot.",

    # --- moment_scan_review.html ---
    "确认识别结果": "Review Results",
    "检查一下 AI 识别的内容，改一改不准确的地方；不想要的取消勾选「保存这条」，最后点保存全部。":
        "Check what the AI recognized and fix anything off — uncheck “Save this” for ones you don't want, then save all.",
    "截图预览": "Screenshot preview",
    "保存这条": "Save this",
    "标题": "Title",
    "内容": "Content",
    "保存全部": "Save All",
    "重新上传": "Upload Again",
    "没有识别出任何内容。": "Nothing was recognized.",

    # --- trading (error/info flash messages set from Python) ---
    "请选择一个 CSV 文件": "Choose a CSV file",
    "文件解析失败，确认是券商导出的交易记录 CSV": "Couldn't parse the file — make sure it's a broker-exported transaction CSV",
    "导入完成：新增 {n} 条，跳过 {s} 条重复。": "Import done: {n} added, {s} duplicates skipped.",
    "已清空所有导入的交易记录。": "All imported trades have been cleared.",
    "请选择一个 PDF 文件": "Choose a PDF file",
    "打不开这个文件，确认密码是否正确、文件是否为工商银行历史明细 PDF": "Couldn't open this file — check the password, and make sure it's an ICBC statement PDF",
    "文件解析失败，确认是工商银行导出的历史明细 PDF": "Couldn't parse the file — make sure it's an ICBC-exported statement PDF",
    "已清空所有导入的流水记录。": "All imported bank transactions have been cleared.",

    # --- expenses.html ---
    "消费追踪": "Spending Tracker",
    "导入银行流水": "Import Bank Statement",
    "目前支持工商银行「历史明细」PDF（需要密码）。可以随时导入新的导出文件追加记录，已经导入过的交易会自动跳过，不会重复计算。":
        "Currently supports ICBC's \"历史明细\" (statement) PDF (needs the password). Import a fresh export "
        "any time to add more — transactions already imported are automatically skipped, never double-counted.",
    "PDF 密码": "PDF password",
    "确定清空所有已导入的流水记录吗？此操作不可撤销。": "Clear all imported bank transactions? This can't be undone.",
    "还没有导入任何流水记录，上传上面的 PDF 开始看消费日历。":
        "No transactions imported yet — upload a PDF above to see the spending calendar.",
    "总支出": "Total expense",
    "总收入": "Total income",
    "净流入": "Net flow",
    "支出分类": "Spending by Category",
    "还没有支出记录。": "No expenses yet.",
    "收入分类": "Income by Category",
    "还没有收入记录。": "No income yet.",
    "最新余额": "Latest balance",
    "年末余额": "Year-end balance",
    "周日": "Sun",
    "周六": "Sat",
    "各月消费汇总": "Monthly Spending",
    "{y} 年消费汇总": "{y} Spending Summary",
    "全年消费合计：": "Year net spending: ",
    "按月消费柱状图": "Monthly spending bar chart",
    "分享图不会显示具体金额，只显示每月消费的高低走势。": "The share image doesn't show exact amounts, just the shape of month-to-month spending.",
    "分享图不会显示具体金额，只显示走势形状、盈利/亏损天数、胜率和盈亏比。": "The share image doesn't show exact amounts, just the shape of the curve, the win/loss day counts, the win rate, and the win/loss ratio.",
    "{y} 年消费商户 Top 10": "{y} Top 10 Merchants",
    "本月消费商户 Top 10": "Top 10 Merchants This Month",

    # --- trading.html ---
    "交易盈亏": "Trading P&L",
    "导入交易记录": "Import Transactions",
    "目前支持 Schwab 导出的「Transactions」CSV。可以随时导入新的导出文件追加记录，已经导入过的交易会自动跳过，不会重复计算。":
        "Currently supports Schwab's \"Transactions\" CSV export. Import a fresh export any time to add more — "
        "trades already imported are automatically skipped, never double-counted.",
    "上传": "Upload",
    "确定清空所有已导入的交易记录吗？此操作不可撤销。": "Clear all imported trades? This can't be undone.",
    "清空所有记录": "Clear All",
    "还没有导入任何交易记录，上传上面的 CSV 开始看盈亏日历和走势图。":
        "No trades imported yet — upload a CSV above to see the P&L calendar and chart.",
    "累计已实现盈亏": "Total realized P&L",
    "盈利天数": "Winning days",
    "亏损天数": "Losing days",
    "盈亏比": "Win/loss ratio",
    "平均每个盈利日 ÷ 平均每个亏损日（取绝对值）": "Average winning day ÷ average losing day (absolute value)",
    "胜率": "Win rate",
    "盈利天数 ÷（盈利天数 + 亏损天数）": "Winning days ÷ (winning days + losing days)",
    "按天统计": "By Day",
    "按笔统计": "By Trade",
    "同一天可能有好几笔交易，只看当天合计是赚是赔": "A day can have several trades — this only looks at whether the day's total was up or down",
    "每一笔平仓单独算一笔交易，跟按天统计是两回事": "Each closing trade counts on its own here — a different thing from the by-day stats",
    "盈利笔数 ÷（盈利笔数 + 亏损笔数）": "Winning trades ÷ (winning trades + losing trades)",
    "平均每笔盈利 ÷ 平均每笔亏损（取绝对值）": "Average winning trade ÷ average losing trade (absolute value)",
    "最佳单日 ({d})": "Best day ({d})",
    "最差单日 ({d})": "Worst day ({d})",
    "总交易笔数": "Total trades",
    "盈利笔数": "Winning trades",
    "亏损笔数": "Losing trades",
    "按品种统计": "By Symbol",
    "品种": "Symbol",
    "笔数": "Trades",
    "总盈利": "Total win",
    "总亏损": "Total loss",
    "净盈亏": "Net P&L",
    "目前仍持有的仓位": "Open positions",
    "有 {n} 笔平仓在导入的记录里找不到对应的开仓，可能是导入范围之前建的仓——这部分暂时按 $0 盈亏处理，不会拉低或拉高总盈亏。":
        "{n} closing trade(s) have no matching opening trade in the imported data — likely positions opened "
        "before the imported range. Treated as $0 P&L for now, so they don't skew the total either way.",
    "累计盈亏走势": "Cumulative P&L",
    "累计盈亏走势图": "Cumulative P&L chart",
    "上月": "Prev",
    "下月": "Next",
    "毛利润（未扣手续费）": "Gross P&L (before fees)",
    "手续费合计": "Total fees",
    "净利润（已扣手续费）": "Net P&L (after fees)",
    "各月盈亏汇总": "Monthly Summary",
    "周一": "Mon",
    "周二": "Tue",
    "周三": "Wed",
    "周四": "Thu",
    "周五": "Fri",

    # --- showcase.html ---
    "网站现在有哪些功能": "What the Site Can Do",
    "功能一览": "Features",
    "✨ 功能一览": "✨ Features",
    "交易 · 消费 · 创作 · 生活点滴，都在这一个地方": "Trading, spending, writing, and everyday life -- all in one place",
    "去看看 →": "Take a look →",
    "分享图是一张介绍这几个功能的图片，方便发给别人看。": "The share image is a poster introducing these features, handy for sending to someone else.",
    "从前，有座山，山里有座庙……": "Once upon a time, on a mountain, there was a temple...",
    "第三章 · 山雨欲来": "Chapter 3 · The Storm Ahead",
    "读完《百年孤独》第三章": "Finished Ch. 3 of a novel",
    "跑步 5 公里": "Ran 5 km",
    "今天想明白一件事": "Figured something out today",
}
