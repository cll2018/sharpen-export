# 站点验证 DNS 记录清单（Cloudflare 操作）

站托管在 Cloudflare Pages。"域名所有权验证"必须在 **Cloudflare DNS** 里加 TXT 记录（不是改代码）。
下面把各平台要加的解析记录都列好，**值由你登录后从对应平台复制**，本表只给"主机记录名 + 类型 + 指向/内容"的骨架。

> 怎么加：Cloudflare 控制台 → 你的站点 `sapu-cn.online` → DNS → 记录 → Add record（类型 TXT）。
> Cloudflare 免费版 DNS 变更约 1–5 分钟生效，GSC 验证时可点"重新验证"。

---

## 1. Google Search Console（最重要）

平台给的验证串形如 `google-site-verification=abcDEF...`（**整段照抄**）。

| 类型 | 名称 | 内容 |
|------|------|------|
| TXT  | `google-site-verification` | `google-site-verification=把GSC给的验证码粘贴在这` |

- GSC 入口：https://search.google.com/search-console → 添加资源 → "网址前缀" → `https://www.sapu-cn.online/`
- 选择验证方式 "DNS 记录"，复制 `google-site-verification=xxx`，填到 Cloudflare 上面那条 TXT。
- 回到 GSC 点"验证"（成功即完成）。
- 验证后：
  1. 左侧 **Sitemap** → 输入 `/sitemap.xml` → 提交（70 URL 全部进队列）。
  2. **URL 检查** → 输入 `https://www.sapu-cn.online/en/` → "请求编入索引"。
  3. 可选：再提交一次首页 `https://www.sapu-cn.online/`（根域跳 en）。

> 备选"HTML 标签"法（不想动 DNS 时）：把 GSC 给的 `<meta ...>` 整段填进
> `_data/site.js` 的 `gscVerifyMeta` 字段并部署，全站 14 语种首页都会带该标签，
> 然后 GSC 选"HTML 标签"法验证。

---

## 2. Bing Webmaster Tools（同时驱动 Yandex / Ecosia）

Bing 给的验证串有两种：TXT（`ms=...`）或 **CNAME 别名记录**。你当前这条是 **CNAME**：

| 类型 | 名称（子域） | 指向 / 值 |
|------|------|------|
| CNAME | `8cbed92e5e67f8673771e5f0b8af5b1c` | `verify.bing.com` |

> 在 Cloudflare：DNS → 记录 → Add record → 类型 **CNAME**、名称填 `8cbed92e5e67f8673771e5f0b8af5b1c`、目标/指向填 `verify.bing.com`（省掉前缀子域即可，CF 会自动拼 `.sapu-cn.online`）。

- 入口：https://www.bing.com/webmasters → 添加站点 → `https://www.sapu-cn.online`
- 选 "DNS record"，复制 Bing 给的 CNAME（名称 + verify.bing.com），加到 Cloudflare。
- 验证后 Indexing → Sitemaps → 提交 `https://www.sapu-cn.online/sitemap.xml`。
- 用同一 Bing 账号登录 **Yandex Webmaster**（https://yandex.com/webmasters）提交同一 sitemap。

---

## 3. 百度站长平台（中国国内）

| 方式 | 说明 |
|------|------|
| 文件验证（推荐，代码侧已支持） | 百度会给一个文件名+校验文件，放仓库根目录 `functions/verify/baidu.js` 响应即可 |
| HTML 标签 | 百度给 `<meta ...>`，填进 `_data/site.js` 的 `baiduVerifyMeta` 并部署 |
| DNS TXT | 形如 `baidu-site-verification=xxx`，加 Cloudflare TXT |

- 入口：https://ziyuan.baidu.com → 添加网站 → `https://www.sapu-cn.online`
- 提交：左侧 "普通收录/快速收录" 粘贴 sitemap `https://www.sapu-cn.online/sitemap.xml` 或首页 URL。
- 注意：.online 域名 Baidu 爬得慢，可加"快速收录"接口（需人工/付费）。

---

## 4. 搜狗 / 360 站长平台（可选，国内长尾）

| 平台 | 入口 | 验证 |
|------|------|------|
| 搜狗站长 | https://zhanzhang.sogou.com | 添加域名后提交 sitemap / 首页 |
| 360 站长 | https://zhanzhang.so.com | 同上，DNS TXT `360-site-verification=xxx` |

---

## 5. 其他全球引擎（可选）

- **Yandex Webmaster**：https://yandex.com/webmasters（Bing 账号登录，提同一 sitemap）
- **Brave Search**：https://search.brave.com/business（提交 sitemap）
- **Mojeek**：https://www.mojeek.com/submit
- **Seznam.cz**（捷克）：https://www.seznam.cz/zh/request
- **Ecosia**（底层走 Bing，自动收录，无需单独提交）

---

## 自动化（已预留）

- `scripts/ping_gsc.py`：Cloudflare Pages 部署 hook 里定期 POST 触发 GSC 抓取（验证过的账号效果更好，需 GSC 提供的 API key 走 Search Console API 的 `urls:submitIndex`）。
- `_data/seo.js`：每次 Cloudflare 重建自动刷新 `sitemap.xml` 的 `lastmod`（=构建日），搜索引擎可感知更新。
