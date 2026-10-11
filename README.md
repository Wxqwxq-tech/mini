# C1 · 课程资料获取与翻译

> 挑战编号：`ch-20260717031336-pxzwy0`　|　截止时间：2026-12-31 23:59
> 主题：把「Vibe Coding」课程（CS146S）的在线/离线资料抓取下来，建立一套**可复用的机器翻译流水线**，产出高质量中文版并沉淀术语表。

---

## 一、成果概览

| 指标 | 数值 |
|---|---|
| 原始材料规模 | 31 个网页 + 4 份 PDF（原文 **105,079 词**） |
| 翻译分段 | **60 个单元**（按 2600 词/段切分） |
| 成品译文 | **35 篇**（31 网页 + 4 PDF），Markdown 格式 |
| 术语表 | 四类 **77 条术语** + **6 条翻译硬规则** |
| 抽检结果 | 缺译 0；高英文残留 2（均为站点头部/专有名词/无关摘要，正文已全译） |

---

## 二、目录结构

```
C1工作区/
├── 材料_解压/          # CS146S_offline.zip 解压后的原始站点（pages/ pdfs/ assets/ site/ …）
├── source/             # 01_extract.py 抽取的纯文本（pages/ + pdfs/）
├── work/               # 02_segment.py 分段后的翻译单元 + units.json
├── translated/
│   ├── _parts/         # 60 个单元的译文（中间态）
│   ├── pages/          # 31 篇网页成品译文
│   └── pdfs/           # 4 篇 PDF 成品译文
├── pipeline/           # 可复用流水线脚本 + 术语表
│   ├── 01_extract.py   # 抽取：zip/PDF → 纯文本
│   ├── 02_segment.py   # 分段：按 2600 词切分，生成 units.json
│   ├── 03_assemble.py  # 装配：合并 part → 成品文章
│   ├── 04_spotcheck.py # 抽检：缺译/英文残留/术语命中率
│   └── 术语表.md        # 77 条标准译法 + 6 条硬规则
├── inventory.json       # 材料清单（抽取统计）
└── 交付物/             # README / AI日志 / AAR / 拿来说明
```

---

## 三、翻译质量保障

1. **术语统一**：翻译前先建术语表（Vibe Coding→氛围编程、Prompt Injection→提示注入、Code Review→代码评审 等 77 条），60 个单元全部按表翻译。
2. **分批机器翻译**：60 个单元分批交给 AI 翻译，每批核对落盘与字符数，异常单元人工复核（如 43 字符的纯导航页、Medium 拦截页）。
3. **脚本化抽检**：`04_spotcheck.py` 自动统计缺译、英文残留比例、术语命中率，产出可复现的质检报告。
4. **诚实覆盖声明**：拿不到的源内容（登录墙/拦截/空页/扫描件）不硬造，统一写「覆盖说明」，在 AI日志/AAR 中如实记录。

---

## 四、覆盖情况（诚实声明）

**完整翻译：30 篇网页 + 3 份 PDF。**

**覆盖缺口（源站拿不到或需 OCR）：**

| 单元 | 原因 | 处置 |
|---|---|---|
| peeking-under-the-hood-of-claude-code | Medium 拦截自动抓取 | 保留原文链接，落盘覆盖说明 |
| good-context-good-code | Ghost「输入访问码」登录墙 | 落盘覆盖说明 |
| how-warp-uses-warp | 仅 Notion 嵌入占位 | 落盘覆盖说明 |
| lessons-from-ai-code-reviews | 源文件 0 字符 | 落盘覆盖说明 |
| Vibe_Coding_Playbook.pdf（14 页扫描件） | 无文字层，需 OCR；本地 OCR 运行时安装失败 | 落盘覆盖说明，待联网补 OCR |

---

## 五、如何复现

完整步骤见 **《拿来说明.md》**；核心命令依次为：

```bash
python pipeline/01_extract.py   # 抽取
python pipeline/02_segment.py   # 分段
# （AI 分批翻译 _parts 单元）
python pipeline/03_assemble.py  # 装配
python pipeline/04_spotcheck.py # 抽检
```

---

## 六、交付物清单

- `README.md` —— 本文件，项目总览
- `AI日志.md` —— AI 使用全程记录
- `AAR.md` —— 课后复盘（KSTAR）
- `拿来说明.md` —— 材料获取与复现指南


---

## 七、GitHub 仓库内容说明

本仓库对应 EduSeed 挑战 **C1 课程资料获取与翻译**（挑战编号 `ch-20260717031336-pxzwy0`），收纳可公开的成品与可复用件：

```
.
├── README.md                    # 项目总览（本文件）
├── 交付物/
│   ├── AI日志.md                 # AI 协作日志
│   ├── AAR.md                   # KSTAR 复盘
│   └── 拿来说明.md               # 取用与复现说明
├── translated/
│   ├── pages/                   # 31 篇网页成品译文
│   ├── pdfs/                    # 4 篇 PDF 成品译文
│   ├── _assemble_report.json    # 分段装配报告
│   └── _spotcheck.json          # 抽检报告（缺译 0 篇）
├── pipeline/
│   ├── 01_extract.py            # 材料抽取
│   ├── 02_segment.py            # 按 2600 词切段
│   ├── 03_assemble.py           # 回装成篇
│   ├── 04_spotcheck.py          # 覆盖与残留抽检
│   └── 术语表.md                 # 77 条术语 + 6 条硬规则
└── inventory.json               # 材料清单
```

> 原始站点材料（`材料_解压/`）与分段中间态（`work/_parts`）体积较大，未纳入本仓库。需要完整复现时，按《拿来说明.md》先运行 `pipeline/01_extract.py` 重新抽取即可。

*生成时间：2026-10-10*
