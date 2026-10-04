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
  4. 维护索引数据：_data/newsSlugs.json、_data/productOrder.json、_data/productSlugs.json
  5. 重新生成 _data/products.js（首页与产品列表卡片）
  6. 校验产出的页面（标题 / permalink / lang 齐全）后提交回 main
        │
        ▼
Cloudflare Pages 自动重建 → 1~2 分钟后 14 个语种全部更新
```

工作流文件：`.github/workflows/i18n-sync.yml`
翻译脚本：`scripts/i18n-sync.mjs`
术语表（中英德日… 统一说法）：`data/translation-glossary.json`

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
| 想检查改动是否合理 | 看 GitHub 上那次 `i18n: sync 13 languages from zh [i18n-sync]` 提交的 diff |

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
