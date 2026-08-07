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
    {
        "date": "2026-07-24",
        "title": "修复：分享图简介每行末尾多了个缺字方块",
        "title_en": "Fixed: a tofu box appeared at the end of every summary line",
        "summary": (
            "上一条修复上线后线上实测，简介每一行末尾都多了个小方块「□」——因为文本是"
            "Windows 风格换行符（\\r\\n），只按 \\n 切分的话，每段末尾会剩一个 \\r，字体没有"
            "这个控制字符的字形，就画成了缺字方块。改成先把 \\r\\n 和单独的 \\r 都统一换成 "
            "\\n 再切分，用真实数据在线上重新核对过，方块没了。"
        ),
        "summary_en": (
            "Tested the previous fix against production and found a tofu box at the end of "
            "every summary line — the text uses Windows-style line endings (\\r\\n), and "
            "splitting on \\n alone leaves a trailing \\r on each segment, which has no glyph "
            "in the font. Normalized \\r\\n and lone \\r to \\n before splitting; re-verified "
            "against the real production data and the boxes are gone."
        ),
        "image": None,
        "lines_changed": 4,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "修复：所有分享图被 CDN 缓存 30 天，改完看不到最新效果",
        "title_en": "Fixed: all share images were CDN-cached for 30 days",
        "summary": (
            "上一条修复部署上线后，线上截图还是老样子——查了下响应头，`cache-control: "
            "public, max-age=2592000`，CDN 缓存命中，压根没打到源站。根因是之前给静态"
            "文件设置的 30 天缓存（`SEND_FILE_MAX_AGE_DEFAULT`）是全局默认值，`send_file()` "
            "没单独指定的话，连这种每次都应该重新生成的动态分享图也套用了同一个 30 天缓存，"
            "小说、条目、每日、更新日志这四个分享图接口全都中招。给这四处都显式加了 "
            "`max_age=0`，改完之后分享图不再被 CDN 长期缓存，每次都是当前最新内容。"
        ),
        "summary_en": (
            "Deployed the previous fix but production still showed the old image — checked "
            "the response headers and found `cache-control: public, max-age=2592000`, an edge "
            "cache hit that never reached the origin. Root cause: the 30-day cache set for "
            "static files (`SEND_FILE_MAX_AGE_DEFAULT`) is a global default, and every "
            "`send_file()` call that doesn't override it — including these dynamically "
            "generated share images that should regenerate every time — inherited the same "
            "30-day cache. All four share-image endpoints (novel, item, day, changelog) had "
            "this. Added an explicit `max_age=0` to each, so they're no longer cached long-"
            "term at the edge and always reflect current content."
        ),
        "image": None,
        "lines_changed": 4,
        "estimated": False,
    },
    {
        "date": "2026-07-24",
        "title": "分享图链接加上版本号，避开已经卡住的旧缓存",
        "title_en": "Share links now carry a version param to dodge already-stuck caches",
        "summary": (
            "上一条修完 CDN 长期缓存的问题后，用带随机参数的网址测过源站确实是好的、参考"
            "书目封面也正常，但小说页上那个固定的分享链接（没有参数）在修复上线前就已经被"
            "缓存住了，`max_age=0` 只能防止以后的请求被长期缓存，改不了这一个已经缓存了的"
            "网址——不重新生成一个新网址的话，还是会一直卡在那次旧快照上，得等最多 30 天。"
            "干脆给「一键生成分享图」和「先预览」的链接都加上一个时间戳参数，每次打开小说"
            "页拿到的都是一个全新网址，直接绕开旧缓存，不用等它过期。"
        ),
        "summary_en": (
            "After fixing the long-lived CDN caching, verified with a cache-busted URL that "
            "the origin was correct and reference covers loaded fine — but the plain share "
            "link on the novel page (no query params) had already been cached before that fix "
            "shipped. max_age=0 only stops new long-lived caching going forward; it can't "
            "un-cache a URL that's already cached, so without a new URL it would keep serving "
            "that stale snapshot for up to 30 days. Added a timestamp query param to both the "
            "share and preview links, so every page load gets a brand-new URL that bypasses "
            "the stuck cache entirely instead of waiting it out."
        ),
        "image": None,
        "lines_changed": 8,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "修复：未登录时参考书目封面显示不出来",
        "title_en": "Fixed: reference book covers didn't load when logged out",
        "summary": (
            "这次是真找错方向了——问题根本不在分享图，是小说详情页本身：参考书目的豆瓣"
            "封面走 /cover-proxy 这个防盗链代理路由，但这个路由没被加进「公开路由」名单，"
            "没登录时访问会被直接 302 跳转到登录页而不是返回图片，所以封面显示不出来；"
            "登录之后能绕开这个跳转，看起来就正常了。跟手机/电脑、跟发不发新版本都没关系，"
            "纯粹是登录状态的问题——小说封面和人物立绘走的是另一个本来就公开的路由，没受"
            "影响，只有参考书目这一处会坏。把 cover_proxy 加进公开路由名单就好了。"
        ),
        "summary_en": (
            "Was chasing the wrong thing — this had nothing to do with the share image, it was "
            "the novel detail page itself: reference book covers go through the /cover-proxy "
            "anti-hotlink route, which was never added to the public-routes allowlist. Logged-"
            "out requests got redirected straight to the login page instead of the image, so "
            "the cover never rendered; logged in, the redirect never fires and it looks fine. "
            "Had nothing to do with device or deploys — purely login state. The novel's own "
            "cover and character standees use a different route that was already public, so "
            "only reference-book covers were affected. Added cover_proxy to the public "
            "endpoints list."
        ),
        "image": None,
        "lines_changed": 1,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "性能优化：让图片走 CDN 缓存、图片懒加载、数据库加索引",
        "title_en": "Perf pass: CDN-cache images, lazy-load them, add DB indexes",
        "summary": (
            "又做了一轮性能优化，这次先测再改。拆解时序发现服务器处理只占 ~0.18 秒，大头是"
            "到新加坡的网络往返；但意外发现所有图片（书封面、人物立绘、豆瓣封面）的 x-cache "
            "都是 DYNAMIC——明明设了缓存头却没被 CDN 缓存，每张图都一路回源新加坡。对比发现"
            "根因：Flask 的 send_file 给图片加了 Content-Disposition 和 Accept-Ranges 两个头，"
            "Railway 的 CDN 就因此不缓存了（被压缩的 CSS 没这俩头，所以能缓存）。加了个 "
            "after_request 钩子，把内联图片/视频的 Content-Disposition 去掉（图片再去掉 "
            "Accept-Ranges，视频保留以便拖动进度），分享图下载的 attachment 不受影响。这样图片"
            "就能被离用户近的边缘节点缓存了。另外给所有 <img> 加了 loading=lazy（首屏外的图"
            "延迟加载），给数据库外键和日期列补了索引（数据量涨了不至于劣化）。"
        ),
        "summary_en": (
            "Another performance pass, measure-first this time. Breaking down the timing showed "
            "server processing is only ~0.18s — the bulk is network round-trips to Singapore — "
            "but I found that every image (book covers, character art, Douban covers) had "
            "x-cache: DYNAMIC: despite proper cache headers the CDN wasn't caching them, so each "
            "image round-tripped to the origin. Root cause: Flask's send_file adds "
            "Content-Disposition and Accept-Ranges to image responses, and Railway's CDN skips "
            "caching when those are present (the gzip-compressed CSS has neither, which is why it "
            "cached). Added an after_request hook that strips Content-Disposition from inline "
            "images/videos (and Accept-Ranges from images; videos keep it for seeking), leaving "
            "share-card attachment downloads untouched — so images now cache at the edge node "
            "near the viewer. Also added loading=lazy to every <img> (defers off-screen loads) "
            "and indexes on the DB foreign-key/date columns (keeps lookups from degrading as "
            "chapters/logs grow)."
        ),
        "image": None,
        "lines_changed": 73,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "更新日志分享图链接也加上版本号，避开旧缓存",
        "title_en": "Changelog share links now carry a version param too",
        "summary": (
            "点更新日志的「今天的更新分享图」，出来的是老的 24 号残缺图。查了下发现源站现在"
            "生成的其实是对的（25 号两条，完整），问题是这个分享链接是固定网址，在 24 号"
            "（加 max_age=0 之前）就被某个 CDN 边缘节点缓存了 30 天，缓存的是当时还没写完的"
            "24 号内容，正好被点到那个节点。之前给小说分享链接加过版本号绕开这个问题，更新"
            "日志的「最近 10 条」「今天」两个分享链接漏了，这次补上——每次打开页面都是新网址，"
            "直接绕开卡住的旧缓存。"
        ),
        "summary_en": (
            "Clicking the changelog's \"today's updates\" share image returned a stale, "
            "incomplete July-24 image. The origin actually generates the correct one now "
            "(two complete July-25 entries) — the problem was the fixed share URL had been "
            "cached on July 24 (before max_age=0 shipped) with that day's then-incomplete "
            "content, on an edge node the click happened to hit. The novel share links already "
            "got a version param for exactly this; the changelog's \"recent 10\" and \"today\" "
            "links were missed. Added it to both, so each page load gets a fresh URL that "
            "bypasses the stuck cache."
        ),
        "image": None,
        "lines_changed": 6,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "公开首页的更新日志只显示今天的",
        "title_en": "Public homepage now shows only today's changelog",
        "summary": (
            "未登录的公开首页原来会显示最近 5 天的更新日志、还能往下无限加载。改成只显示"
            "今天的更新，首页更清爽；如果今天还没更新，就退回显示最近一天的，避免首页空着。"
            "同时关掉了首页这块的「加载更多」。完整的更新日志（/changelog 页面）不受影响，"
            "仍然按天分页显示全部历史。"
        ),
        "summary_en": (
            "The logged-out public homepage used to show the last 5 days of changelog with "
            "infinite scroll. Changed it to show only today's updates for a cleaner landing "
            "page, falling back to the single most recent day when there's no update today so "
            "it never looks empty, and turned off the homepage's load-more. The full changelog "
            "page (/changelog) is unchanged and still paginates through all history."
        ),
        "image": None,
        "lines_changed": 11,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "公开首页去掉分享图按钮和站点状态卡片",
        "title_en": "Removed share buttons and live-stats card from the public homepage",
        "summary": (
            "把未登录公开首页上的「更新分享图」两个按钮和「站点实时概况」卡片都去掉了，"
            "首页更简洁。这俩在完整的 /changelog 页面还保留着（分享图、站点状态卡片都在），"
            "只是首页这个精简展示不再放它们。"
        ),
        "summary_en": (
            "Removed the two changelog share-image buttons and the live-stats card from the "
            "logged-out public homepage for a cleaner landing page. Both remain on the full "
            "/changelog page — only the trimmed homepage view drops them."
        ),
        "image": None,
        "lines_changed": 11,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "更新日志页面改成按天查看，加了日期选择器",
        "title_en": "Changelog page now views one day at a time with a date picker",
        "summary": (
            "完整的 /changelog 页面原来是一屏 5 天、往下无限加载。改成一次只显示一天，默认"
            "今天（今天还没更新就退回最近一天），标题下面加了个日期下拉框，可以选任意一个"
            "有更新的日期来查看那天的日志。下拉里只列出真正有更新的日期，不会选到空的。切换"
            "中英文、分享图这些都保留着。"
        ),
        "summary_en": (
            "The full /changelog page used to show 5 days at once with infinite scroll. Now it "
            "shows one day at a time, defaulting to today (falling back to the most recent day "
            "when today has no entries), with a date dropdown under the heading to jump to any "
            "day that has updates. The dropdown only lists days that actually have entries, so "
            "you can't land on an empty one. The language toggle and share buttons stay."
        ),
        "image": None,
        "lines_changed": 55,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "更新首页的技术架构图，补上这几轮新增的部分",
        "title_en": "Updated the homepage architecture diagram to match recent iterations",
        "summary": (
            "这么多轮迭代后，首页那张技术架构图有点跟不上了，补了两处：Flask 应用里加了一格"
            "「Pillow 图片 / ffmpeg 视频处理」（生成分享图、压缩上传图片、压缩视频抽封面帧），"
            "持久化存储里加了 novel_media/（小说封面/立绘/视频），tracker.db 的说明也从纯书影"
            "改成「书影/动态/小说 数据」。CDN 那行顺便改成「图片/静态资源边缘缓存」，对应这轮"
            "刚修好的图片 CDN 缓存。图下面的说明文字一并更新。"
        ),
        "summary_en": (
            "After all these iterations the homepage architecture diagram had drifted, so "
            "updated two spots: added a 'Pillow image / ffmpeg video processing' box to the "
            "Flask app (share-card generation, upload compression, video compression + poster "
            "frames), and added novel_media/ (novel covers/standees/videos) to persistent "
            "storage, with tracker.db relabeled from books/shows to 'books, moments & novels'. "
            "Also tweaked the CDN line to 'image/static-asset edge caching' to match the image "
            "CDN-caching fix from this pass, and refreshed the caption below."
        ),
        "image": None,
        "lines_changed": 26,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "登录页加了「返回公开主页」链接",
        "title_en": "Added a 'back to public homepage' link on the login page",
        "summary": (
            "登录页原来是个死胡同——不想登录就只能改地址栏。在登录按钮下面加了个「← 返回"
            "公开主页」的链接，点一下回到公开首页（那些不需要登录也能看的内容）。"
        ),
        "summary_en": (
            "The login page used to be a dead end — without logging in you had to edit the URL "
            "bar to leave. Added a '← back to public homepage' link under the login button that "
            "returns to the public landing page (the content viewable without logging in)."
        ),
        "image": None,
        "lines_changed": 16,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "参考书目改成搜索补全，不再把所有书都列出来",
        "title_en": "Reference books are now added via search autocomplete",
        "summary": (
            "之前挑参考书目是把所有已添加的书都列成勾选框，书一多就很长。改成搜索补全："
            "输入书名或作者，实时搜出匹配的书（已经加过的会自动排除，不重复出现），点一下"
            "就加进参考书目。已加的书还是显示在上面、带移除按钮。加了个 JSON 搜索接口，"
            "输入时带 250ms 防抖，只返回前 10 条。"
        ),
        "summary_en": (
            "Picking reference books used to list every book you'd added as checkboxes, which "
            "got long fast. Switched to search autocomplete: type a title or author, get live "
            "matches (already-added books are excluded so they don't show up twice), and click "
            "one to add it. Added books still show above with remove buttons. Backed by a small "
            "JSON search endpoint, 250ms debounce on input, top 10 results."
        ),
        "image": None,
        "lines_changed": 123,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "章节里选人物和视频也改成搜索添加",
        "title_en": "Chapter character/video selection is now search-based too",
        "summary": (
            "把参考书目那套搜索补全也用到了章节编辑里选出场人物和本章视频。跟参考书目不一样"
            "的是，章节的人物/视频要跟正文一起提交保存（新建章节时还没有章节 ID），所以做成"
            "搜索→点选→加成「已选标签」（客户端），随章节表单一起保存。人物的搜索结果和标签"
            "都带头像，选人物看脸更直观。人物/视频列表是单本小说范围、数量不多，所以搜索框点"
            "一下（空查询）就列出全部，输入再过滤，无标题的视频也能选到（显示成「视频 #编号」）。"
        ),
        "summary_en": (
            "Extended the reference-book search pattern to picking a chapter's characters and "
            "videos. Unlike references, a chapter's characters/videos are saved together with "
            "the chapter body (a new chapter has no id yet), so this is search → click → add as "
            "a client-side chip that submits with the chapter form. Character search results "
            "and chips show thumbnails so you can pick by face. Since each novel's character/"
            "video lists are small, focusing the box (empty query) lists everything and typing "
            "filters — untitled videos are still reachable, shown as '视频 #<id>'."
        ),
        "image": None,
        "lines_changed": 241,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "修复：今天新加的书没写进度/评论时，查看今天看不到",
        "title_en": "Fixed: books added today without a log didn't show in the day view",
        "summary": (
            "点开「今天」页面看不到刚加的书，因为 day_view 只查 logs 表（要有进度/评论记录"
            "才算），没记录任何进度的新书压根没查。这个坑首页 feed 早就处理过（build_feed "
            "里专门查了「没有 log 的新条目」），day_view 当时漏了。加了同样的查询：当天创建、"
            "还没有任何 log 的条目也会显示，标成「新添加 · 状态」。每日分享图用的是同一份"
            "数据，顺手一起修了，复用了进度卡片的样式（显示成「用时 0 分钟」，稍微有点多余但"
            "总比看不见强）。"
        ),
        "summary_en": (
            "Clicking into \"today\" didn't show books just added, because day_view only "
            "queried the logs table (which requires a progress/comment entry) — items with no "
            "log yet were never fetched. The homepage feed already handled this exact gap "
            "(build_feed has a dedicated query for \"new items with no log\"); day_view had "
            "just never gotten the same treatment. Added the same query: items created that "
            "day with no log yet now show, labeled \"newly added · <status>\". The daily share "
            "image pulls from the same data, so fixed that too, reusing the log-card layout "
            "(shows \"0 minutes\", a bit redundant but better than invisible)."
        ),
        "image": None,
        "lines_changed": 51,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "参考书目的封面图缩小了一些",
        "title_en": "Reference book covers are a bit smaller now",
        "summary": (
            "参考书目跟小说列表页共用同一套网格样式，之前封面跟小说封面一样大。加了个"
            "reference-grid 修饰类，只缩小参考书目这里的卡片（最小宽度从 180px 降到 110px），"
            "小说列表页和其他用到同一套样式的地方不受影响。"
        ),
        "summary_en": (
            "Reference book cards shared the same grid styling as the novel list, so covers "
            "were as large as novel covers. Added a reference-grid modifier that only shrinks "
            "cards in the reference-bibliography section (min-width 180px down to 110px); the "
            "novels list and everything else using the shared grid is untouched."
        ),
        "image": None,
        "lines_changed": 15,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "没上传封面时，占位图标不再孤零零飘在空色块里",
        "title_en": "Fixed the cover placeholder looking bare and unbalanced",
        "summary": (
            "反馈说小说详情页的封面看着不协调——其实是没上传封面时的占位图标（一个小 emoji "
            "飘在一大块纯色背景里），旁边配上一段很长的简介，显得很空。改成一个带阴影的白色"
            "圆形徽章托着图标，外面的色块加了一圈细边框。这个占位样式是书影条目和小说共用的，"
            "两边都顺带好看了一些。"
        ),
        "summary_en": (
            "Reported the novel detail page's cover looking mismatched — turned out to be the "
            "no-cover-uploaded placeholder (a bare emoji floating in a flat color block), which "
            "looked especially empty next to a long summary. Changed it to a small white "
            "circular badge with a soft shadow holding the icon, plus a subtle border around the "
            "cover box. This placeholder is shared with book/show items, so both got the same "
            "polish."
        ),
        "image": None,
        "lines_changed": 10,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "分享图重新设计：封面放大，去掉简介和人物，参考书目改成手动挑选",
        "title_en": "Redesigned the share image: bigger cover, no summary/characters, curated references",
        "summary": (
            "小说分享图做了四处调整：封面从占约一半宽度放大到接近满宽；简介和人物角色两个"
            "板块整个去掉了；参考书目从「有啥放啥」改成手动挑——每本参考书旁边加了个「在"
            "分享图中显示」的勾选框，勾哪几本就出现哪几本，编辑页上有个「已选 N 本」的实时"
            "提示，超过 10 本时分享图只取前 10 本。给 novel_references 表加了 in_share 字段"
            "记这个状态。"
        ),
        "summary_en": (
            "Four changes to the novel share image: the cover grew from about half the card "
            "width to nearly full width; the summary and character sections were dropped "
            "entirely; and reference books switched from \"show everything\" to a manual pick — "
            "each reference now has an \"in share image\" checkbox, and only the checked ones "
            "appear, with a live \"N selected\" hint on the edit page (capped at 10 in the "
            "actual image). Added an in_share column on novel_references to track the flag."
        ),
        "image": None,
        "lines_changed": 51,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "修复：小说分享图生成慢——豆瓣封面图现在也走磁盘缓存",
        "title_en": "Fixed slow novel share-image generation by disk-caching reference covers",
        "summary": (
            "小说分享图最多带 10 本参考书，之前每次生成都要挨个现抓豆瓣封面，一本一本"
            "顺序请求，慢的时候单张图要等好几秒。其实网站里 /cover-proxy 早就有一套按"
            "网址哈希存本地的封面缓存，只是分享图生成用的是另一段独立代码，没接上这套"
            "缓存。现在两边共用同一个缓存目录：命中缓存直接读本地文件，本地测了一下，"
            "首次现抓要 6 秒，命中缓存后只要 0.015 秒。"
        ),
        "summary_en": (
            "Novel share images can include up to 10 reference books, and each one was "
            "fetched live from Douban on every single generation — sequentially, so a slow "
            "run could take several seconds. The site already had a disk cache for cover "
            "images keyed by URL hash (used by /cover-proxy), but the share-card code was a "
            "separate path that never used it. Now both share the same cache directory: a "
            "cache hit reads straight from disk. Measured locally: 6s on a cold fetch vs "
            "0.015s once cached."
        ),
        "image": None,
        "lines_changed": 18,
        "estimated": False,
    },
    {
        "date": "2026-07-25",
        "title": "更新日志页面加了搜索框",
        "title_en": "Added a search box to the changelog page",
        "summary": (
            "更新日志之前只能按日期一天天翻，现在加了个搜索框，按标题和正文（中英文都会"
            "搜）匹配，结果按日期分组显示，跟日期选择互斥——一搜索就不再受选中日期限制，"
            "清空搜索框可以一键回到按日期查看。"
        ),
        "summary_en": (
            "The changelog could only be browsed one day at a time before. Added a search "
            "box that matches title and body text (both languages), with results grouped by "
            "date and no longer limited to the selected day; clearing the box goes back to "
            "the date view."
        ),
        "image": None,
        "lines_changed": 65,
        "estimated": False,
    },
    {
        "date": "2026-07-26",
        "title": "修复：小说章节正文在手机上仍然能长按复制",
        "title_en": "Fixed novel chapters still being copyable on mobile via long-press",
        "summary": (
            "之前防复制只加了 user-select: none，桌面端够用，但手机浏览器（尤其是 iOS "
            "Safari）长按弹出的「复制」菜单是靠一个专门的 -webkit-touch-callout 属性关"
            "掉的，之前漏加了。补上这个属性，并且把选中保护套用到章节正文里的所有子元素"
            "上，另外 JS 那边也加了 selectstart / dragstart 兜底。"
        ),
        "summary_en": (
            "The previous copy-protection only set user-select: none, which is enough on "
            "desktop but not mobile — the long-press \"Copy\" callout on mobile browsers "
            "(especially iOS Safari) is controlled by a separate -webkit-touch-callout "
            "property that was missing. Added it, applied the selection lock to every child "
            "element inside the chapter body, and added selectstart/dragstart as a JS "
            "fallback."
        ),
        "image": None,
        "lines_changed": 8,
        "estimated": False,
    },
    {
        "date": "2026-07-26",
        "title": "小说加了导出 Word / PDF，全文一次导出，需要登录",
        "title_en": "Added Word/PDF export for the whole novel (login required)",
        "summary": (
            "小说详情页新增「导出 Word」「导出 PDF」两个按钮，把简介和所有章节按顺序打"
            "包成一份 .docx 或 .pdf，章节之间自动分页。两个导出接口都没加进公开路由白名"
            "单，所以跟其他创作类功能一样，必须先登录才能用。Word 用 python-docx 生成，"
            "PDF 用 reportlab，中文字体复用了分享图那套 Noto CJK 字体查找逻辑。"
        ),
        "summary_en": (
            "Added \"Export Word\" and \"Export PDF\" buttons on the novel detail page — "
            "each bundles the summary and every chapter, in order, into a single .docx or "
            ".pdf with a page break between chapters. Neither export route is in the public "
            "route allowlist, so like the rest of the authoring features, they require "
            "login. Word generation uses python-docx, PDF uses reportlab, and both reuse "
            "the same Noto CJK font lookup the share-card generator already had."
        ),
        "image": None,
        "lines_changed": 168,
        "estimated": False,
    },
    {
        "date": "2026-07-26",
        "title": "修复：小说导出的 PDF 中文乱码",
        "title_en": "Fixed garbled Chinese text in the novel PDF export",
        "summary": (
            "PDF 导出本地测过没问题，但线上生成的 PDF 中文是乱码。原因是 PDF 那边用的字"
            "体加载方式跟分享图的 Pillow 不一样：分享图用 Pillow/FreeType 读字体没问题，"
            "但 PDF 库 reportlab 自己解析字体文件的逻辑对 Linux 上那个 Noto Sans CJK 字"
            "体文件（虽然后缀是 .ttc，内部其实是 CFF 轮廓）支持得不好，解析错了字形对应"
            "关系，所以显示出来是乱码而不是报错——本地测试用的是 macOS 系统字体，没测到"
            "线上这条路径，所以之前没发现。改成用 reportlab 自带的中文字体支持（不用解"
            "析任何字体文件，直接引用阅读器自带的中文字体），彻底绕开这个解析问题。"
        ),
        "summary_en": (
            "The PDF export tested fine locally, but the Chinese text came out garbled once "
            "generated in production. The PDF path used a different font-loading route than "
            "the share-card images: Pillow/FreeType reads the Linux CJK font file just fine, "
            "but reportlab's own font parser doesn't handle that particular Noto Sans CJK "
            "file well (it's a .ttc by extension but CFF-outlined internally), so it mapped "
            "character codes to the wrong glyphs instead of erroring out — and the local test "
            "used a macOS system font, so it never exercised that code path. Switched to "
            "reportlab's built-in CJK font support instead, which doesn't parse any font "
            "file at all, sidestepping the bug entirely."
        ),
        "image": None,
        "lines_changed": 10,
        "estimated": False,
    },
    {
        "date": "2026-07-26",
        "title": "修复：小说章节标题太长时显示不全",
        "title_en": "Fixed long chapter titles getting cut off",
        "summary": (
            "小说目录是一排 3 个的网格排版，之前标题超长会被单行省略号截断，看不到完整"
            "标题。改成允许换行显示完整标题，卡片跟着变高；顺手把旁边的「删除」按钮也"
            "固定宽度，不会被挤到跟着换行。"
        ),
        "summary_en": (
            "The chapter list uses a 3-column grid, and overly long titles were being cut "
            "off with a single-line ellipsis. Switched to letting titles wrap and grow the "
            "card instead, and fixed the width of the adjacent \"删除\" (delete) button so it "
            "no longer gets squeezed into wrapping too."
        ),
        "image": None,
        "lines_changed": 8,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "小说章节加了分享图，正文全文都会显示",
        "title_en": "Added per-chapter share images with the full chapter text",
        "summary": (
            "章节阅读页新增「生成本章分享图」，把整章正文原样生成一张图，不摘要不截断——"
            "图片高度是按内容自动算的，短章节图短，长章节图长（小红书常见的那种「长"
            "图」）。跟小说编辑/导出功能一样需要登录才能用，按钮和链接对未登录访客都不"
            "显示；链接也带了版本号避开 CDN 缓存卡住的老问题。"
        ),
        "summary_en": (
            "Added a \"Generate chapter share image\" button on the chapter reading page — "
            "it renders the entire chapter text as-is into one image, no summarizing or "
            "truncation. The image height is computed from the actual content, so short "
            "chapters get a short image and long ones get a tall one (the common \"long "
            "screenshot\" format). Requires login, like the novel authoring/export features — "
            "the button and link are hidden from anonymous visitors. The link is also "
            "versioned to avoid the CDN-staleness issue from earlier."
        ),
        "image": None,
        "lines_changed": 98,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "小说和章节都可以单独上锁，未登录看不了",
        "title_en": "Added per-chapter and per-novel locking for chapter content",
        "summary": (
            "小说和章节原本都是公开可读的。现在编辑页多了一个「锁定」勾选框：锁一章，"
            "这一章未登录就看不了（会跳去登录页，登录后自动回来）；锁整本小说，底下所"
            "有章节都看不了，不用一章一章去锁。目录里锁定的章节会带个 🔒 图标提示，小"
            "说详情页也会标出「已锁定」。没配置登录密码的话锁定不生效——毕竟锁了也没法"
            "登录解锁。"
        ),
        "summary_en": (
            "Novels and chapters used to be fully public. Added a \"lock\" checkbox on both "
            "the novel and chapter edit forms: lock a chapter and anonymous visitors can't "
            "read it (redirected to login, then bounced back after signing in); lock the "
            "whole novel and every chapter under it is blocked, without locking each one "
            "individually. Locked chapters show a 🔒 badge in the table of contents, and a "
            "locked novel is flagged on its detail page. Locking is a no-op when no login "
            "password is configured, since there'd be no way to unlock it."
        ),
        "image": None,
        "lines_changed": 65,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "锁定的章节改成显示前几段预览，不再直接跳登录页",
        "title_en": "Locked chapters now show a text preview instead of redirecting to login",
        "summary": (
            "之前锁定的章节未登录访问会直接跳转登录页，正文一个字都看不到。现在改成正"
            "常打开章节页，显示正文前 3 段（带渐隐效果），底下有个「本章已锁定」的提示"
            "和登录按钮，登录后回到本章看剩下的内容。预览状态下也不会剧透本章的出场人"
            "物立绘和视频。"
        ),
        "summary_en": (
            "Locked chapters used to redirect straight to the login page with zero text "
            "visible. Now the chapter page opens normally and shows the first 3 paragraphs "
            "(with a fade-out effect), followed by a \"this chapter is locked\" prompt and a "
            "login button that returns to the chapter afterward. The preview also holds back "
            "character standees and videos tied to the rest of the chapter, so it doesn't "
            "spoil anything beyond the visible text."
        ),
        "image": None,
        "lines_changed": 85,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "小说编辑页可以批量锁定/解锁章节了",
        "title_en": "Added bulk lock/unlock for chapters in the novel editor",
        "summary": (
            "之前锁章节要点进每一章的编辑页勾一次，章节多了很麻烦。现在小说编辑页的章"
            "节列表每一行前面加了个勾选框，勾几章、点一下「锁定选中章节」或「解锁选中"
            "章节」，就一次批量改完，不用逐章打开。"
        ),
        "summary_en": (
            "Locking chapters used to mean opening each chapter's edit page one at a time — "
            "tedious once a novel has more than a few. Added a checkbox next to each chapter "
            "in the novel editor's chapter list, plus \"lock selected\" / \"unlock selected\" "
            "buttons that apply to all checked chapters in one request."
        ),
        "image": None,
        "lines_changed": 45,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "多用户系统第一步：数据库打好底子，网站行为不变",
        "title_en": "Multi-user groundwork (step 1 of a phased rollout): schema only, no behavior change",
        "summary": (
            "打算把网站从单人用的改成能支持多个独立账号，每人数据互相隔离，后台还能"
            "一键开关是否允许自助注册——但这个改动牵一发动全身，所以拆成好几步来上，"
            "先从最不冒险的一步开始：新建 users（账号）和 app_settings（站点设置）两"
            "张表，给书影/动态/小说相关的 7 张表都加上 user_id 字段，并且自动建一个"
            "admin 账号（密码沿用现在的登录密码），把所有已有数据都归到这个账号名"
            "下。这一步网站的登录方式、页面显示完全没变——纯粹是把底子打好，后面几步"
            "才会真正开始用上这些字段。"
        ),
        "summary_en": (
            "Planning to turn this from a single-owner site into one that supports several "
            "independent accounts, each with fully private data, with an admin toggle for "
            "public self-registration — but that's a big, cross-cutting change, so it's "
            "landing in phases. This is the safest first step: new users and app_settings "
            "tables, a user_id column added to the 7 tables holding personal content, and a "
            "bootstrap admin account (password carried over from the current login password) "
            "that all existing data gets attributed to. Nothing about how the site works or "
            "looks changes yet — this just lays the groundwork the later steps build on."
        ),
        "image": None,
        "lines_changed": 53,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "多用户系统第二步：登录方式换成账号+密码",
        "title_en": "Multi-user step 2: login switched from shared password to username + password",
        "summary": (
            "上一步只是把数据库底子打好，这一步开始真正把登录机制换掉：以前是一个共享"
            "密码，现在是查 users 表里的真实账号（用户名+密码），登录页也加了用户名输"
            "入框。因为目前 users 表里只有上一步自动建的那个 admin 账号（密码沿用原来"
            "的登录密码），所以从使用体验上几乎感觉不到变化——用 admin 账号照常登录就"
            "行，导航栏现在会显示当前登录的用户名。小说的「锁定」章节逻辑也跟着换成新"
            "的登录判断，行为不变。"
        ),
        "summary_en": (
            "The previous step only laid the database groundwork; this one actually swaps "
            "the login mechanism — from a single shared password to a real account lookup "
            "(username + password) against the users table, with a username field added to "
            "the login page. Since the users table currently holds only the one admin "
            "account created by the last step's bootstrap (password carried over from the "
            "old shared password), this is nearly invisible day to day — log in as admin as "
            "usual, and the nav bar now shows the signed-in username. The novel \"lock\" "
            "check was updated to the new session model too, with no change in behavior."
        ),
        "image": None,
        "lines_changed": 42,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "小说加了字数统计和更新时间",
        "title_en": "Added word counts and update timestamps to novels",
        "summary": (
            "小说列表、小说详情页、编辑页、章节阅读页现在都会显示字数：小说列表和详情"
            "页显示整本小说的总字数，目录里每章也单独标了这一章的字数，另外都带上了"
            "最后更新时间（章节改内容会更新这个时间）。字数统计不含空白字符，用"
            "SQLite 的 LENGTH() 直接在数据库里算，没有额外拉取正文内容。"
        ),
        "summary_en": (
            "The novels list, novel detail page, editor, and chapter reading page all now "
            "show word counts — total word count for the whole novel on the list/detail "
            "pages, and each chapter's own count next to it in the table of contents — plus "
            "a last-updated date everywhere (bumped whenever a chapter's content changes). "
            "Counts are computed with SQLite's LENGTH() directly in the query, so list views "
            "don't need to fetch the full chapter text just to size it up."
        ),
        "image": None,
        "lines_changed": 46,
        "estimated": False,
    },
    {
        "date": "2026-07-27",
        "title": "修复：批量锁定/解锁按钮文字看不清",
        "title_en": "Fixed low-contrast text on the bulk lock/unlock buttons",
        "summary": (
            "「锁定选中章节」「解锁选中章节」这两个按钮之前套了 .btn-link 这个类，"
            "本意是想要淡一点的文字链接样式，但因为它俩本质是 <button>，网站默认的按"
            "钮样式会给个橙色底，.btn-link 只改了文字颜色（改成了灰色），最后就是灰"
            "字配橙底，糊成一片。去掉这个类，让它们走默认的白字橙底按钮样式，跟「保"
            "存」按钮一个风格，看得清了。"
        ),
        "summary_en": (
            "The \"lock selected\" / \"unlock selected\" buttons had a .btn-link class on "
            "them, meant for a plain muted-text-link look — but since they're actual "
            "<button> elements, the site's default button style still gave them a solid "
            "orange background, and .btn-link only overrode the text color to gray, leaving "
            "low-contrast gray text on orange. Removed the class so they fall back to the "
            "default white-on-orange button style, matching \"保存\" (Save) elsewhere."
        ),
        "image": None,
        "lines_changed": 2,
        "estimated": False,
    },
    {
        "date": "2026-07-31",
        "title": "小说章节页加了朗读功能",
        "title_en": "Added a read-aloud feature for novel chapters",
        "summary": (
            "章节阅读页新增「朗读本章」，用的是浏览器自带的语音合成（Web Speech "
            "API），不用服务器生成音频、不用接第三方 TTS 接口，零成本。可以暂停/继"
            "续/停止、调语速（0.75x–1.5x），还有个「自动连播下一章」——念完这一章自"
            "动跳到下一章接着念。锁定章节朗读的也是当前显示的预览段落，不会把还没解"
            "锁的内容读出来。缺点是音色和是否支持中文朗读要看访客自己浏览器/系统装"
            "了什么语音引擎，网站这边控制不了。"
        ),
        "summary_en": (
            "Added a \"read chapter aloud\" button on the chapter reading page, using the "
            "browser's built-in Web Speech API — no server-side audio generation, no "
            "third-party TTS integration, zero cost. Supports pause/resume/stop, an "
            "adjustable rate (0.75x–1.5x), and an \"auto-continue to next chapter\" option "
            "that keeps reading straight through. On a locked chapter it only reads the "
            "visible preview paragraphs, never the hidden rest. The tradeoff: voice quality "
            "and Chinese-language support depend entirely on whatever speech engine the "
            "visitor's own browser/OS has installed — nothing the site can control."
        ),
        "image": None,
        "lines_changed": 133,
        "estimated": False,
    },
    {
        "date": "2026-07-31",
        "title": "修复：章节页朗读按钮太挤、「停止」看不清",
        "title_en": "Fixed the read-aloud controls being cramped, and the Stop button being unreadable",
        "summary": (
            "朗读功能上线后发现两个问题：分享图按钮和朗读控件两排贴在一起没有间距；"
            "「停止」按钮又是那个熟悉的坑——套了 .btn-link 但本质是 <button>，灰字配"
            "橙底看不清（跟之前批量锁定按钮一模一样的 bug，这次是新加的朗读功能里漏"
            "改了）。给两排之间加了间距，「停止」改成描边的次要按钮样式，跟主按钮"
            "「朗读本章」分得清楚。"
        ),
        "summary_en": (
            "Two issues surfaced after the read-aloud feature shipped: the share-image "
            "button row and the read-aloud controls row sat with zero gap between them, "
            "and the Stop button hit the exact same bug as the bulk lock buttons before it "
            "— a .btn-link class on a real <button>, giving gray text on the default solid "
            "orange background. Added spacing between the two rows and switched Stop to an "
            "outlined secondary style, visually distinct from the primary Play button."
        ),
        "image": None,
        "lines_changed": 8,
        "estimated": False,
    },
    {
        "date": "2026-07-31",
        "title": "修复：朗读功能点「停止」不管用",
        "title_en": "Fixed the read-aloud Stop button not actually stopping",
        "summary": (
            "点朗读本章再点停止，声音不停，一直往下念。原因是 speechSynthesis.cancel"
            "() 会触发当前这段话的 onend 事件——跟正常念完一段是同一个事件，之前的代"
            "码收到 onend 就无脑接着念下一段，于是「停止」实际上变成了「跳到下一"
            "段」。改成给每次朗读发一个序号，点停止时先把序号加一，onend 触发时先核"
            "对序号对不对，对不上（说明是被取消的）就不再继续。用模拟的语音引擎重现"
            "了这个 race condition 并验证修好了。"
        ),
        "summary_en": (
            "Clicking Stop didn't stop the reading — it just kept going. Root cause: "
            "speechSynthesis.cancel() fires the current utterance's onend event, the exact "
            "same event as a normal paragraph finishing, and the old handler always "
            "advanced to the next paragraph on onend — so Stop was effectively acting as "
            "\"skip to next paragraph\" instead of stopping. Fixed by tagging each utterance "
            "with a session token that gets bumped before cancelling; the stale onend "
            "checks the token and bails instead of continuing. Reproduced the exact race "
            "condition with a mocked speech engine and confirmed the fix."
        ),
        "image": None,
        "lines_changed": 15,
        "estimated": False,
    },
    {
        "date": "2026-07-31",
        "title": "朗读功能改成需要登录",
        "title_en": "The read-aloud feature now requires login",
        "summary": (
            "章节朗读控件之前对所有人可见，跟章节分享图之前的情况一样。现在改成跟"
            "「生成本章分享图」放在同一个登录判断里，只有登录后才会显示朗读按钮，未"
            "登录访客看不到也用不了。"
        ),
        "summary_en": (
            "The read-aloud controls were visible to everyone, same as the chapter share "
            "image was before. Moved them into the same login check as \"Generate chapter "
            "share image,\" so the read-aloud button now only shows up when logged in."
        ),
        "image": None,
        "lines_changed": 3,
        "estimated": False,
    },
    {
        "date": "2026-07-31",
        "title": "修复：朗读点暂停后过一会儿会自己继续念",
        "title_en": "Fixed paused read-aloud spontaneously resuming on its own",
        "summary": (
            "点暂停之后放着不管，过一会儿它会自己接着念下去。这是浏览器（主要是"
            "Chrome）speechSynthesis.pause() 一个已知的老问题：暂停状态放久了会被浏"
            "览器自己悄悄放弃，播放不打招呼就恢复了。之前的代码单纯信任浏览器的暂停"
            "状态，浏览器一旦擅自恢复，代码就跟着当成正常念完接着往下走。改成不再依"
            "赖浏览器的 pause()/resume()，暂停时直接取消当前这段的朗读（同时靠序号"
            "机制防止误触发下一段），继续时从暂停的那一段重新念一遍。用模拟的语音引"
            "擎复现了这个「浏览器擅自恢复」的场景并验证修好了。"
        ),
        "summary_en": (
            "Leaving the reader paused for a while, it would start reading again on its "
            "own. This is a known long-standing browser bug (mainly Chrome) in "
            "speechSynthesis.pause() — a paused utterance can get silently abandoned by the "
            "browser and resume playback without notice. The old code trusted the "
            "browser's pause state; once the browser quietly resumed, the code treated it "
            "as a normal paragraph finish and kept going. Fixed by no longer relying on "
            "pause()/resume() at all — pausing now fully cancels the current paragraph "
            "(guarded by the same session-token mechanism so it can't misfire into the next "
            "one), and resuming re-speaks that paragraph from the start. Reproduced the "
            "\"browser resumes on its own\" scenario with a mocked speech engine and "
            "confirmed the fix."
        ),
        "image": None,
        "lines_changed": 12,
        "estimated": False,
    },
    {
        "date": "2026-08-02",
        "title": "添加书、添加剧、记录动态合并成一个入口",
        "title_en": "Merged add-book/add-show/record-moment into one entry point",
        "summary": (
            "导航栏原来有三个添加相关的链接（添加书、添加剧、记录动态），现在合并成"
            "一个「+ 添加」。新页面顶部有个类型下拉框，六个类型（书/剧/股票/运动/照"
            "片/想法）都在里面，选哪个就切换显示对应的表单（书影表单还带着豆瓣自动"
            "填充），提交到的还是原来各自的接口，没改后端逻辑，纯粹是前端合并入口、"
            "少点一次。"
        ),
        "summary_en": (
            "The nav bar used to have three separate \"add\" links (add book, add show, "
            "record moment) — merged into a single \"+ Add\" entry. The new page has one "
            "type dropdown covering all six types (book/show/stock/exercise/photo/thought); "
            "picking one switches which form is shown (the book/show form keeps its Douban "
            "auto-fill). Each form still posts to its existing backend route unchanged — "
            "this is purely a front-end consolidation, one less click to get anywhere."
        ),
        "image": None,
        "lines_changed": 197,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "小说章节可以归入卷了，每卷可以起名字",
        "title_en": "Novel chapters can now be grouped into named volumes",
        "summary": (
            "新加了个 novel_volumes 表，一本小说下面可以建好几卷，每卷有名字（比如"
            "「第一卷 风起」）。章节编辑页多了个「所属卷」下拉框，选哪卷就归到哪卷，"
            "不选就是未分卷。小说编辑页新增了「分卷」管理区（新增/删除卷），目录和编"
            "辑页的章节列表都按卷分段显示，带分割线；Word/PDF 导出也会在卷交界处插入"
            "卷标题。删除一卷不会删掉里面的章节，只是把它们变回未分卷。没建过卷的小"
            "说完全看不出变化——只有用到分卷功能才会显示卷标题。"
        ),
        "summary_en": (
            "Added a novel_volumes table — a novel can now have several volumes, each with "
            "a name (e.g. \"Volume 1: The Wind Rises\"). The chapter editor got a \"volume\" "
            "dropdown to assign a chapter to one (or leave it unassigned); the novel editor "
            "got a volume management section (add/delete). Both the public table of "
            "contents and the editor's chapter list now render in volume-grouped sections "
            "with dividers, and the Word/PDF export inserts a volume heading wherever the "
            "volume changes. Deleting a volume doesn't delete its chapters, just unassigns "
            "them. Novels that never use volumes look completely unchanged — the heading "
            "only appears once at least one volume exists."
        ),
        "image": None,
        "lines_changed": 236,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "小说章节可以批量移卷了",
        "title_en": "Added bulk-move-to-volume for novel chapters",
        "summary": (
            "上一条加了分卷功能后，一章一章打开去选所属卷太麻烦。现在跟批量锁定用同"
            "一套勾选框：勾几章，在旁边的下拉框选目标卷（或者选「移到未分卷」），点"
            "「批量移卷」一次性挪过去。因为勾选框只能绑定一个表单，批量移卷这边是提"
            "交前用 JS 把勾中的章节 id 现塞进表单里，跟批量锁定共用同一批勾选框。"
        ),
        "summary_en": (
            "After the previous volumes feature landed, assigning a volume meant opening "
            "each chapter individually — tedious for more than a couple. Reused the same "
            "checkboxes as bulk lock/unlock: check some chapters, pick a target volume (or "
            "\"move to unassigned\") from a dropdown, click \"bulk move.\" Since a checkbox "
            "can only be form-associated with one form, the bulk-move form collects the "
            "checked chapter ids itself via JS right before submitting, sharing the same "
            "checkbox set as the lock/unlock action."
        ),
        "image": None,
        "lines_changed": 57,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "小说分享图上也显示卷和总字数了",
        "title_en": "Novel share images now show volumes and total word count",
        "summary": (
            "小说的一键分享图之前只有章节目录，没有字数、也不分卷。现在封面下面的状"
            "态标签旁边加了「共 X 字」，章节目录部分也跟着网页版一样按卷分组显示（带"
            "卷名的小标题），没分卷的章节归到「未分卷」下面。没建过卷的小说分享图不"
            "受影响，还是原来那样。"
        ),
        "summary_en": (
            "The novel share image only ever showed the chapter list — no word count, no "
            "volume grouping. Added a \"共 X 字\" pill next to the status pill below the "
            "cover, and the chapter list now groups by volume the same way the web page "
            "does, with a small heading per volume (unassigned chapters fall under \"未分"
            "卷\"). Share images for novels with no volumes look exactly as before."
        ),
        "image": None,
        "lines_changed": 69,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "多用户系统第三步：书影/动态数据按账号隔离",
        "title_en": "Multi-user step 3: personal tracker data scoped per account",
        "summary": (
            "上一步把登录换成了真账号，但数据库里书影/动态数据其实还是不管谁登录都"
            "能看全部、改全部。这一步把首页、搜索、打卡热力图、条目详情/编辑/删除/"
            "记进度、按天查看、动态记录，全部加上了按账号过滤——每个账号只能看到、"
            "改到自己的数据，猜 URL 直接访问别人的条目会得到 404。顺手修了一个刚写"
            "完时冒出来的 bug：g.user 之前只在渲染模板时才会被填充，路由函数自己想提"
            "前用就会报 AttributeError，现在挪到登录检查那一步统一先填好。新建了第二"
            "个测试账号，实测了条目、进度、动态、按天查看、搜索这几个地方的隔离，都"
            "符合预期。"
        ),
        "summary_en": (
            "The previous step swapped in real accounts, but the actual book/show/moment "
            "data was still visible and editable by any logged-in account. This step adds "
            "an ownership filter to the homepage feed, search, the activity heatmap, item "
            "detail/edit/delete/progress-logging, the day view, and moment recording — each "
            "account now only sees and can modify its own data, and guessing another "
            "user's item URL returns a 404. Also fixed a bug that surfaced while writing "
            "this: g.user was only populated when a template happened to render, so a "
            "route reading it earlier hit an AttributeError -- moved the population into "
            "the login check so it's always set before any view function runs. Created a "
            "second test account and verified isolation across items, progress logs, "
            "moments, the day view, and search."
        ),
        "image": None,
        "lines_changed": 72,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "多用户系统第四步：小说也按账号隔离，锁定改成只有作者能看",
        "title_en": "Multi-user step 4: novels scoped per account, locked content is now author-only",
        "summary": (
            "上一步把书影/动态数据隔离了，这一步轮到小说：新建小说、编辑、删除、加"
            "章节/分卷/人物/视频/参考书目，这些创作类操作现在都要求是小说的作者本人"
            "才能做，猜 URL 也进不去别人的小说编辑页。小说本身的公开阅读（目录、章"
            "节正文、分享图）完全没变，谁都能看——只有「锁定」这个功能的含义变了："
            "以前是「随便哪个账号登录了就能看」，现在是「只有这本小说的作者本人（或"
            "管理员）能看」。用两个测试账号加一个临时的管理员账号，把「作者本人看到"
            "全文、别的账号只看预览、管理员绕过锁定」这几种情况都测了一遍。"
        ),
        "summary_en": (
            "Following the previous step's personal-tracker isolation, novels are now "
            "scoped too: creating, editing, deleting a novel, and adding chapters/volumes/"
            "characters/videos/reference books all require being the novel's own author — "
            "guessing another account's novel edit URL now 404s. Public reading (the table "
            "of contents, chapter text, share images) is completely unchanged and still "
            "open to everyone; only the meaning of \"locked\" changed, from \"any logged-in "
            "account\" to \"the novel's own author (or an admin)\". Verified all four cases "
            "with two test accounts plus a temporary admin flag: the owner sees full "
            "content, another account only sees the preview, and an admin bypasses the "
            "lock on someone else's novel."
        ),
        "image": None,
        "lines_changed": 80,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "多用户系统第五步：后台加了账号管理页面",
        "title_en": "Multi-user step 5: added an admin account management page",
        "summary": (
            "新加了 /admin/users，只有管理员账号能进（普通账号访问会看到 404，压根"
            "不知道这个页面存在）。上面能看到所有账号的列表，能手动加新账号（可以顺"
            "手勾成管理员），还有一个「允许自助注册」的开关——先加在这儿备用，默认"
            "关闭，真正的 /register 注册页面还没做，等这个做完开关才有实际用处。导"
            "航栏里「🛡️ 账号管理」这个入口也只有管理员账号才看得到。"
        ),
        "summary_en": (
            "Added /admin/users, reachable only by admin accounts (a non-admin gets a "
            "plain 404 — the page doesn't even hint that it exists). It lists every "
            "account, has a form to add a new one (with an optional \"make admin\" "
            "checkbox), and an \"allow self-registration\" toggle — wired up now for later, "
            "off by default; the actual /register page doesn't exist yet, so the toggle "
            "has no real effect until that's built. The \"🛡️ Account Management\" nav link "
            "is likewise only visible to admin accounts."
        ),
        "image": None,
        "lines_changed": 67,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "多用户系统收尾：开放自助注册",
        "title_en": "Multi-user rollout finished: self-registration is live",
        "summary": (
            "多用户改造的最后一步：加了 /register 页面。开关关着的时候这个页面直接"
            "404，跟不存在一样；管理员在账号管理页打开开关之后，登录页会多一条「还没"
            "有账号？去注册」的链接，任何人都能自己开一个账号（新账号不会是管理员），"
            "注册完自动登录。密码最少 6 位，用户名重复会被拒绝。修了一个写的时候手滑"
            "的 bug：把一个普通函数插到了 @app.route 装饰器和它要修饰的 login() 函数"
            "中间，导致装饰器实际上修饰到了别的函数，/login 路由直接注册失败——测试"
            "的时候一堆请求跟着报错才发现。到这里，多用户系统五步全部做完了。"
        ),
        "summary_en": (
            "The final step of the multi-user rollout: added a /register page. With the "
            "toggle off it's a plain 404, indistinguishable from not existing; once an "
            "admin flips it on from the account management page, the login page grows a "
            "\"no account yet? register\" link, and anyone can create their own account "
            "(never as admin), auto-logged-in right after. Minimum 6-character password, "
            "duplicate usernames rejected. Fixed a slip made while writing this: an "
            "ordinary helper function ended up sandwiched between the @app.route decorator "
            "and the login() function it was meant to decorate, so the decorator silently "
            "attached to the wrong function and the /login route never got registered at "
            "all -- a wave of test failures caught it immediately. That closes out all five "
            "steps of the multi-user rollout."
        ),
        "image": None,
        "lines_changed": 54,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "管理员后台加了「下载完整备份」",
        "title_en": "Added a full-backup download to the admin page",
        "summary": (
            "账号管理页新加一块「数据备份」，管理员点一下就能把网站数据库文件加所有"
            "上传/生成的图片视频打包成一个 zip 下载下来，不区分账号，是最完整的一份"
            "快照。非管理员访问这个链接照样是 404。写的时候踩了一个坑：一开始直接把"
            "整个 DATA_DIR 目录打包，本地开发环境因为没设 DATA_DIR 环境变量，这个目"
            "录其实就是整个项目文件夹——测试的时候打出来的 zip 里混进了 db.py、"
            "Dockerfile 这些源代码文件。线上环境因为 Dockerfile 里明确写了 DATA_DIR=/"
            "data，本来就不会有这个问题，但还是改成只打包数据库文件加三个上传目录，"
            "不管 DATA_DIR 指到哪儿都不会打包错东西。"
        ),
        "summary_en": (
            "Added a \"Data Backup\" section to the account management page: one click "
            "and an admin gets a zip of the database file plus every uploaded/generated "
            "image and video, not scoped to any one account -- the most complete snapshot "
            "available. Non-admins still get a 404 on the link. Hit a snag while building "
            "it: the first version just zipped everything under DATA_DIR, and since local "
            "dev never sets that environment variable, it defaults to the whole project "
            "folder -- testing turned up db.py, Dockerfile and other source files mixed "
            "into the zip. Production was never actually at risk, since the Dockerfile "
            "pins DATA_DIR=/data there, but switched to explicitly listing the database "
            "file plus the three upload directories anyway, so it can't pick up the wrong "
            "thing regardless of what DATA_DIR happens to point at."
        ),
        "image": None,
        "lines_changed": 50,
        "estimated": False,
    },
    {
        "date": "2026-08-03",
        "title": "忘记密码怎么办：管理员可以帮账号重置密码了",
        "title_en": "Added admin-assisted password recovery",
        "summary": (
            "账号管理页给每个账号加了两个操作：一个是管理员直接输入新密码帮对方重置"
            "（最简单粗暴，改完口头告诉本人）；另一个是生成一次性重置链接，24 小时内"
            "有效、用一次就失效，管理员复制链接通过微信之类的渠道发给对方，对方点开"
            "自己设新密码，管理员不用知道对方设的是什么。没有接邮件发送服务——账号"
            "目前都是熟人在用，这两种方式已经够用，也省去了配置邮件服务商的麻烦。"
        ),
        "summary_en": (
            "Added two actions to each account row on the account-management page: an "
            "admin can directly set a new password for someone (simplest option -- just "
            "tell them the new password afterward), or generate a one-time reset link "
            "(valid 24 hours, single use) that the admin copies and sends through any "
            "channel -- the recipient opens it and sets their own new password without "
            "the admin ever seeing it. Deliberately skipped hooking up an email-sending "
            "service: with a small, known set of accounts, these two options cover it "
            "without the setup overhead of a transactional email provider."
        ),
        "image": None,
        "lines_changed": 196,
        "estimated": False,
    },
    {
        "date": "2026-08-04",
        "title": "小说章节编辑框改成跟阅读页一样宽、一样大字号",
        "title_en": "Chapter editor now matches the reader view's width and font size",
        "summary": (
            "编辑章节正文的输入框之前套用的是通用表单样式，最大只有 560px 宽，比"
            "实际阅读页窄很多，写的时候很难感觉出真实排版效果。现在编辑框和阅读页"
            "的正文区域宽度、字号、行高都对齐了（都是 870px 宽、16px 字号、1.9 倍行"
            "距），编辑时看到的宽度基本就是读者看到的宽度。中途踩了个 CSS 优先级的"
            "坑：新加的字号规则一开始被更早的通用规则（`.form textarea`）盖掉了，"
            "因为后者选择器权重更高，改成更具体的选择器才生效。"
        ),
        "summary_en": (
            "The chapter content textarea was using the generic form style, capped at "
            "560px wide -- much narrower than the actual reading page, making it hard to "
            "judge real layout while writing. Now the editor and the reader view line up "
            "on width, font size, and line height (both 870px wide, 16px text, 1.9x line "
            "height), so what you see while editing is close to what readers will see. Hit "
            "a CSS specificity snag along the way: the new font-size rule was silently "
            "overridden by an earlier, more specific generic rule (`.form textarea`) until "
            "switched to a more specific selector."
        ),
        "image": None,
        "lines_changed": 15,
        "estimated": False,
    },
    {
        "date": "2026-08-07",
        "title": "英文版第一步：公开页面（首页、小说、登录）能切成英文了",
        "title_en": "English site, step 1: public pages (home, novels, login) now switch",
        "summary": (
            "导航栏加了一个 中文/EN 切换按钮，点一下整站记住，下次访问不用再切。这一步先翻了访客能看到的"
            "公开页面：公开首页（含技术架构图）、登录/注册/重置密码、小说列表和小说阅读页——界面文字（导航、"
            "按钮、提示语）换成英文，但书影读后感、动态、小说正文这些自己写的内容永远不翻译，还是原文显示。"
            "机制上是一个新的 translations.py 里的字典，键就是中文原文本身，没翻译到的字符串会自动原样"
            "显示中文，不会出现空白或报错。日常使用的核心页面（首页动态流、加书加剧、写小说）还没翻，下一步"
            "继续。"
        ),
        "summary_en": (
            "Added a 中文/EN toggle to the nav — one click and it's remembered site-wide, no need to "
            "flip it again on the next visit. This first pass covers the pages a visitor without an "
            "account would actually see: the public homepage (including the architecture diagram), "
            "login/register/reset-password, and the novel list + reader — UI chrome (nav, buttons, "
            "hints) switches to English, but anything you actually wrote yourself (book notes, moments, "
            "novel chapters) is never machine-translated and always stays as written. Under the hood: a "
            "new translations.py dict keyed by the Chinese source text itself, so anything not yet added "
            "just falls back to showing the original Chinese instead of breaking or going blank. The "
            "day-to-day pages (main feed, add book/show, write a novel) aren't translated yet — next up."
        ),
        "image": None,
        "lines_changed": 320,
        "estimated": False,
    },
    {
        "date": "2026-08-07",
        "title": "英文版第二步：日常使用页面（首页动态流、加书、写动态）也能切英文了",
        "title_en": "English site, step 2: day-to-day pages (feed, add, moments) now switch",
        "summary": (
            "接着上一步，把登录后天天在用的页面也翻了：首页动态瀑布流、单条目详情页、加书/加剧/记录动态"
            "的表单、按天查看、全站搜索。翻的还是界面文字（按钮、标签、提示语、状态名如「想看/进行中/已"
            "完成」），感想、评论、动态内容这些自己写的东西一如既往不翻译。顺手修了两个小问题：一是首页"
            "动态流和按天查看里混进来的「网站更新」卡片之前没跟着切语言，现在也会显示对应语言的标题和摘要；"
            "二是发现登录/注册/退出的时候后端会清空整个 session，之前设置的语言偏好也被一起清掉了——测试"
            "的时候切成英文、登出再登入，页面又变回中文才发现——现在这三个地方都会在清空前把语言偏好先存"
            "一下、清完再放回去。"
        ),
        "summary_en": (
            "Continuing from step 1: translated the pages used every day once logged in — the main "
            "feed, item detail, the add-book/add-show/log-a-moment forms, the day view, and site "
            "search. Same scope as before: UI chrome only (buttons, labels, hints, status names like "
            "\"want to / in progress / done\") — reviews, comments, and moment content you actually "
            "wrote are never touched. Fixed two small things along the way: the \"site update\" cards "
            "that show up in the main feed and day view weren't switching language before, now they "
            "show the matching title/summary; and login/register/logout were calling session.clear(), "
            "which wiped the language preference along with everything else -- caught it while testing "
            "when switching to English, logging out, and back in reset the site to Chinese. All three "
            "now stash the language choice before clearing and restore it after."
        ),
        "image": None,
        "lines_changed": 260,
        "estimated": False,
    },
]
