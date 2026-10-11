# -*- coding: utf-8 -*-
"""C1 流水线 阶段2：分段
把 source/ 下的文件按段落边界切成 <=MAX_WORDS 的翻译单元，
落到 work/ 目录，并生成 units.json 供并行翻译与后续拼装使用。
换源复用：只依赖 source/ 的结构与 MAX_WORDS 阈值。
"""
import os, re, json

BASE = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C1工作区"
SRC_PAGES = os.path.join(BASE, "source", "pages")
SRC_PDFS  = os.path.join(BASE, "source", "pdfs")
WORK = os.path.join(BASE, "work")
os.makedirs(WORK, exist_ok=True)

MAX_WORDS = 2600  # 每个翻译单元最大英文词数

def words(t):
    return len(re.findall(r"[A-Za-z0-9']+", t))

def split_text(text):
    """按段落（空行）切分，贪心合并到接近 MAX_WORDS"""
    paras = re.split(r"\n\s*\n", text)
    units, cur = [], []
    cur_w = 0
    for p in paras:
        w = words(p)
        # 单段超限：按句子再切
        if w > MAX_WORDS:
            if cur:
                units.append("\n\n".join(cur)); cur=[]; cur_w=0
            for s in re.split(r"(?<=[.!?。！？])\s+", p):
                sw = words(s)
                if cur_w + sw > MAX_WORDS and cur:
                    units.append("\n\n".join(cur)); cur=[]; cur_w=0
                cur.append(s); cur_w += sw
        elif cur_w + w > MAX_WORDS and cur:
            units.append("\n\n".join(cur)); cur=[p]; cur_w=w
        else:
            cur.append(p); cur_w += w
    if cur:
        units.append("\n\n".join(cur))
    return units

manifest = []
def process_dir(src_dir, out_prefix, kind):
    for fn in sorted(os.listdir(src_dir)):
        path = os.path.join(src_dir, fn)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        units = split_text(text)
        base = fn.rsplit(".", 1)[0]
        for i, u in enumerate(units):
            if len(units) == 1:
                out_fn = f"{out_prefix}__{base}.md"
            else:
                out_fn = f"{out_prefix}__{base}__part{i+1:02d}.md"
            with open(os.path.join(WORK, out_fn), "w", encoding="utf-8") as f:
                f.write(u)
            manifest.append({"unit": out_fn, "source": fn, "kind": kind,
                             "part": i+1, "parts": len(units),
                             "words": words(u), "chars": len(u)})

process_dir(SRC_PAGES, "page", "page")
process_dir(SRC_PDFS,  "pdf",  "pdf")

manifest.sort(key=lambda x: -x["words"])
with open(os.path.join(WORK, "units.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"units={len(manifest)}  total_words={sum(m['words'] for m in manifest)}")
for m in manifest:
    print(f"  {m['words']:>5}w  {m['kind']:>4}  {m['unit']}")
