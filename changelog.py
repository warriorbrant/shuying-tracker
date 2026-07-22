CHANGELOG = [
    {
        "date": "2026-07-21",
        "title": "项目起步：书影追踪网站上线",
        "title_en": "Project kickoff: 书影追踪 (Book/Show Tracker) launches",
        "summary": (
            "用 Flask + SQLite 搭了一个本地跑的个人网站，用来记录看过的书和剧："
            "条目展示、每日进度、用时统计、感想评论，数据全部存在本地，不联网。"
        ),
        "summary_en": (
            "Built a personal, locally-run website with Flask + SQLite to track books and "
            "shows: entries, daily progress, time spent, and comments. All data stays local, "
            "no network calls."
        ),
        "image": "item-form.png",
        "lines_changed": 970,
        "estimated": True,
    },
    {
        "date": "2026-07-21",
        "title": "条目管理增强",
        "title_en": "Better entry management",
        "summary": (
            "加了编辑条目、首页卡片上直接切换状态（想看/进行中/已完成/放弃）、"
            "GitHub 风格的打卡热力图，以及单条目一键生成分享图（可直接发小红书）。"
        ),
        "summary_en": (
            "Added editing entries, switching status right from the homepage card "
            "(to-read/in-progress/done/dropped), a GitHub-style activity heatmap, and "
            "one-click shareable image cards for a single item."
        ),
        "image": None,
        "lines_changed": 380,
        "estimated": True,
    },
    {
        "date": "2026-07-21",
        "title": "豆瓣自动导入",
        "title_en": "Auto-import from Douban",
        "summary": (
            "添加条目时可以粘贴豆瓣链接自动填充标题、封面、作者/页数或集数。"
            "豆瓣读书页面抓取很稳定；豆瓣电影/剧集页面有反爬，改用手机版页面 + 搜索接口来拿数据。"
        ),
        "summary_en": (
            "Pasting a Douban link when adding an item now auto-fills the title, cover, "
            "author/page count or episode count. Douban's book pages scrape reliably; the "
            "movie/show pages have anti-bot protection, so those go through the mobile site "
            "plus a search endpoint instead."
        ),
        "image": "item-form.png",
        "lines_changed": 230,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "动态系统上线：股票 / 运动 / 照片 / 想法",
        "title_en": "Moments launch: stocks / exercise / photos / thoughts",
        "summary": (
            "除了书和剧，还能记录股票关注、运动、照片（支持本地上传）、日常想法，"
            "每条都能写评论。新增「日」视图，把当天所有记录汇总在一起，也能一键生成当天的分享图。"
        ),
        "summary_en": (
            "Beyond books and shows, you can now log stock watches, exercise, photos "
            "(local upload supported), and everyday thoughts, each with its own comment. "
            "Added a day view that rolls up everything from that day, with a one-click "
            "share image for it too."
        ),
        "image": "day-view.png",
        "lines_changed": 550,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "AI 截图识别导入",
        "title_en": "AI screenshot import",
        "summary": (
            "本想直接对接微信朋友圈导入内容，调研后发现没有可行的公开接口（第三方导出工具大多有隐私风险）。"
            "改成更实际的方案：手机截图朋友圈动态，上传后用 Claude 视觉模型自动识别文字、判断类型、"
            "草拟内容，人工确认后再批量保存。"
        ),
        "summary_en": (
            "Originally wanted to import WeChat Moments directly, but there's no viable "
            "public API for that (most third-party export tools carry real privacy risk). "
            "Went with a more practical approach instead: screenshot your Moments posts, "
            "upload them, and a Claude vision model reads the text, guesses the type, and "
            "drafts the content for you to review before batch-saving."
        ),
        "image": "moment-scan.png",
        "lines_changed": 365,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "首页重做：合并成统一瀑布流时间线",
        "title_en": "Homepage rebuilt into one unified feed",
        "summary": (
            "原来的「书影网格 + 最近动态列表」两个区块合并成一条按日期倒序的瀑布流时间线。"
            "书/剧每次更新进度都会作为新记录出现在当天，不会因为静态网格只显示一次；"
            "还没开始看的条目按加入日期出现一次，不会从首页消失。"
        ),
        "summary_en": (
            "Merged the old \"book/show grid + recent moments list\" into a single "
            "reverse-chronological masonry feed. Every progress update on a book/show now "
            "shows up as a new card on that day, instead of the item just sitting once in a "
            "static grid; untouched items still appear once, on the day they were added, so "
            "nothing vanishes from the homepage."
        ),
        "image": "homepage.png",
        "lines_changed": 300,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "部署准备：登录鉴权 / 持久化存储 / 容器化",
        "title_en": "Deployment prep: auth, persistent storage, containerization",
        "summary": (
            "为了能部署到云端随时随地用手机访问，加了密码登录（本地跑不受影响）、"
            "数据库和图片统一走可配置的持久化目录、Linux 中文字体适配、Dockerfile 和 Fly.io 部署配置，"
            "还加了 PWA 图标，可以在手机上「添加到主屏幕」当 App 用。部署到 Fly.io 这步还在等你处理账号和 API Key。"
        ),
        "summary_en": (
            "To eventually deploy to the cloud and use it from a phone anywhere, added "
            "password auth (no-op for local runs), a configurable persistent-storage "
            "directory for the DB and photos, Linux CJK font support, a Dockerfile and "
            "Fly.io config, and PWA icons so it can be added to a phone's home screen. "
            "Actually deploying to Fly.io is still pending — waiting on the account and API "
            "key."
        ),
        "image": "login.png",
        "lines_changed": 300,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "分享卡片改成瀑布流布局",
        "title_en": "Share cards switched to a masonry layout",
        "summary": (
            "「一键分享」生成的图片也从单列堆叠改成了双列瀑布流，跟网站首页风格一致；"
            "顺带修了卡片标题/元信息文字没有自动换行、长标题会超出卡片边框的问题。"
        ),
        "summary_en": (
            "The one-click share images moved from a single stacked column to a two-column "
            "masonry layout, matching the homepage's style. Also fixed card titles/metadata "
            "text not wrapping, which let long titles spill past the card border."
        ),
        "image": "share-card.png",
        "lines_changed": 180,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "一批图片显示问题修复",
        "title_en": "A round of image-rendering fixes",
        "summary": (
            "陆续修了：豆瓣图片防盗链导致封面显示不出来（不同豆瓣服务器对 Referer 要求还互相矛盾，"
            "最后加了后端图片代理彻底解决）、豆瓣海报被裁图参数压成正方形导致变形、"
            "封面图撑爆卡片高度和留白、CSS 缓存导致修改后刷新看不到效果等问题。"
        ),
        "summary_en": (
            "Fixed a string of issues: Douban's hotlink protection blocking cover images "
            "(different Douban servers even disagree on whether a Referer header is "
            "required — solved for good with a backend image proxy), Douban posters getting "
            "squashed into a square by a crop parameter, cover images stretching cards taller "
            "with blank space, and stale CSS caching hiding style changes after a refresh."
        ),
        "image": "item-detail.png",
        "lines_changed": 130,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "更新日志页面上线，并接入首页动态流",
        "title_en": "Changelog page launches, wired into the homepage feed",
        "summary": (
            "新增「更新日志」页面（导航栏可进），把这次会话的开发历程整理成时间线，配了效果截图。"
            "同时把每条更新也变成首页动态流里的一种状态（🛠️ 网站更新），跟股票/运动/照片/想法混排，"
            "但不占用真实的 moments 数据表，不会被误删。以后每次有意义的迭代，都会自动补一条记录进来。"
        ),
        "summary_en": (
            "Added a Changelog page (linked from the nav bar) laying out this session's "
            "development history as a timeline, with screenshots. Each entry also now shows "
            "up as its own type of card in the homepage feed (🛠️ Site update), mixed in with "
            "stocks/exercise/photos/thoughts — but it doesn't touch the real moments table, so "
            "it can't be accidentally deleted. From here on, every meaningful iteration gets "
            "an entry automatically."
        ),
        "image": "changelog-in-feed.png",
        "lines_changed": 270,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "「今天」页面接入网站更新 + 更新日志一键分享图",
        "title_en": "Day view picks up site updates + one-click changelog share images",
        "summary": (
            "查看某一天的详情页时，那天的网站更新记录现在也会一起显示。"
            "更新日志页面新增两个一键分享图按钮：最近 10 条更新 / 今天的更新，"
            "生成的图片是跟每日分享图一样的双列瀑布流卡片（第一版做成单列大图，"
            "结果一张图有 7000 多像素高没法用，改成小缩略图 + 瀑布流才正常）。"
        ),
        "summary_en": (
            "Viewing a specific day's detail page now also shows that day's site-update "
            "entries. The Changelog page got two one-click share buttons: last 10 updates / "
            "today's updates, rendered as the same two-column masonry cards as the daily "
            "share image (the first version was a single tall column — one image ended up "
            "over 7000px tall and was unusable; switching to small thumbnails + masonry "
            "fixed it)."
        ),
        "image": "changelog-share.png",
        "lines_changed": 205,
        "estimated": True,
    },
    {
        "date": "2026-07-22",
        "title": "更新日志加上代码量热力图",
        "title_en": "Code-volume heatmap added to the changelog",
        "summary": (
            "更新日志页面顶部加了一个 GitHub 风格的热力图，按天汇总每次更新改动的代码行数（不是用时）。"
            "列表也从纯时间顺序改成按天分组：每天显示这天一共几次更新、当天总共改了多少行代码，"
            "每条更新也单独标出自己的改动行数。这个项目一直没有用 Git，历史记录的行数只能是回顾估算的，"
            "标了「估算」；从这条开始的每一条都是改动时精确统计的。"
        ),
        "summary_en": (
            "Added a GitHub-style heatmap to the top of the Changelog page, aggregating each "
            "day's lines-of-code changed (not time spent). The list also changed from a flat "
            "timeline to day-grouped sections: each day shows how many updates happened and "
            "the day's total lines changed, with each entry also labeled with its own line "
            "count. This project never used Git, so history before this point is a rough, "
            "reconstructed estimate (marked \"estimated\"); every entry from this one onward "
            "is measured precisely at the time of the change."
        ),
        "image": "changelog-heatmap.png",
        "lines_changed": 169,
        "estimated": False,
    },
    {
        "date": "2026-07-22",
        "title": "更新日志分享图里也加上代码量热力图",
        "title_en": "Code-volume heatmap added to changelog share images too",
        "summary": (
            "「最近 10 条更新」「今天的更新」这两张一键分享图，之前只有标题和卡片列表，"
            "现在顶部也加上了跟网页版一样的代码量热力图（图片里用 Pillow 手绘的小方块网格），"
            "分享出去的图片信息更完整。"
        ),
        "summary_en": (
            "The \"last 10 updates\" and \"today's updates\" share images used to only have a "
            "heading and the card list; now they also get the same code-volume heatmap shown "
            "on the web page (hand-drawn as a small grid with Pillow), so the shared image "
            "carries more context on its own."
        ),
        "image": "changelog-share-heatmap.png",
        "lines_changed": 40,
        "estimated": False,
    },
    {
        "date": "2026-07-22",
        "title": "网站更名为「知行合一AI实验室」",
        "title_en": "Site renamed to \"知行合一AI实验室\" (Unity of Knowledge and Action AI Lab)",
        "summary": (
            "网站从「书影追踪」改名为「知行合一AI实验室」——页面标题、导航栏、登录页、"
            "PWA 图标和分享图水印都同步换了新名字。历史记录里提到旧名字的地方（比如项目起步那条）"
            "保留不改，算是准确的历史记录。"
        ),
        "summary_en": (
            "Renamed the site from \"书影追踪\" (Book/Show Tracker) to \"知行合一AI实验室\" — "
            "the page title, nav bar, login page, PWA icons, and share-image watermarks all "
            "updated to the new name. Historical entries that mention the old name (like the "
            "kickoff one) were left as-is, as an accurate record of what it was called at the "
            "time."
        ),
        "image": "rebrand.png",
        "lines_changed": 25,
        "estimated": False,
    },
    {
        "date": "2026-07-22",
        "title": "更新日志页面支持中英双语",
        "title_en": "Changelog page now supports Chinese and English",
        "summary": (
            "只有「更新日志」这一块加了国际化：页面上一个中/EN 按钮手动切换，每条记录、"
            "热力图月份标签、两张一键分享图都会跟着切换语言。网站其他部分（首页、条目详情等）"
            "保持中文不变，按你的要求只限定在日志部分。"
        ),
        "summary_en": (
            "Internationalization added, scoped to just the Changelog page: a manual "
            "中/EN toggle button switches the language for entries, the heatmap's month "
            "labels, and both one-click share images. The rest of the site (homepage, item "
            "detail, etc.) stays Chinese-only, as requested — this was scoped to the "
            "changelog specifically."
        ),
        "image": "changelog-i18n.png",
        "lines_changed": 271,
        "estimated": False,
    },
]
