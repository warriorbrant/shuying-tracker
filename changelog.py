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
]
