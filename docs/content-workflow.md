# 内容维护手册（中文为唯一内容源）

本站有 14 个语种，但**只需要维护中文**。在后台改中文 → 保存并发布 →
系统自动把改动翻译并同步到其余 13 个语种 → Cloudflare 自动重建上线。
整个过程不需要人工处理其它语言。

---

## 1. 后台入口与登录

| 用途 | 地址 |
| --- | --- |
| 内容管理后台 | `https://www.sapu-cn.online/admin/` |
| 一键发布（新建长文/产品，带翻译预览） | `https://www.sapu-cn.online/admin/publish.html` |

后台用 GitHub 账号登录（自建 OAuth 代理，见 `functions/decap/auth.js`）。
登录后左侧菜单就是可编辑的内容，**中文的集合排在最上面**。

> 因为开启了「编辑工作流」，保存后会先进入草稿，点 **Publish** 才真正上线。

### 谁能登录（登录白名单）

本站的 GitHub OAuth App 是公开的，任何人点「Login with GitHub」都能走到 GitHub 的
授权页 —— **授权页本身不是门**。真正的门在 `functions/decap/auth/callback.js`：
拿到令牌后会用令牌问 GitHub「你是谁」，只有当登录名出现在环境变量
`GITHUB_ALLOWED_LOGINS` 里，才把令牌交给后台；否则**拒绝**（并把刚签发的令牌立刻吊销）。

| 项目 | 值 |
| --- | --- |
| Cloudflare Pages 环境变量 | `GITHUB_ALLOWED_LOGINS` |
| 当前值 | `cll2018`（多个账号用英文逗号分隔，如 `cll2018,someone-else`） |
| 生效范围 | production 与 preview 两套都要配（项目级变量分两套） |

要点：

- **变量为空 / 未设置时，校验会被跳过**，行为退回改动前的样子 ——
  所以这个变量只可能收紧权限，不会把你自己锁在门外。
- 被拒绝的人看到的是「GitHub 账号 @xxx 不在本后台的登录白名单内」，
  后台登录页也会同时弹出这条原因，不会一直转圈。
- 换人维护时：改这个环境变量即可，不用改代码。改完 Cloudflare 会重新部署一次。

---

### 接口限流（大模型 20 次/分钟、询盘按 IP 限制）

两个容易把线上打坏的地方，统一在 `functions/_lib/rate-limit.js` 里处理，
计数存在 Cloudflare D1（Pages 绑定名 `RATE_LIMIT_DB`，库名 `sapu-ratelimit`）。

| 限制对象 | 默认值 | 说明 |
| --- | --- | --- |
| 大模型调用 | **20 次 / 分钟**（全站共享） | `agnes-3.0-flash` 超过就会回 429。`/ai-chat` 和 `/translate` **共用同一份额度**，因为服务商是按密钥计的，不是按接口 |
| 询盘提交 | 同 IP **5 分钟内 5 次** | 超过返回 429，前端按当前语种弹出提示 |
| 询盘提交 | 同 IP **累计 10 次** | 超过即拒绝（提示改用邮件 / WhatsApp） |

要点：

- **为什么用数据库**：Pages Functions 是无状态的，进程内计数器只能管住单个实例；
  而大模型的额度是按密钥全局算的，只有共享计数才真的防得住 429。
- **一律「失败放行」**：D1 出问题时限流自动失效，网站照常可用，询盘也不会丢。
- **只存哈希**：访客 IP 只以 `SHA-256(盐 + IP)` 入库，从不保存原始地址。
- **计数口径**：询盘只在**真正提交成功后**才计数，所以访客填错表单不会消耗自己的额度。
- **想调数值**：改 Cloudflare Pages 环境变量 `LLM_MAX_PER_MINUTE`、`RFQ_MAX_PER_WINDOW`、
  `RFQ_WINDOW_MINUTES`、`RFQ_MAX_TOTAL_PER_IP`；不配置就用上表默认值。
- `RATE_LIMIT_SALT` 是哈希用的盐。**换掉它等于把已有的询盘计数全部清零**（用于解封）。

---

## 2. 各菜单能改什么

### 只改中文，其余语种自动生成

| 菜单 | 内容 |
| --- | --- |
| Pages (中文) → 首页 / 产品中心 / 关于我们 / 联系与询盘 / 新闻中心 | 各页面的标题、SEO 描述、正文 |
| 隐私政策 / 搜索页（中文） | 这两个页面的标题、描述、正文 |
| 新闻文章 · 中文（简体） | 新闻的增 / 删 / 改 |
| 产品介绍 · 中文（简体） | 产品的增 / 删 / 改 |
| 界面文案（i18n） | 按钮、页脚、搜索框等所有界面短文案（只维护中文一列） |
| 站点信息 · Site Info | 品牌名、联系方式、导航、页脚（只维护中文相关字段） |
| AI 设置 | AI 在线客服的行为与话术（非页面文案） |

### 不需要手改

`繁體中文 / English / Deutsch / 日本語 / 한국어 / Русский / Español /
Português / Français / Italiano / Türkçe / العربية / Tiếng Việt` 这些集合
**由中文自动同步生成**。菜单里也能看到、能改，但手改的内容会在下一次
中文更新时被覆盖；确实需要长期固定某个语种的说法时，请连同中文一起
说明，或直接改仓库里 `zh/` 下的对应文件。

---

## 3. 保存并发布之后会发生什么

```
后台保存中文 → Publish（提交到 GitHub main）
        │
        ▼
GitHub Action「i18n sync (中文 → 其余 13 语种)」
  1. 找出这次改了哪些 zh/ 文件、data/i18n.json、data/site.json
  2. 调用 LLM 翻译成其余 13 个语种
  3. 结构字段（permalink / lang / productId / 图片路径 等）按语种自动改好
  4. 本地化一致性检查：语种专属的 site.* 变量、正文站内链接
  5. 维护索引数据：_data/newsSlugs.json、_data/productOrder.json、_data/productSlugs.json
  6. 重新生成 _data/products.js（首页与产品列表卡片）
  7. 校验产出的页面（标题 / permalink / lang 齐全）后提交回 main
        │
        ▼
Cloudflare Pages 自动重建 → 1~2 分钟后 14 个语种全部更新
```

工作流文件：`.github/workflows/i18n-sync.yml`
翻译脚本：`scripts/i18n-sync.mjs`
术语表（中英德日… 统一说法）：`data/translation-glossary.json`

### 第 4 步「本地化一致性检查」做什么

有两件事属于**机械改写**而不是翻译，所以不依赖中文是否改动，每次同步都会重做一遍：

- **语种专属的站点变量**：中文页面写 `{{ site.addressZh }}` / `{{ site.nameZh }}`，
  其余语种必须换成 `{{ site.address }}` / `{{ site.name }}`，
  繁体中文换成 `{{ site.addressZhTw }}` / `{{ site.nameZhTw }}`。
- **正文里的站内链接**：中文正文写的 `/zh/contact/` 之类，要改成读者所在语种的
  `/<语种>/contact/`。

每次同步都重跑，是为了让**历史遗留和被手工改过的文件能自己纠正**——
例如 `zh-tw/contact.md` 曾一直用着 `{{ site.addressZh }}`，
于是繁体页面显示的是简体地址；这种情况会被自动发现并修好。

> 顺带一提：脚本会**保留文件原本的换行风格**（仓库里大多数文件是 LF，
> 但每个语种的 5 个单页文件早年是以 CRLF 提交的）。
> 若强行统一成 LF，会把「改一个词」变成「整个文件重写」，
> 提交记录就没法看了。

### 术语一致性

`data/translation-glossary.json` 里钉住了行业术语的固定译法
（金刚石砂轮 / CBN砂轮 / 硬质合金 / 金属陶瓷结合剂 / 均热板 …），
后台一键发布页和自动同步都用同一份术语表，所以两种发布途径出来的
用词是一致的。要改统一说法，改这个文件即可。

---

## 4. 新增内容

### 新增一条新闻

1. 后台 →「新闻文章 · 中文（简体）」→ 右上角新增。
2. 填写：发布日期、栏目、标题、SEO 描述、**URL Slug**、正文。
   URL Slug 是**必填**项，只能用小写英文 + 短横线（例 `tinico-heat-spreader-dev`）。
3. 这条 slug 同时决定文件名和网址：中文是 `/zh/news/<slug>/`，
   另外 13 个语种是 `/<语种>/news/<slug>/`——所有语种共用同一个
   ASCII 网址，不会出现中文网址。
4. Publish → 自动翻译并同步。

### 新增一个产品

1. 后台 →「产品介绍 · 中文（简体）」→ 新增。
2. 填写：产品名称、SEO 描述、卡片简介、**产品锚点 ID**、产品图、产品详情 HTML。
   产品锚点 ID 是**必填**项（小写英文 + 短横线），它同时是该产品的页面网址
   `/zh/products/<ID>/` 和产品列表里的跳转锚点。
3. Publish → 自动翻译；首页与产品中心的卡片会自动多出这一项。

### 删除

在对应中文集合里删除条目并发布，其余 13 个语种的同名页面会自动一并删除。

---

## 5. 出问题时怎么办

| 现象 | 处理 |
| --- | --- |
| 中文已发布，但其它语种没变 | 打开 GitHub → Actions →「i18n sync」看运行日志；也可以在 Actions 页面手动 Run workflow |
| 某个语种翻译失败 | 日志里会有 `::warning::`；该语种保持原内容不会写坏，重跑一次即可 |
| 翻译用词不对 | 改 `data/translation-glossary.json` 里的术语，然后手动 Run workflow |
| 某个语种的联系方式 / 站内链接不对 | 手动 Run workflow 即可，第 4 步会自动纠正并留一条提交记录 |
| 想检查改动是否合理 | 看 GitHub 上那次 `i18n: sync 13 languages from zh [i18n-sync]` 提交的 diff |
| 一键发布页提示「上游接口限流（429）」 | 大模型接口按次数限流。等约 1 分钟再点「① 生成 14 语种」；不要连续狂点，重试太快只会加剧限流 |
| 后台登录被拒，提示账号不在白名单 | 改 Cloudflare Pages 环境变量 `GITHUB_ALLOWED_LOGINS`（见第 1 节） |
| 网站 AI 客服只回「稍后联系」套话、不给答案 | 说明大模型没回话。看 D1 里 `llm_window` 的 `used` 是否接近 20，或服务商侧限流（会回 429） |
| 客户说询盘提交被拦 | 该网络 5 分钟内超过 5 次或累计超过 10 次。确认是真实客户后，可在 Cloudflare 的 D1 控制台执行 `DELETE FROM rfq_events;` 立即解封（只影响限流计数，不影响任何已收到的询盘） |

> 说明：本站 zone 的 `origin_error_page_pass_thru` 为 `off`，Cloudflare 会把
> Pages 返回的 5xx 正文替换成它自己的「502 Bad gateway」页。所以
> `/translate` 一律用 `HTTP 200 + ok:false` 报告失败，这样后台能看到**真实原因**
> 而不是一句没有信息量的 502。

工作流的运行前提是仓库里配置了 Actions 密钥 `AI_LLM_API_KEY`
（与 Cloudflare Pages 上同名环境变量一致），已配置完成。

---

## 6. 派生数据文件（不要手改）

| 文件 | 来源 |
| --- | --- |
| `_data/products.js` | 由 `scripts/gen_products_data.py` 从各语种 `products/*.md` 生成 |
| `data/i18n.json` | 界面文案，后台「界面文案」集合维护 |
| `data/site.json` | 站点信息，后台「站点信息」集合维护 |
| `data/translation-glossary.json` | 术语表 |
| `_data/newsSlugs.json` | 新闻标题索引（sitemap 与列表用），同步脚本自动维护 |
| `_data/productOrder.json`、`_data/productSlugs.json` | 产品顺序与 slug 映射，同步脚本自动维护 |
