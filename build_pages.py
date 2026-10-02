import json, re, html, os
from overviews import OV
d=json.load(open("data.json")); enrich=json.load(open("enrich.json")); imgmap=json.load(open("imgmap.json"))
abs_list=d["antibodies"]; panels=d["panels"]
def slug(k): return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",k.lower())).strip("-")
for a in abs_list: a["slug"]=slug(a["key"])
key2ab={a["key"]:a for a in abs_list}
# panels membership per marker
memb={}
for p in panels:
    for t in p["targets"]: memb.setdefault(t,[]).append(p["name"])

# ---- style.css : pull CSS from existing index.html + add subpage styles ----
cur=open("index.html").read()
css=re.search(r"<style>(.*?)</style>",cur,re.S).group(1)
sub_css='''
/* ---- subpage ---- */
.crumbs{font-size:.86rem;color:var(--muted);margin:26px 0 6px}
.crumbs a{color:var(--muted)} .crumbs a:hover{color:var(--brand)}
.ab-head{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:26px}
.ab-head h1{font-size:clamp(2rem,5vw,2.9rem);margin:.1em 0}
.ab-head .full{color:var(--muted);font-size:1.1rem}
.ab-cat{font-size:.8rem;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--brand),var(--brand2));padding:6px 12px;border-radius:999px}
.ab-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:28px;align-items:start}
@media(max-width:860px){.ab-grid{grid-template-columns:1fr}}
.block{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:22px;box-shadow:var(--shadow);margin-bottom:20px}
.block h2{font-size:1.15rem;margin-bottom:10px}
.refs{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.refs li{border-left:3px solid var(--brand);padding:2px 0 2px 14px}
.refs .t{font-weight:600;font-size:.95rem;line-height:1.4}
.refs .m{font-size:.82rem;color:var(--muted);margin-top:3px}
.refs .m a{font-weight:600}
figure{margin:0}
figure img{width:100%;border-radius:10px;border:1px solid var(--line);display:block}
figcaption{font-size:.78rem;color:var(--muted);margin-top:8px;line-height:1.4}
.hpa-link{display:inline-flex;align-items:center;gap:8px;background:var(--surface2);border:1px solid var(--line);padding:11px 16px;border-radius:10px;font-weight:700;color:var(--ink);margin-top:4px}
.hpa-link:hover{border-color:var(--brand)}
.kv{display:flex;flex-direction:column;gap:9px;font-size:.9rem}
.kv .row{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dashed var(--line);padding-bottom:8px}
.kv .row:last-child{border:0}
.kv .row span:first-child{color:var(--muted)}
.chips a{text-decoration:none}
.note2{font-size:.76rem;color:var(--muted);margin-top:10px}
td a.tlink{color:var(--brand2);font-weight:700}
.chip.lnk:hover{border-color:var(--brand);color:var(--brand)}
'''
open("style.css","w").write(css+sub_css)

# ---- index.html : external css + subpage links ----
idx=cur.replace("<style>"+css+"</style>",'<link rel="stylesheet" href="style.css"/>')
# add slug into inlined DATA: re-inline fresh data with slug
dataobj=json.loads(re.search(r"const DATA=(\{.*?\});",idx,re.S).group(1))
for a in dataobj["antibodies"]:
    a["slug"]=slug(a["key"])
idx=re.sub(r"const DATA=\{.*?\};",lambda m:"const DATA="+json.dumps(dataobj,separators=(",",":"))+";",idx,flags=re.S)
# link catalog target -> subpage
idx=idx.replace('`<tr><td><b>${a.target}</b></td>',
                '`<tr><td><a class="tlink" href="antibody/${a.slug}.html">${a.target}</a></td>')
# link panel marker chips -> subpage
idx=idx.replace('return `<span class="chip">${a?a.target:t}</span>`',
                'return a?`<a class="chip lnk" href="antibody/${a.slug}.html">${a.target}</a>`:`<span class="chip">${t}</span>`')
open("index.html","w").write(idx)

# ---- subpages ----
os.makedirs("antibody",exist_ok=True)
NAV='''<header><div class="wrap"><nav>
 <a class="logo" href="../index.html" style="text-decoration:none;color:inherit"><span class="dot"></span>Spatia&middot;CODEX</a>
 <div class="links"><a href="../index.html#panels">Panels</a><a href="../index.html#catalog">Antibodies</a><a href="../index.html#celltypes">Cell types</a><a href="../index.html#workflow">Workflow</a></div>
 <a href="../index.html#contact" class="btn" style="margin-left:14px">Start a project</a>
</nav></div></header>'''
PAPERFIG={"Ki67":("../img/paper_IMC_asthma_Ki67_tryptase.png","Imaging mass cytometry marker heatmap resolving Ki-67 (with EPX, MBP, tryptase, &alpha;SMA) across 750,883 airway cells. Liegeois et al., <i>J Clin Invest</i> 2025 (PMID 40091838), Fig 3D &mdash; CC BY 4.0."),
"MCT":("../img/paper_IMC_asthma_Ki67_tryptase.png","Imaging mass cytometry marker heatmap resolving mast-cell tryptase (with EPX, MBP, Ki-67) and identifying mast cells across airway tissue. Liegeois et al., <i>J Clin Invest</i> 2025 (PMID 40091838), Fig 3D &mdash; CC BY 4.0.")}
def esc(s): return html.escape(s or "",quote=True)
for a in abs_list:
    k=a["key"]; e=enrich.get(k,{}); im=imgmap.get(k,{})
    gene=e.get("gene",""); ensg=e.get("ensembl","")
    hpa=f"https://www.proteinatlas.org/{ensg}-{gene}" if ensg and gene else f"https://www.proteinatlas.org/search/{esc(gene or a['target'])}"
    # refs
    refs=e.get("refs",[])
    ref_html=""
    for r in refs:
        link=(f"https://europepmc.org/articles/{r['pmcid']}" if r.get("pmcid") else (f"https://doi.org/{r['doi']}" if r.get("doi") else f"https://europepmc.org/article/MED/{r['pmid']}"))
        meta=" &middot; ".join([x for x in [esc(r.get('journal','')),esc(str(r.get('year','')))] if x])
        oa=" &middot; <span style='color:var(--brand)'>open access</span>" if r.get("pmcid") else ""
        ref_html+=f'<li><div class="t">{esc(r.get("title",""))}</div><div class="m">{meta}{oa} &middot; <a href="{link}" target="_blank" rel="noopener">view paper &amp; figures &rarr;</a></div></li>'
    if not ref_html: ref_html='<li class="m">No open-access spatial-proteomics paper indexed yet &mdash; see the Human Protein Atlas entry and the Europe PMC search.</li>'
    epmc_q=f"https://europepmc.org/search?query=%22{esc(a['target'].split(' ')[0])}%22%20AND%20(%22imaging%20mass%20cytometry%22%20OR%20CODEX%20OR%20CyCIF%20OR%20MIBI)"
    # figure block
    if k in PAPERFIG:
        src,cap=PAPERFIG[k]
        fig=f'<figure><img src="{src}" alt="Spatial-proteomics figure for {esc(a["target"])}"/><figcaption>{cap}</figcaption></figure>'
    elif im.get("img"):
        fig=f'<figure><img src="../{im["img"]}" alt="{esc(a["target"])} expression"/><figcaption>Representative immunohistochemistry for <b>{esc(a["target"])}</b> ({esc(gene)}). Image &copy; <a href="{hpa}" target="_blank" rel="noopener">Human Protein Atlas</a>, CC BY-SA 3.0. See the HPA entry for spatial / single-cell expression.</figcaption></figure>'
    else:
        fig=f'<div class="block" style="text-align:center;color:var(--muted)">Expression imagery: see the <a href="{hpa}" target="_blank" rel="noopener">Human Protein Atlas</a> entry.</div>'
    cells=" &middot; ".join(esc(c) for c in a["cells"])
    pan=memb.get(k,[])
    pan_html="".join(f'<a class="chip lnk" href="../index.html#panels">{esc(p)}</a>' for p in pan) or '<span class="muted">—</span>'
    ov=esc(OV.get(k,""))
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(a["target"])} &mdash; Spatia&middot;CODEX antibody</title>
<meta name="description" content="{esc(a["target"])} ({esc(gene)}) for CODEX / spatial proteomics: overview, cell types resolved, spatial-proteomics literature and Human Protein Atlas expression."/>
<link rel="stylesheet" href="../style.css"/></head><body>
{NAV}
<div class="wrap">
 <div class="crumbs"><a href="../index.html">Home</a> / <a href="../index.html#catalog">Antibody library</a> / {esc(a["target"])}</div>
 <div class="ab-head"><div><h1>{esc(a["target"])}</h1><div class="full">{esc(gene) or ""}{(" &middot; ") if gene else ""}resolves {cells}</div></div><div><span class="ab-cat">{esc(a["cat"])}</span></div></div>
 <div class="ab-grid">
  <div>
   <div class="block"><h2>Overview</h2><p>{ov}</p></div>
   <div class="block"><h2>Selected spatial-proteomics literature</h2>
     <ul class="refs">{ref_html}</ul>
     <p class="note2">Auto-compiled from Europe PMC: open-access papers where <b>{esc(a["target"])}</b> co-occurs with a CODEX / PhenoCycler, MIBI, CyCIF or imaging-mass-cytometry method. <a href="{epmc_q}" target="_blank" rel="noopener">See all results &rarr;</a></p>
   </div>
  </div>
  <div>
   <div class="block"><h2>Expression</h2>{fig}<a class="hpa-link" href="{hpa}" target="_blank" rel="noopener">&#128279; Human Protein Atlas &rarr;</a></div>
   <div class="block"><h2>At a glance</h2><div class="kv">
     <div class="row"><span>Target</span><b>{esc(a["target"])}</b></div>
     <div class="row"><span>Gene</span><b>{esc(gene) or "—"}</b></div>
     <div class="row"><span>Compartment</span><b>{esc(a["cat"])}</b></div>
     <div class="row"><span>Resolves</span><b style="text-align:right;max-width:60%">{cells}</b></div>
   </div></div>
   <div class="block"><h2>In our panels</h2><div class="chips">{pan_html}</div></div>
  </div>
 </div>
 <p style="margin:30px 0 50px"><a href="../index.html#catalog" class="btn ghost">&larr; Back to the antibody library</a></p>
</div>
<footer><div class="wrap foot"><div class="muted">Spatia&middot;CODEX &middot; spatial-proteomics CRO. For research use only.</div><div class="muted"><a href="../index.html">Home</a></div></div></footer>
</body></html>'''
    open(f"antibody/{a['slug']}.html","w").write(page)
print("subpages written:",len(abs_list))
print("sample slugs:",[a["slug"] for a in abs_list[:6]])
