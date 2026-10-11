# -*- coding: utf-8 -*-
"""C1 流水线 阶段4：质量抽检
对翻译产出做三类可追溯检查，输出抽检报告（供 AAR 引用）：
 1) 完整性：每个源文件是否有对应译文、是否有缺译单元
 2) 残留英文率：译文正文（剔除代码块/URL）中纯英文词占比，过高说明疑似漏译
 3) 术语一致性：核心术语标准译法出现次数 + 疑似未译英文术语残留
"""
import os, re, json

BASE = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C1工作区"
SRC_PAGES = os.path.join(BASE, "source", "pages")
SRC_PDFS  = os.path.join(BASE, "source", "pdfs")
TR_PAGES  = os.path.join(BASE, "translated", "pages")
TR_PDFS   = os.path.join(BASE, "translated", "pdfs")

TERMS = ["氛围编程","提示工程","上下文","智能体","代码评审","漏洞","提示注入",
         "可观测性","值班","模型上下文协议","拉取请求","复盘","令牌","护栏","检索"]
RAW_HINTS = ["Vibe Coding","Prompt Engineering","Context Rot","Code Review",
             "Hallucination","Prompt Injection","Observability","On-call","Retrieval"]

def strip_code(md):
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    md = re.sub(r"`[^`]*`", "", md)
    md = re.sub(r"https?://\S+", "", md)
    md = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "", md)  # 链接/图片
    return md

def en_ratio(text):
    t = strip_code(text)
    en = re.findall(r"[A-Za-z]{3,}", t)
    cn = re.findall(r"[\u4e00-\u9fff]", t)
    total = len(en) + len(cn)
    return (len(en) / total) if total else 0.0

report = {"missing_files": [], "high_en_ratio": [], "files": [], "term_counts": {}}
term_total = {t: 0 for t in TERMS}
raw_total = {t: 0 for t in RAW_HINTS}

def check(src_dir, tr_dir, kind):
    if not os.path.isdir(src_dir):
        return
    for fn in sorted(os.listdir(src_dir)):
        base = fn.rsplit(".", 1)[0] + ".md"
        tr = os.path.join(tr_dir, base)
        if not os.path.exists(tr):
            report["missing_files"].append(base); continue
        text = open(tr, encoding="utf-8").read()
        ratio = en_ratio(text)
        rec = {"file": base, "kind": kind, "chars": len(text), "en_ratio": round(ratio, 4)}
        report["files"].append(rec)
        if ratio > 0.28:
            report["high_en_ratio"].append({"file": base, "en_ratio": round(ratio, 4)})
        for t in TERMS:
            term_total[t] += text.count(t)
        for r in RAW_HINTS:
            raw_total[r] += strip_code(text).count(r)

check(SRC_PAGES, TR_PAGES, "page")
check(SRC_PDFS, TR_PDFS, "pdf")

report["term_counts"] = {t: term_total[t] for t in TERMS if term_total[t]}
report["raw_term_hints"] = {t: raw_total[t] for t in RAW_HINTS if raw_total[t]}

with open(os.path.join(BASE, "translated", "_spotcheck.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("== 抽检报告 ==")
print(f"文件总数 {len(report['files'])}，缺译 {len(report['missing_files'])}，高英文残留 {len(report['high_en_ratio'])}")
for m in report["missing_files"]:
    print("  MISSING:", m)
for h in report["high_en_ratio"]:
    print(f"  HIGH-EN {h['en_ratio']:.0%}  {h['file']}")
print("术语标准译法命中:")
for t, c in sorted(report["term_counts"].items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")
print("疑似未译英文术语残留:")
for t, c in sorted(report["raw_term_hints"].items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")
