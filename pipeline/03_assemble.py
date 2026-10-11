# -*- coding: utf-8 -*-
"""C1 流水线 阶段3：拼装
把 translated/_parts/ 下各单元的译文，按 units.json 的分段顺序合并成最终文件。
最终输出：translated/pages/*.md 与 translated/pdfs/*.md
"""
import os, json
from collections import OrderedDict

BASE = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C1工作区"
WORK  = os.path.join(BASE, "work")
PARTS = os.path.join(BASE, "translated", "_parts")
OUT_PAGES = os.path.join(BASE, "translated", "pages")
OUT_PDFS  = os.path.join(BASE, "translated", "pdfs")
for d in (PARTS, OUT_PAGES, OUT_PDFS):
    os.makedirs(d, exist_ok=True)

units = json.load(open(os.path.join(WORK, "units.json"), encoding="utf-8"))
groups = OrderedDict()
for u in units:
    groups.setdefault((u["kind"], u["source"]), []).append(u)

report = []
missing = []
for (kind, source), parts in groups.items():
    parts = sorted(parts, key=lambda x: x["part"])
    out_dir = OUT_PAGES if kind == "page" else OUT_PDFS
    final = source.rsplit(".", 1)[0] + ".md"
    final_path = os.path.join(out_dir, final)

    # 单段且已直接产出最终文件的情况（如首次试译）——跳过重建
    if len(parts) == 1:
        pfile = os.path.join(PARTS, parts[0]["unit"])
        if (not os.path.exists(pfile)) and os.path.exists(final_path):
            with open(final_path, encoding="utf-8") as f:
                report.append({"file": final, "kind": kind,
                               "parts": 1, "chars": len(f.read())})
            continue

    chunks = []
    for p in parts:
        pfile = os.path.join(PARTS, p["unit"])
        if os.path.exists(pfile):
            chunks.append(open(pfile, encoding="utf-8").read().strip())
        else:
            missing.append(p["unit"])
            chunks.append(f"\n<!-- [缺译] {p['unit']} -->\n")
    body = "\n\n".join(chunks)
    if body.strip():
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(body)
    report.append({"file": final, "kind": kind,
                   "parts": len(parts), "chars": len(body)})

json.dump(report, open(os.path.join(BASE, "translated", "_assemble_report.json"),
                       "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"assembled={len(report)}  missing_units={len(missing)}")
for m in missing:
    print("  MISSING:", m)
for r in report:
    print(f"  {r['kind']:>4} {r['parts']:>2}p {r['chars']:>7}c  {r['file']}")
