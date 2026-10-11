# -*- coding: utf-8 -*-
"""C1 流水线 阶段1：抽取归档
把 CS146S 课程材料（HTML 页面 + PDF）抽取为结构化 Markdown/纯文本，
统一落到 source/ 目录，并生成 manifest.json 供后续分段与抽检使用。
换源复用：只需改 SRC_* 路径，输出结构保持不变。
"""
import os, re, json, html, sys
from html.parser import HTMLParser

BASE = r"D:\cogseed\userWorkSpace\我的挑战有哪些\C1工作区".replace(r"\.", ".")
BASE = r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C1工作区"
UNZIP = os.path.join(BASE, "材料_解压")
MAT   = os.path.join(BASE, "挑战_C1 课程资料获取与翻译_pxzwy0_材料")
OUT   = os.path.join(BASE, "source")
PAGES_OUT = os.path.join(OUT, "pages")
PDFS_OUT  = os.path.join(OUT, "pdfs")
os.makedirs(PAGES_OUT, exist_ok=True)
os.makedirs(PDFS_OUT, exist_ok=True)

# ---------- HTML -> Markdown ----------
class MD(HTMLParser):
    BLOCK = {"p","div","section","article","header","footer","nav","li","ul","ol",
             "h1","h2","h3","h4","h5","h6","tr","table","blockquote","pre","br"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out=[]; self.skip=0; self.pre=0; self.list_depth=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ("script","style","noscript"): self.skip+=1; return
        if self.skip: return
        if tag=="pre": self.pre+=1; self.out.append("\n```\n"); return
        if tag=="code" and not self.pre: self.out.append("`"); return
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self.out.append("\n"+"#"*int(tag[1])+" ")
        elif tag=="li": self.out.append("\n- ")
        elif tag=="br": self.out.append("\n")
        elif tag in ("p","div","tr"): self.out.append("\n")
        elif tag=="blockquote": self.out.append("\n> ")
        if tag=="img":
            alt=a.get("alt",""); src=a.get("src","")
            if alt or src: self.out.append(f"[图: {alt or src}]")
    def handle_endtag(self, tag):
        if tag in ("script","style","noscript"):
            if self.skip: self.skip-=1
            return
        if self.skip: return
        if tag=="pre": self.pre-=1; self.out.append("\n```\n"); return
        if tag=="code" and not self.pre: self.out.append("`"); return
        if tag in ("p","div","li","h1","h2","h3","h4","h5","h6","tr","blockquote"):
            self.out.append("\n")
    def handle_data(self, data):
        if self.skip: return
        self.out.append(data)
    def text(self):
        t="".join(self.out)
        t=re.sub(r"[ \t]+"," ",t)
        t=re.sub(r"\n[ \t]+","\n",t)
        t=re.sub(r"\n{3,}","\n\n",t)
        return t.strip()

def html_to_md(path):
    with open(path,"r",encoding="utf-8",errors="ignore") as f:
        raw=f.read()
    p=MD(); p.feed(raw); return p.text()

# ---------- PDF -> text ----------
def pdf_to_text(path):
    import pymupdf
    doc=pymupdf.open(path)
    parts=[]
    for i,page in enumerate(doc):
        parts.append(f"\n<!-- page {i+1} -->\n"+page.get_text())
    doc.close()
    return "\n".join(parts)

manifest={"pages":[],"pdfs":[]}
pages_dir=os.path.join(UNZIP,"CS146S_offline","pages")
pdfs_dir=os.path.join(UNZIP,"CS146S_offline","pdfs")

for fn in sorted(os.listdir(pages_dir)) if os.path.isdir(pages_dir) else []:
    if not fn.endswith(".html"): continue
    md=html_to_md(os.path.join(pages_dir,fn))
    out_fn=fn[:-5]+".md"
    with open(os.path.join(PAGES_OUT,out_fn),"w",encoding="utf-8") as f:
        f.write(md)
    manifest["pages"].append({"file":out_fn,"chars":len(md),
                              "words":len(re.findall(r"[A-Za-z0-9']+",md))})

def extract_pdf(path, outname):
    txt=pdf_to_text(path)
    with open(os.path.join(PDFS_OUT,outname),"w",encoding="utf-8") as f:
        f.write(txt)
    manifest["pdfs"].append({"file":outname,"chars":len(txt),
                             "words":len(re.findall(r"[A-Za-z0-9']+",txt))})

if os.path.isdir(pdfs_dir):
    for fn in sorted(os.listdir(pdfs_dir)):
        if fn.endswith(".pdf"):
            extract_pdf(os.path.join(pdfs_dir,fn), fn[:-4]+".txt")

# 额外材料：Vibe_Coding_Playbook.pdf（在材料根目录，zip 之外）
for fn in os.listdir(MAT):
    if fn.lower().endswith(".pdf"):
        extract_pdf(os.path.join(MAT,fn), fn[:-4]+".txt")

manifest["pages"].sort(key=lambda x:-x["chars"])
with open(os.path.join(OUT,"manifest.json"),"w",encoding="utf-8") as f:
    json.dump(manifest,f,ensure_ascii=False,indent=2)

tp=sum(x["chars"] for x in manifest["pages"]); tw=sum(x["words"] for x in manifest["pages"])
pp=sum(x["chars"] for x in manifest["pdfs"]); pw=sum(x["words"] for x in manifest["pdfs"])
print(f"pages={len(manifest['pages'])} chars={tp} words={tw}")
print(f"pdfs ={len(manifest['pdfs'])} chars={pp} words={pw}")
for p in manifest["pages"]:
    print(f"  {p['chars']:>8} chars {p['words']:>6} words  {p['file']}")
for p in manifest["pdfs"]:
    print(f"  {p['chars']:>8} chars {p['words']:>6} words  {p['file']}")
