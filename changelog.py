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
    {
        "date": "2026-07-22",
        "title": "上传图片自动压缩",
        "title_en": "Uploaded photos are now auto-compressed",
        "summary": (
            "手机拍的照片动辄几 MB，之前上传是原样存的。现在超过 1600px 的一律等比缩小，"
            "转成压缩率更高的 JPEG（实测一张 10MB 的照片能压到 1MB 出头）；"
            "带透明通道的 PNG 保留 PNG 格式不转 JPEG，GIF 不处理以免破坏动图。"
        ),
        "summary_en": (
            "Phone photos are often several MB each, and uploads used to be stored as-is. "
            "Now anything over 1600px gets scaled down proportionally and re-encoded as a "
            "more efficient JPEG (a 10MB test photo came down to just over 1MB). PNGs with "
            "real transparency stay PNG instead of being converted to JPEG, and GIFs are "
            "left untouched so animations don't break."
        ),
        "image": None,
        "lines_changed": 33,
        "estimated": False,
    },
    {
        "date": "2026-07-22",
        "title": "网站正式上线，修好了 Railway 自动部署",
        "title_en": "Site is live, and Railway auto-deploy is finally fixed",
        "summary": (
            "网站正式部署上线了，数据库和照片也从本地迁移过去了。中间卡了好一阵：push 代码后 "
            "Railway 一直不会自动重新部署，Source 设置里显示「GitHub Repo not found」——"
            "原因是 Railway 这个 GitHub App 从来没有真正装到 GitHub 账号上，只做过一次身份登录。"
            "去 github.com/apps/railway-app 重新安装并勾选这个仓库，再断开重连一次 Source，"
            "auto deploy 就正常了。这条本身就是用来验证修复是否生效的测试提交。"
        ),
        "summary_en": (
            "The site is now live in production, with the database and photos migrated over "
            "from local. Got stuck for a while first: pushing code never triggered a Railway "
            "redeploy, and the Source settings showed \"GitHub Repo not found\" — turned out "
            "the Railway GitHub App had never actually been installed on the GitHub account, "
            "only an identity sign-in had happened. Reinstalling it at github.com/apps/"
            "railway-app with this repo selected, then disconnecting/reconnecting the Source, "
            "fixed auto-deploy. This entry itself is the test commit used to confirm the fix."
        ),
        "image": None,
        "lines_changed": 12,
        "estimated": False,
    },
    {
        "date": "2026-07-22",
        "title": "首页改成瀑布流分页：一开始只加载 20 条",
        "title_en": "Homepage feed is now paginated: loads 20 at a time",
        "summary": (
            "首页动态流原来一次性把所有记录都渲染出来。现在改成只加载最新 20 条，"
            "往下滚动接近底部时用 IntersectionObserver 自动请求下一批 20 条并追加到列表末尾，"
            "全部加载完才会停止监听。筛选条件（类型/状态）在翻页时也会保持一致。"
        ),
        "summary_en": (
            "The homepage feed used to render every record at once. Now it only loads the "
            "most recent 20, and an IntersectionObserver watching the bottom of the list "
            "automatically fetches and appends the next 20 as you scroll down, stopping once "
            "everything's loaded. Active type/status filters carry through to each page."
        ),
        "image": "infinite-scroll.png",
        "lines_changed": 202,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "滚动加载扩展到全站，首页排序也调整了",
        "title_en": "Infinite scroll extended site-wide, homepage ordering tweaked",
        "summary": (
            "把首页那套滚动加载的逻辑抽成了一个通用的 static/infinite-scroll.js，"
            "现在条目详情页的「历史记录」和更新日志页（按天分页）也用上了同一套机制，"
            "不用再各写一份重复代码。同时改了首页排序规则：同一天内，网站更新会排在"
            "书影/动态等其他内容之后，但整个当天的内容仍然排在前一天之前，不会打乱按天分组的顺序。"
        ),
        "summary_en": (
            "Extracted the homepage's scroll-loading logic into a reusable "
            "static/infinite-scroll.js. The item detail page's history list and the "
            "changelog page (paginated by day) now use the same mechanism instead of each "
            "having its own copy. Also tweaked homepage ordering: within the same day, site "
            "update entries now sort after everything else (books/shows/moments), while the "
            "whole day's content still comes before the previous day's, so day-grouping "
            "stays intact."
        ),
        "image": "full-site-pagination.png",
        "lines_changed": 257,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "加了全站搜索",
        "title_en": "Added site-wide search",
        "summary": (
            "导航栏新增「🔍 搜索」。能搜书/剧的标题、作者、总评，也能搜每日进度里的备注、"
            "以及股票/运动/照片/想法这些动态的标题和内容。结果复用了首页动态卡片的样式，"
            "同样支持滚动加载。"
        ),
        "summary_en": (
            "Added a \"🔍 Search\" link in the nav bar. It searches book/show titles, "
            "authors, and reviews, plus daily progress comments and the title/content of "
            "stock/exercise/photo/thought moments. Results reuse the same card styling as "
            "the homepage feed and support infinite scroll too."
        ),
        "image": "search-feature.png",
        "lines_changed": 139,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "更新日志页面对所有人公开，其余页面仍需登录",
        "title_en": "Changelog page is now public; everything else still needs login",
        "summary": (
            "部署到公网后之前是全站都要密码登录，现在改成只有更新日志页面（含中英切换、"
            "两张一键分享图）任何人都能直接看，不用登录；其他页面（首页、条目详情、搜索等）"
            "照旧需要密码。顺带修了个小问题：没登录时访问更新日志页，之前会错误地显示"
            "「退出登录」按钮，现在只有真正登录了才会出现。"
        ),
        "summary_en": (
            "After deploying publicly, the whole site used to require a password. Now only "
            "the changelog page (including the Chinese/English toggle and both one-click "
            "share images) is open to anyone without logging in; everything else (homepage, "
            "item detail, search, etc.) still needs the password. Also fixed a small bug "
            "where the \"Log out\" button showed up even for anonymous visitors to the "
            "changelog page — it now only appears when actually logged in."
        ),
        "image": "public-changelog.png",
        "lines_changed": 7,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "首页对未登录访客改成公开的更新日志 + 登录入口",
        "title_en": "Homepage shows a public changelog + login prompt when signed out",
        "summary": (
            "之前部署到公网后，没登录访问首页会直接跳转到登录页。现在改成首页本身就能打开，"
            "没登录时显示的是更新日志内容（热力图、按天分组、两张分享图）加一个登录按钮，"
            "导航栏里「添加书」「记录动态」「搜索」这些需要登录的入口也会先隐藏，登录后自动"
            "换回完整的个人动态首页。本地不设密码的时候还是跟以前一样直接显示全部内容，不受影响。"
        ),
        "summary_en": (
            "Previously, an unauthenticated visit to the homepage on the public deployment "
            "just redirected straight to the login page. Now the homepage itself always "
            "loads: signed out, it shows the changelog content (heatmap, day groups, both "
            "share images) plus a login button, and the nav links that need login (add "
            "book, log a moment, search) are hidden until you sign in — after which it "
            "switches back to the full personal feed. Local runs with no password configured "
            "are unaffected and still show everything directly."
        ),
        "image": "public-homepage.png",
        "lines_changed": 112,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "修复服务器时区导致的日期错位",
        "title_en": "Fixed a server-timezone bug that misdated \"today\"",
        "summary": (
            "线上出现过热力图没显示 23 号、但更新日志里已经有 23 号记录的不一致。根因是 "
            "Python 的 date.today() 和 SQLite 的 datetime('now','localtime') 都跟着服务器"
            "所在时区走，Railway 的服务器在美区，比北京时间晚了大半天，导致服务器还以为是"
            "22 号。修复方式是在应用启动时把进程时区强制固定成 Asia/Shanghai，这样不管部署"
            "在哪个地区，「今天」都以北京时间为准。Docker 镜像里也加装了 tzdata，避免精简"
            "镜像缺时区数据库导致设置不生效。"
        ),
        "summary_en": (
            "Production showed an inconsistency where the heatmap hadn't picked up the "
            "23rd yet, but the changelog already had entries dated the 23rd. Root cause: "
            "both Python's date.today() and SQLite's datetime('now','localtime') follow "
            "whatever timezone the server happens to be in — Railway's server is in the US, "
            "many hours behind Beijing time, so the server still thought it was the 22nd. "
            "Fixed by pinning the process timezone to Asia/Shanghai at startup, so \"today\" "
            "is always Beijing time regardless of which region it's deployed in. Also "
            "installed tzdata in the Docker image so the slim base image actually has the "
            "timezone database available."
        ),
        "image": "timezone-fix.png",
        "lines_changed": 10,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "公开首页加了开发流程示意图",
        "title_en": "Added a dev-workflow diagram to the public homepage",
        "summary": (
            "未登录访客看到的首页顶部加了一个小示意图：跟 Claude 对话提需求 → Claude Code "
            "写代码 → 推送到 GitHub → Railway 自动部署 → 网站更新上线，直观展示这个网站全程"
            "怎么做出来的，旁边带了 GitHub 仓库链接。手机窄屏下会自动从横排切成竖排。"
        ),
        "summary_en": (
            "Added a small diagram near the top of the public (signed-out) homepage: "
            "chat with Claude about what to build → Claude Code writes it → push to GitHub "
            "→ Railway auto-deploys → the site updates, with a link to the GitHub repo "
            "alongside it. Switches from a horizontal row to a stacked column automatically "
            "on narrow phone screens."
        ),
        "image": "dev-pipeline.png",
        "lines_changed": 99,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "更新定位文案：从「书影/生活追踪」到「个人AI应用实验室」",
        "title_en": "Updated positioning copy: from a tracker to a personal AI app lab",
        "summary": (
            "网站已经不只是一个书影/生活追踪工具了，改了公开首页横幅、README、PWA "
            "描述里的措辞，把它说清楚：这是一个用 AI 从零搭建的个人应用实验室，"
            "书影/生活追踪是目前跑在里面的第一个功能，以后会陆续加新的实验性功能进来。"
        ),
        "summary_en": (
            "The site has grown past being just a book/show/life tracker. Updated the "
            "wording on the public homepage banner, README, and PWA description to say so: "
            "this is a personal AI app lab built from scratch with AI, and the book/show/"
            "life tracker is just the first feature running in it — more experimental "
            "features to come."
        ),
        "image": None,
        "lines_changed": 6,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "加了传统开发流程对比图",
        "title_en": "Added a traditional-workflow comparison diagram",
        "summary": (
            "在 AI 开发流程示意图下面，加了一版对比：传统开发模式（写需求文档 → 工程师"
            "手写代码 → 写测试跑测试 → Code Review → 手动构建部署 → 上线），图标做成灰度"
            "区分两种模式，两边都标了大致耗时——AI 模式几分钟到几小时，传统模式通常数天"
            "到数周，一眼看出差别。"
        ),
        "summary_en": (
            "Added a comparison below the AI workflow diagram: the traditional development "
            "process (write a spec → an engineer hand-writes the code → write and run tests "
            "→ code review → manual build/deploy → launch), with grayscale icons to visually "
            "set it apart from the AI flow. Both are labeled with a rough timeframe — minutes "
            "to hours for the AI mode, typically days to weeks for the traditional one — so "
            "the difference is obvious at a glance."
        ),
        "image": "pipeline-comparison.png",
        "lines_changed": 125,
        "estimated": False,
    },
    {
        "date": "2026-07-23",
        "title": "性能优化：缓存豆瓣封面、开启压缩",
        "title_en": "Performance: cache Douban covers, enable compression",
        "summary": (
            "四项优化：① 豆瓣封面图代理之前每次都要重新跨太平洋抓一遍，现在抓过一次就存到"
            "本地磁盘，实测第二次访问从 3.3 秒降到 0.13 秒；② 全站开启了 gzip/brotli 压缩，"
            "页面体积明显变小；③ 静态资源（CSS、图标）加了 30 天的浏览器缓存；④ 分享卡片"
            "生成用到的字体文件之前每次画字都要重新加载，现在缓存住了。服务器所在地区带来的"
            "基础网络延迟没动，这个之后有需要再考虑迁移机房解决。"
        ),
        "summary_en": (
            "Four optimizations: (1) the Douban cover-image proxy used to re-fetch across "
            "the Pacific on every request — now it's cached to local disk after the first "
            "fetch, cutting a repeat load from 3.3s to 0.13s in testing; (2) enabled gzip/"
            "brotli compression site-wide, noticeably shrinking page size; (3) static assets "
            "(CSS, icons) now get a 30-day browser cache; (4) the fonts used for generating "
            "share cards used to reload from disk on every single text draw — now cached. "
            "The baseline network latency from the server's region is untouched by any of "
            "this — that would need an actual region migration if it's ever worth doing."
        ),
        "image": "performance.png",
        "lines_changed": 35,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "实测了一下性能优化的效果",
        "title_en": "Measured the actual impact of the performance work",
        "summary": (
            "把上次做的性能优化实测了一遍，写个真实数字：本地首页压缩前 67.9KB，开 gzip 后 "
            "9.1KB，体积降了约 87%，本地响应都在 20-30ms。豆瓣封面代理缓存的效果之前测过，"
            "同一张图第二次访问从 3.3 秒降到 0.13 秒。线上（Railway）从这次测试所在的网络环境"
            "访问首页大概 0.9-1.1 秒，这个数字主要是服务器地区带来的基础网络延迟，跟你实际"
            "从国内访问的体验不完全一样，仅供参考——这也是当时决定暂不迁移机房、先做应用层"
            "优化的原因。"
        ),
        "summary_en": (
            "Actually measured last session's performance work instead of just claiming it "
            "helps: locally, the homepage is 67.9KB uncompressed vs 9.1KB with gzip (~87% "
            "smaller), with local responses at 20-30ms. The Douban cover-proxy cache had "
            "already been measured: 3.3s down to 0.13s for a repeat load of the same image. "
            "Hitting the live Railway deployment from this testing environment, the homepage "
            "takes roughly 0.9-1.1s — that's mostly baseline network latency from the "
            "server's region, and won't exactly match what the user sees from mainland China "
            "— for reference only. This is also why the region-migration option was deferred "
            "in favor of application-level fixes for now."
        ),
        "image": None,
        "lines_changed": 0,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "服务器迁到新加坡机房，开启 CDN 缓存",
        "title_en": "Moved the server to Singapore, turned on CDN caching",
        "summary": (
            "上一条实测数据显示，剩下的延迟主要来自服务器所在地区，于是把 Railway 的部署"
            "区域从美西迁到了新加坡（Railway 原生支持带 Volume 的服务迁移区域，会自动搬运"
            "数据，迁移过程中确认了书影条目、代码量统计等数据完好无损）。同时开启了 Railway "
            "的边缘 CDN 缓存：默认模式下只有主动设置了 Cache-Control 的响应才会被缓存，登录"
            "态的动态页面因为带 Set-Cookie 天然被排除在外，实测静态资源（CSS/JS、豆瓣封面、"
            "上传的照片）已经能命中边缘缓存（x-cache: HIT），个人数据不受影响。"
        ),
        "summary_en": (
            "The previous measurement showed the remaining latency was mostly the server's "
            "region, so migrated the Railway deployment from US West to Singapore (Railway "
            "natively supports migrating volume-backed services between regions, moving the "
            "data automatically — verified afterward that items, logs, and the code-volume "
            "stats were all intact). Also turned on Railway's edge CDN caching: by default it "
            "only caches responses that explicitly set Cache-Control, and authenticated pages "
            "are naturally excluded since they carry a Set-Cookie header. Confirmed static "
            "assets (CSS/JS, cached Douban covers, uploaded photos) now hit the edge cache "
            "(x-cache: HIT) with no change to private/dynamic content."
        ),
        "image": None,
        "lines_changed": 0,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "加了性能指标：延迟和 QPS",
        "title_en": "Added performance metrics: latency and QPS",
        "summary": (
            "给网站接了一套轻量的请求耗时统计：每个请求进出都记一笔，存在内存里的一个环形"
            "缓冲区（不落盘，服务重启就清零）。登录后能看私密的 /admin/metrics 页面，有最近 "
            "60 秒和 5 分钟的 QPS、平均延迟、P50/P95/P99，以及按接口拆分的请求量和状态码"
            "分布，每 3 秒自动刷新。更新日志页面也加了一个精简版的公开统计卡片。因为线上用 "
            "gunicorn 起了多个 worker 进程，内存数据不共享，顺带把部署配置从多进程改成单"
            "进程多线程，这样统计到的才是全站真实数据，不是随机分到某个 worker 上的一部分。"
        ),
        "summary_en": (
            "Added lightweight request-timing instrumentation: every request records its "
            "duration into an in-memory ring buffer (no disk writes, resets on restart). "
            "Logged-in users get a private /admin/metrics page showing QPS, avg latency, and "
            "P50/P95/P99 over the last 60s and 5 minutes, plus a per-endpoint breakdown and "
            "status-code counts, auto-refreshing every 3 seconds. The changelog page also got "
            "a smaller public summary card. Since production ran gunicorn with multiple worker "
            "processes, the in-memory stats weren't shared between them — switched the deploy "
            "config to a single process with threads instead, so the numbers reflect the whole "
            "site rather than whichever worker happened to handle a request."
        ),
        "image": None,
        "lines_changed": 339,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "首页加了一张详细的技术架构图",
        "title_en": "Added a detailed architecture diagram to the homepage",
        "summary": (
            "在公开首页的开发流程图下面，加了一张手绘的技术架构图（SVG）：浏览器 → Railway "
            "边缘 CDN（缓存命中直接返回，未命中才打到源站）→ 源站容器（Railway 新加坡，"
            "gunicorn 单进程多线程）→ Flask 应用内部（路由鉴权、Jinja2 渲染、压缩、请求耗时"
            "统计）→ 再往下分两支：持久化存储（Volume 里的 SQLite 数据库、上传照片、豆瓣封面"
            "缓存）和外部服务（豆瓣抓取、Claude API）。图下面配了一段文字补充细节。"
        ),
        "summary_en": (
            "Added a hand-drawn SVG architecture diagram below the dev-pipeline diagram on the "
            "public homepage: browser → Railway edge CDN (cache hit returns directly, miss goes "
            "to origin) → origin container (Railway Singapore, gunicorn single process/multi-"
            "thread) → inside the Flask app (routing/auth, Jinja2 rendering, compression, "
            "request-latency instrumentation) → branching down into persistent storage (SQLite "
            "DB, uploaded photos, Douban cover cache, all on the Volume) and external services "
            "(Douban scraping, Claude API). A paragraph below the diagram fills in more detail."
        ),
        "image": None,
        "lines_changed": 95,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "修复热力图和架构图在手机上显示不全的问题",
        "title_en": "Fixed the heatmap and architecture diagram overflowing on mobile",
        "summary": (
            "热力图和架构图在手机上只能显示一半、要向右滑才能看完。架构图直接重画成单列纵向"
            "布局，靠 SVG 的 viewBox 整体缩放，不再需要横向滚动。热力图的问题更细：月份标签"
            "（「12月」这种）是每周一个固定宽度的格子，字号再怎么缩小，中文加数字也塞不进"
            "一周格子的宽度，导致整行溢出——干脆在小屏幕上直接隐藏月份标签，格子本身缩小到 "
            "4px，正好能塞进一屏。这次没法用手机实机测，改用无头 Chrome + iframe 撑出一个真实 "
            "375px 视口分别测了两处，确认没有溢出之后才提交。"
        ),
        "summary_en": (
            "The heatmap and architecture diagram only showed half on mobile, requiring a "
            "sideways swipe to see the rest. Redrew the architecture diagram as a single "
            "vertical column that scales as a whole via the SVG viewBox, so it no longer needs "
            "horizontal scrolling. The heatmap's issue was subtler: month labels like \"12月\" "
            "sit in a fixed-width cell matching one week's column, and no matter how small the "
            "font gets, Chinese characters plus digits can't fit into a single week-column's "
            "width, causing the row to overflow — so the labels are just hidden on small "
            "screens, and the day cells themselves shrink to 4px to fit in one screen width. "
            "Couldn't test on a real phone this time, so used headless Chrome with an iframe to "
            "get a genuine 375px viewport and confirmed no overflow in either spot before "
            "committing."
        ),
        "image": None,
        "lines_changed": 57,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "上线小说功能：章节、人物概念图、AI 视频，全部公开可看",
        "title_en": "Launched a novel-writing feature: chapters, character art, AI videos — all public",
        "summary": (
            "加了一个写小说的功能，登录后可以在网站里直接写、按章节管理；每部小说旁边能放"
            "人物角色的概念图（自己用 AI 工具生成好之后上传），还能放根据文字做的 AI 视频——"
            "支持直接上传视频文件（限时 5 分钟，上传后用 ffmpeg 自动压缩、生成封面帧），也支持"
            "粘贴 B 站/YouTube 链接直接嵌入播放。跟网站其余部分不同，这部分内容不需要登录就能"
            "看，只有创作（写章节、加角色、加视频）还是要登录。为了不把私人照片目录也顺带公开，"
            "小说的媒体文件单独存了一个目录、走一个专门的公开路由。视频压缩这一步比较吃 CPU，"
            "顺带把 gunicorn 的超时时间从 60 秒调到了 300 秒，不然大文件压缩到一半请求就被杀了。"
        ),
        "summary_en": (
            "Added a novel-writing feature: chapters can be written and managed directly on the "
            "site once logged in. Each novel can show character concept art (generated "
            "externally with AI tools, then uploaded) and AI-generated videos based on the "
            "text — either upload a video file directly (5-minute cap, auto-compressed with "
            "ffmpeg and given a poster frame) or paste a Bilibili/YouTube link for inline "
            "embedding. Unlike the rest of the site, this content is viewable without logging "
            "in — only authoring (writing chapters, adding characters/videos) still requires "
            "login. To avoid accidentally making the private photo directory public too, novel "
            "media lives in its own directory behind a dedicated public route. Video "
            "compression is CPU-heavy, so gunicorn's timeout went from 60s to 300s — otherwise "
            "the request got killed mid-compression on larger files."
        ),
        "image": None,
        "lines_changed": 988,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "小说章节可以挑选出场人物和视频，人物做成立绘展示",
        "title_en": "Chapters can pick characters/videos, characters shown as standees",
        "summary": (
            "写章节的时候可以从已经上传的人物角色和视频里勾选，不用每章重新上传——加了两张"
            "关联表记录每章的出场人物和本章视频。打开章节页时，勾选的人物不再是一张张方图，"
            "而是做成「立绘」的样子浮在页面上：假设上传的是透明背景的图，不加相框和背景，"
            "配一层柔和的渐变底色和阴影，名字用小圆角标签贴在下面，视频则放在正文下面。"
        ),
        "summary_en": (
            "Writing a chapter now lets you pick from already-uploaded characters and videos "
            "instead of re-uploading per chapter — added two join tables tracking which "
            "characters/videos belong to which chapter. On the chapter page, picked characters "
            "no longer show as boxed photos but as floating standees: assuming a transparent-"
            "background upload, there's no frame or card background, just a soft gradient "
            "backdrop and drop shadow, with the name on a small pill tag underneath. Videos sit "
            "below the chapter text."
        ),
        "image": None,
        "lines_changed": 256,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "立绘显示完整、放大，出场时轻微动画登场",
        "title_en": "Standees show uncropped, bigger, with a subtle entrance animation",
        "summary": (
            "人物立绘之前用 object-fit: cover 会把图裁掉一截，改成 contain 之后完整显示（人物"
            "卡片、章节勾选列表里的缩略图也一起改了）；章节里的立绘尺寸也放大了不少（220px→"
            "340px，手机上 160px→230px）。加了一点互动感但没有做得太花：滚动到人物出场的地方时"
            "会有一个轻微的淡入+上浮动画，一个个错开登场，不是那种刷屏的特效，纯 CSS + 一个"
            "IntersectionObserver，尊重了系统的减弱动效设置。"
        ),
        "summary_en": (
            "Character standees previously used object-fit: cover, which cropped part of the "
            "image — switched to contain so the full image always shows (also fixed the "
            "character cards and the chapter picker thumbnails). Standee size in the chapter "
            "reader got noticeably bigger too (220px to 340px, 160px to 230px on mobile). Added "
            "a touch of interactivity without overdoing it: when you scroll to where a character "
            "appears, they fade and rise into view with a slight stagger between characters — "
            "no flashy effects, just CSS plus one IntersectionObserver, and it respects "
            "prefers-reduced-motion."
        ),
        "image": None,
        "lines_changed": 53,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "修复：立绘出场动画因为没有延迟，播放太快看不出来",
        "title_en": "Fixed: standee entrance animation had no delay, too fast to notice",
        "summary": (
            "上一条加的立绘出场动画，因为人物区块通常在章节页顶部、一打开就在屏幕里，"
            "IntersectionObserver 几乎瞬间触发，动画在页面刚渲染出来的时候就播完了，跟页面"
            "加载混在一起，基本看不出来是个动画。加了 0.3 秒的起始延迟（多角色再依次错开"
            "0.15 秒），让页面先完整显示一下，再开始淡入+上浮，这样才是真的能看到的动画。"
        ),
        "summary_en": (
            "The entrance animation added last commit was too fast to notice in practice — "
            "since the character section usually sits at the top of the chapter page, it's "
            "already in view the instant the page loads, so the IntersectionObserver fired "
            "almost immediately and the animation finished before the page had even settled, "
            "blending into the initial page load. Added a 0.3s base delay (plus 0.15s stagger "
            "per extra character) so the page renders fully first, then the standee fades and "
            "rises — now it actually reads as an animation."
        ),
        "image": None,
        "lines_changed": 4,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "重做：人物立绘改成读到名字时才出现，不是开头",
        "title_en": "Redesigned: standees now reveal at the character's first mention, not upfront",
        "summary": (
            "之前理解错了需求，做成了页面一打开就在顶部展示所有人物；实际想要的是读者读到"
            "这个人物的名字时才触发，比如读到「游企生道」这句才出现游企生的立绘，更有代入感。"
            "重新设计：把章节正文按行拆成段落，服务端找出每个出场人物的名字第一次出现在"
            "哪一段，就把立绘插在那一段后面，读者滚动到那里时才会触发淡入动画。如果某个"
            "人物选了但名字没在正文里出现，就放到章节末尾一个简单的小卡片列表里，不做动画。"
        ),
        "summary_en": (
            "Misread the original request and built characters showing all at once at the top "
            "of the page on load; what was actually wanted was the reveal triggering when the "
            "reader reaches that character's name in the text — e.g. the standee for 游企生 "
            "should appear right as the reader reads the line where he's mentioned, for a "
            "stronger sense of immersion. Redesigned: chapter text is split into paragraphs "
            "server-side, the first paragraph mentioning each selected character is found, and "
            "their standee is inserted right after it — the fade-in now triggers when the "
            "reader actually scrolls there. Characters selected but never mentioned in the text "
            "fall back to a small, unanimated card list at the end of the chapter."
        ),
        "image": None,
        "lines_changed": 76,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "章节目录改成一排 3 个的网格排版",
        "title_en": "Chapter list now shows 3 per row in a grid",
        "summary": "小说详情页和编辑页的章节目录，从竖排列表改成一排 3 个的网格，手机上自动收回单列。",
        "summary_en": (
            "The chapter list on both the novel detail page and the edit page switched from a "
            "single stacked column to a 3-per-row grid, collapsing back to one column on mobile."
        ),
        "image": None,
        "lines_changed": 13,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "人物角色可以编辑/替换概念图，章节里自动同步",
        "title_en": "Characters can now be edited/replaced, chapters sync automatically",
        "summary": (
            "之前人物角色只能新建和删除，没法改。加了一个编辑页，可以改名字、简介，或者"
            "换一张新的概念图（不上传就保持原图）。因为章节里的人物是通过角色 ID 关联查出来"
            "的，不是复制一份数据存死，所以换完图/改完名之后，所有引用了这个角色的章节——"
            "不管是章节顶部的名单还是正文里出场时的立绘——下次打开都会自动显示最新的样子，"
            "不用一章一章去重新设置。"
        ),
        "summary_en": (
            "Characters could previously only be created or deleted, not edited. Added an edit "
            "page: change the name, description, or swap in a new concept art image (leave it "
            "blank to keep the current one). Since chapters reference characters by ID and look "
            "them up live rather than storing a copy, every chapter referencing that character — "
            "including the inline standee reveal in the text — automatically shows the latest "
            "version the next time it's opened, with nothing to update per chapter."
        ),
        "image": None,
        "lines_changed": 81,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "章节正文加了禁止选中/复制/右键",
        "title_en": "Chapter text now blocks selection/copy/right-click",
        "summary": (
            "小说正文加了 user-select: none，鼠标没法拖选文字；同时拦截了 copy / cut / "
            "contextmenu 事件，Ctrl+C 和右键菜单里的复制也不起作用了。说清楚一下：这只是"
            "挡住顺手复制，不是真正的防护——查看网页源码、浏览器开发者工具、直接请求页面"
            "拿 HTML、截图 OCR 这些办法都能绕过去，技术上没有办法百分百阻止别人拿到文本。"
        ),
        "summary_en": (
            "Chapter text now has user-select: none, so mouse drag-selection doesn't work; also "
            "intercepts copy/cut/contextmenu events, so Ctrl+C and the right-click menu's copy "
            "option no longer do anything. Worth being upfront: this only blocks casual "
            "copy-pasting, not a determined attempt — view-source, browser devtools, fetching "
            "the page's HTML directly, or screenshot+OCR all bypass it. There's no way to "
            "technically prevent someone from getting the text once it's in their browser."
        ),
        "image": None,
        "lines_changed": 15,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "小说主页加了参考书目，粘贴豆瓣链接自动填充",
        "title_en": "Added a reference bibliography, auto-filled from a Douban link",
        "summary": (
            "小说详情页加了「参考书目」板块，只存三个字段：书名、封面、豆瓣链接，点封面/书名"
            "直接跳到豆瓣。加书的时候复用了原来「添加书」表单那套逻辑——粘贴豆瓣链接点"
            "「自动填充」，直接调已有的抓取接口把书名和封面填好，不用再重新走一遍手动录入。"
        ),
        "summary_en": (
            "Added a \"reference bibliography\" section to the novel detail page — just three "
            "fields: title, cover, and Douban link, clicking the cover or title jumps straight "
            "to Douban. Adding a book reuses the same auto-fill flow as the existing \"add book\" "
            "form: paste a Douban link, click fetch, and the existing scraping endpoint fills in "
            "the title and cover instead of typing everything by hand."
        ),
        "image": None,
        "lines_changed": 150,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "参考书目改成从已有书目里选，不用重新录入",
        "title_en": "Reference bibliography now picks from existing books instead of re-entering",
        "summary": (
            "上一版参考书目是自己单独存一份书名/封面/豆瓣链接，等于重新加了一遍数据。改成"
            "直接从已经在追踪的书（首页那个书影列表）里勾选，跟章节挑人物/视频一样的勾选框"
            "界面；勾选的书本来就会正常出现在主页的时间线和书目列表里，不需要额外处理。"
            "要引用的书还没加过？表单里有个「先去添加一本」的链接，加完回来勾选就行，不用"
            "跳来跳去重新抓豆瓣数据。顺带给 items 表加了 douban_url 字段，添加书的时候用"
            "豆瓣自动填充会顺便存下豆瓣链接，之后可以点回去看原页面。"
        ),
        "summary_en": (
            "The previous version stored its own copy of title/cover/Douban link per reference "
            "— effectively re-entering data that already existed. Switched to picking directly "
            "from books already being tracked (the same list that shows on the homepage), using "
            "the same checkbox-picker UI as selecting characters/videos for a chapter. Since "
            "referenced books are just regular tracked items, they already show up in the "
            "homepage timeline and book list with no extra work needed. If the book you want to "
            "cite hasn't been added yet, there's a link straight to the add-book form; add it "
            "there and come back to check the box, no need to re-fetch anything from Douban. "
            "Also added a douban_url column to the items table itself, so using Douban auto-fill "
            "when adding a book now saves the original link too, for future reference."
        ),
        "image": None,
        "lines_changed": 86,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "小说主页加了一键分享图，含封面/简介/人物/章节/书目",
        "title_en": "Added a one-click share image for novels",
        "summary": (
            "小说详情页加了「一键生成分享图」，跟书影条目的分享卡片是同一套 Pillow 生成"
            "逻辑：封面、书名、状态、简介在最上面，往下依次是人物立绘（浮在柔和底色上，"
            "跟章节里的展示风格一致）、章节目录（两列，章节多了自动截断显示「还有 N 章」）、"
            "参考书目封面。内容一多卡片就跟着变长，不是固定尺寸。做的时候发现一个 bug："
            "透明背景的人物立绘直接转 RGB 会把透明的地方涂成黑色，改成了用图片自己的透明"
            "通道合成到底色上再画，封面图也做了同样的兼容。"
        ),
        "summary_en": (
            "Added a one-click share image to the novel detail page, using the same Pillow-"
            "based card generation as the book/show share cards. Cover, title, status, and "
            "summary sit at the top, followed by character standees (floating on a soft "
            "backdrop, matching the in-chapter style), a two-column chapter list (truncated "
            "with a \"+N more\" note once there are a lot), and reference-book covers. The card "
            "grows to fit the content instead of being a fixed size. Hit a bug along the way: "
            "naively converting a transparent-background character PNG to RGB painted the "
            "transparent areas black — fixed by compositing using the image's own alpha "
            "channel onto the background color instead, and applied the same fix to the cover "
            "image path."
        ),
        "image": None,
        "lines_changed": 304,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "修复：小说简介换行会导致分享图 500 报错",
        "title_en": "Fixed: a line break in the summary crashed the share image",
        "summary": (
            "线上报错了：生成小说分享图时如果简介是多行的（textarea 允许换行，你的真实"
            "小说简介就是三行），PIL 的 textlength() 一遇到带换行符的字符串就直接报错，"
            "500。这个文字换行函数是分享卡片功能共用的，之前条目的总评/感想只要写了多行"
            "也会中同样的招，只是刚好还没人这么写过。修法是按换行符先把文本切成段，每段"
            "单独换行，而不是把整段文字（含换行符）一起丢给 PIL 量长度——这样用户自己"
            "打的换行也会保留，不是简单粗暴地拼掉。"
        ),
        "summary_en": (
            "Production error: generating a novel's share image crashed with a 500 whenever "
            "the summary had a line break (textareas allow them, and the real novel's summary "
            "is three lines). PIL's textlength() throws on any string containing a newline. "
            "This text-wrapping helper is shared by every share card, so a multi-line book "
            "review or comment would have hit the exact same crash — it just hadn't happened "
            "to occur yet. Fixed by splitting the text on newlines first and wrapping each "
            "line separately, instead of feeding PIL the whole string (newlines included) at "
            "once — this also means the user's own line breaks are preserved rather than "
            "silently collapsed."
        ),
        "image": None,
        "lines_changed": 15,
        "estimated": False,
    },
]
