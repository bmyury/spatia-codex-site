import json
d=json.load(open("data.json"))
abs_list=d["antibodies"]; panels=d["panels"]
# lineage display groups from category
GRP=[("T cells & subsets",["T cell"]),("B & plasma cells",["B cell","Plasma"]),("NK & cytotoxic",["NK"]),
("Myeloid & dendritic",["Myeloid","DC"]),("Granulocytes & mast",["Granulocyte","Mast"]),
("Epithelium & tumour",["Epithelial","Tumor"]),("Stroma, vessels & nerve",["Stromal","Endothelial","Neural"]),
("Functional & activation states",["Checkpoint","Activation","Signaling","Proliferation/DDR","Other"])]
groups=[]
distinct=set()
for gname,cats in GRP:
    cells={}
    for a in abs_list:
        if a["cat"] in cats:
            for c in a["cells"]:
                distinct.add(c); cells.setdefault(c,set()).add(a["target"])
    groups.append({"name":gname,"cells":[{"name":c,"markers":sorted(m)} for c,m in sorted(cells.items())]})
cat_counts={}
for a in abs_list: cat_counts[a["cat"]]=cat_counts.get(a["cat"],0)+1
inject={"antibodies":abs_list,"panels":panels,"groups":groups,
 "stats":{"antibodies":len(abs_list),"cellTypes":len(distinct),"panels":len(panels)},
 "cats":sorted(cat_counts.keys())}
DATA=json.dumps(inject,separators=(",",":"))

html = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Spatia&middot;CODEX — Single-cell spatial proteomics CRO</title>
<meta name="description" content="A CODEX / PhenoCycler spatial-proteomics CRO. __NAB__ validated antibodies, __NCT__ resolvable cell types, and __NPAN__ ready-to-run panels for immuno-oncology, autoimmunity, neuro-inflammation and mucosal disease."/>
<style>
:root{
 --bg:#f6f8fb; --surface:#ffffff; --surface2:#eef2f8; --ink:#0f1b2d; --muted:#54657e;
 --line:#dde5ef; --brand:#0e7c86; --brand2:#2563c9; --accent:#e8614d; --chip:#eaf2f4;
 --shadow:0 1px 2px rgba(16,30,54,.06),0 8px 24px rgba(16,30,54,.06); --r:14px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
 --bg:#0b1220; --surface:#111b2e; --surface2:#16233c; --ink:#eaf1fb; --muted:#9db0cc;
 --line:#243консоль; --line:#223150; --brand:#3bb7c2; --brand2:#5b9bff; --accent:#ff7d68; --chip:#17283f;
 --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px rgba(0,0,0,.35);
}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:var(--brand2);text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
h1,h2,h3{line-height:1.15;letter-spacing:-.02em;margin:.2em 0}
h2{font-size:clamp(1.5rem,3.4vw,2.1rem)}
.muted{color:var(--muted)}
/* nav */
header{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
nav{display:flex;align-items:center;gap:18px;height:62px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.03em;font-size:1.12rem}
.logo .dot{width:26px;height:26px;border-radius:7px;background:linear-gradient(135deg,var(--brand),var(--brand2));box-shadow:0 2px 8px rgba(14,124,134,.5)}
nav .links{display:flex;gap:20px;margin-left:auto}
nav .links a{color:var(--ink);font-weight:600;font-size:.92rem;opacity:.82}
nav .links a:hover{opacity:1;color:var(--brand)}
.btn{display:inline-block;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;padding:11px 18px;border-radius:10px;font-weight:700;font-size:.92rem;border:0;cursor:pointer;box-shadow:var(--shadow)}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
@media(max-width:820px){nav .links{display:none}}
/* hero */
.hero{padding:70px 0 40px;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;inset:-40% -10% auto auto;width:620px;height:620px;background:radial-gradient(circle at 30% 30%,rgba(14,124,134,.22),transparent 60%),radial-gradient(circle at 70% 60%,rgba(37,99,201,.18),transparent 60%);filter:blur(6px);z-index:-1}
.kicker{display:inline-block;font-weight:700;font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brand);background:var(--chip);padding:6px 12px;border-radius:999px;border:1px solid var(--line)}
.hero h1{font-size:clamp(2.1rem,5.4vw,3.6rem);margin:.4em 0 .3em;max-width:16ch}
.hero p.lead{font-size:clamp(1.05rem,2.2vw,1.28rem);color:var(--muted);max-width:60ch}
.cta{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}
.stats{display:flex;gap:14px;margin-top:40px;flex-wrap:wrap}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 20px;box-shadow:var(--shadow);min-width:150px}
.stat b{display:block;font-size:2rem;letter-spacing:-.03em;background:linear-gradient(135deg,var(--brand),var(--brand2));-webkit-background-clip:text;background-clip:text;color:transparent}
.stat span{color:var(--muted);font-size:.9rem}
/* sections */
section{padding:56px 0}
.sec-head{max-width:64ch;margin-bottom:26px}
.sec-head .kicker{margin-bottom:12px}
/* panels */
.grid{display:grid;gap:18px}
.panels{grid-template-columns:repeat(auto-fill,minmax(330px,1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:22px;box-shadow:var(--shadow);display:flex;flex-direction:column}
.card h3{font-size:1.18rem}
.tagrow{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.tag{font-size:.74rem;font-weight:700;padding:4px 9px;border-radius:999px;background:var(--chip);color:var(--brand);border:1px solid var(--line)}
.tag.alt{color:var(--brand2)}
.card .app{font-size:.9rem;color:var(--muted);margin:8px 0 12px}
.card .metrics{display:flex;gap:16px;margin:4px 0 12px;font-size:.84rem;color:var(--muted)}
.card .metrics b{color:var(--ink)}
.toggle{margin-top:auto;background:var(--surface2);border:1px solid var(--line);color:var(--ink);font-weight:700;font-size:.85rem;padding:9px 12px;border-radius:9px;cursor:pointer;text-align:left}
.reveal{display:none;margin-top:12px;border-top:1px dashed var(--line);padding-top:12px}
.reveal.open{display:block}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:.76rem;padding:3px 9px;border-radius:7px;background:var(--surface2);border:1px solid var(--line);color:var(--ink)}
.chip.cell{background:transparent;color:var(--muted)}
.lab{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:12px 0 6px}
/* catalog */
.toolbar{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
#q{flex:1;min-width:220px;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font-size:.95rem}
.filters{display:flex;gap:7px;flex-wrap:wrap}
.fbtn{font-size:.8rem;font-weight:700;padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer}
.fbtn.active{background:var(--brand);color:#fff;border-color:var(--brand)}
.tablewrap{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;font-size:.92rem}
th,td{text-align:left;padding:12px 16px;border-bottom:1px solid var(--line);vertical-align:top}
th{position:sticky;top:62px;background:var(--surface2);font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);z-index:2}
tr:last-child td{border-bottom:0}
td .cat{font-size:.74rem;font-weight:700;color:var(--brand);background:var(--chip);padding:3px 8px;border-radius:6px;white-space:nowrap}
td.cells{color:var(--muted);font-size:.86rem}
.count{color:var(--muted);font-size:.85rem;margin-top:8px}
/* cell types */
.cellgrid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.lin{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px;box-shadow:var(--shadow)}
.lin h3{font-size:1.05rem;margin-bottom:10px}
.lin ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}
.lin li{font-size:.9rem;display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed var(--line);padding-bottom:6px}
.lin li:last-child{border-bottom:0}
.lin li .mk{color:var(--muted);font-size:.78rem;text-align:right;max-width:55%}
/* workflow */
.steps{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.step{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:22px;box-shadow:var(--shadow)}
.step .n{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;margin-bottom:10px}
/* cta */
.band{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-radius:22px;padding:46px;text-align:center;box-shadow:var(--shadow)}
.band h2{color:#fff}.band p{color:#eaf6f7;max-width:56ch;margin:10px auto 22px}
.band .btn{background:#fff;color:var(--brand)}
footer{border-top:1px solid var(--line);padding:30px 0;color:var(--muted);font-size:.85rem}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.note{font-size:.78rem;color:var(--muted);margin-top:10px}
</style>
</head>
<body>
<header><div class="wrap"><nav>
 <div class="logo"><span class="dot"></span>Spatia&middot;CODEX</div>
 <div class="links">
  <a href="#panels">Panels</a><a href="#catalog">Antibodies</a><a href="#celltypes">Cell types</a><a href="#workflow">Workflow</a><a href="#contact">Contact</a>
 </div>
 <a href="#contact" class="btn" style="margin-left:14px">Start a project</a>
</nav></div></header>

<section class="hero"><div class="wrap">
 <span class="kicker">CODEX &middot; PhenoCycler spatial proteomics CRO</span>
 <h1>Single-cell spatial proteomics, panel&#8209;ready.</h1>
 <p class="lead">We image dozens of proteins on a single tissue section and map every cell in its spatial context. Our validated antibody library and application-ready panels resolve the immune, stromal and epithelial compartments of your tissue — from biopsy to spatial single-cell data.</p>
 <div class="cta"><a href="#panels" class="btn">Explore panels</a><a href="#catalog" class="btn ghost">Browse antibody library</a></div>
 <div class="stats" id="stats"></div>
</div></section>

<section id="panels"><div class="wrap">
 <div class="sec-head"><span class="kicker">Ready-to-run panels</span>
  <h2>Application panels, built from in-stock antibodies</h2>
  <p class="muted">Each panel is assembled from our validated library and resolves a defined set of cell types. Panels are starting points — we tune the marker list to your tissue and question.</p></div>
 <div class="grid panels" id="panels-grid"></div>
</div></section>

<section id="catalog" style="background:var(--surface2)"><div class="wrap">
 <div class="sec-head"><span class="kicker">Antibody library</span>
  <h2>In-stock, CODEX-validated antibodies</h2>
  <p class="muted">Search the library and see the cell types each marker helps resolve. Filter by compartment.</p></div>
 <div class="toolbar">
  <input id="q" placeholder="Search a target, e.g. CD8, FoxP3, PD-L1, tryptase…"/>
 </div>
 <div class="filters" id="filters"></div>
 <div class="count" id="count"></div>
 <div class="tablewrap"><table><thead><tr><th>Target</th><th>Compartment</th><th>Resolves cell type(s)</th></tr></thead><tbody id="rows"></tbody></table></div>
 <p class="note">Library reflects the Nolan-lab CODEX antibody inventory. Clones/conjugations confirmed at project scoping; additional targets conjugated on request.</p>
</div></div></section>

<section id="celltypes"><div class="wrap">
 <div class="sec-head"><span class="kicker">Resolvable biology</span>
  <h2>Cell types &amp; states you can differentiate</h2>
  <p class="muted">Combinations of these markers assign single-cell identity and functional state across every major lineage.</p></div>
 <div class="grid cellgrid" id="cell-grid"></div>
</div></section>

<section id="workflow" style="background:var(--surface2)"><div class="wrap">
 <div class="sec-head"><span class="kicker">How it works</span><h2>From tissue to spatial single-cell data</h2></div>
 <div class="grid steps">
  <div class="step"><div class="n">1</div><h3>Design &amp; scope</h3><p class="muted">We pick a panel and tailor markers to your tissue, question and controls.</p></div>
  <div class="step"><div class="n">2</div><h3>Conjugate &amp; validate</h3><p class="muted">Antibodies are barcoded and validated on your tissue type with positive-control tissues.</p></div>
  <div class="step"><div class="n">3</div><h3>Image</h3><p class="muted">Cyclic CODEX/PhenoCycler imaging captures all markers on one FFPE or frozen section.</p></div>
  <div class="step"><div class="n">4</div><h3>Analyse &amp; deliver</h3><p class="muted">Segmentation, cell-type calling and neighbourhood analysis — delivered as figures + data.</p></div>
 </div>
</div></section>

<section id="contact"><div class="wrap">
 <div class="band">
  <h2>Map your tissue at single-cell resolution</h2>
  <p>Tell us your tissue, disease and the populations you need to resolve — we will propose a panel and a timeline.</p>
  <a href="mailto:spatial-core@example.org?subject=CODEX%20spatial%20proteomics%20project" class="btn">Request a panel design</a>
 </div>
</div></section>

<footer><div class="wrap foot">
 <div><div class="logo" style="font-size:1rem"><span class="dot"></span>Spatia&middot;CODEX</div>
  <div class="muted" style="margin-top:8px;max-width:48ch">CODEX / PhenoCycler spatial-proteomics services. Antibody library and panels derived from the Nolan-lab CODEX inventory.</div></div>
 <div class="muted">Panels: immuno-oncology &middot; autoimmunity &middot; myeloid &middot; NK &middot; stroma &middot; mucosal disease<br/>&copy; 2026 Spatia&middot;CODEX core. For research use only.</div>
</div></footer>

<script>
const DATA=__DATA__;
const $=s=>document.querySelector(s), ce=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
// stats
const S=DATA.stats;
[["antibodies","validated antibodies"],["cellTypes","cell types &amp; states"],["panels","ready-to-run panels"]].forEach(([k,l])=>{
 const s=ce("div","stat");s.innerHTML=`<b>${k=="cellTypes"?S[k]+"+":S[k]}</b><span>${l}</span>`;$("#stats").append(s);});
// panels
DATA.panels.forEach(p=>{
 const c=ce("div","card");
 c.innerHTML=`<h3>${p.name}</h3><p class="muted" style="margin:.3em 0 0;font-size:.95rem">${p.blurb}</p>
 <p class="app">${p.app}</p>
 <div class="metrics"><span><b>${p.targets.length}</b> markers</span><span><b>${p.cells.length}</b> cell types</span></div>`;
 const btn=ce("button","toggle",`Show ${p.targets.length} markers &amp; resolved cells ▾`);
 const rev=ce("div","reveal");
 rev.innerHTML=`<div class="lab">Markers</div><div class="chips">${p.targets.map(t=>{const a=DATA.antibodies.find(x=>x.key==t);return `<span class="chip">${a?a.target:t}</span>`}).join("")}</div>
  <div class="lab">Resolves</div><div class="chips">${p.cells.map(c=>`<span class="chip cell">${c}</span>`).join("")}</div>`;
 btn.onclick=()=>{rev.classList.toggle("open");btn.innerHTML=rev.classList.contains("open")?"Hide markers ▴":`Show ${p.targets.length} markers &amp; resolved cells ▾`};
 c.append(btn,rev);$("#panels-grid").append(c);
});
// filters + table
let active="All";
const cats=["All",...DATA.cats];
cats.forEach(cat=>{const b=ce("button","fbtn"+(cat=="All"?" active":""),cat);b.onclick=()=>{active=cat;document.querySelectorAll(".fbtn").forEach(x=>x.classList.toggle("active",x.textContent==cat));render()};$("#filters").append(b)});
function render(){
 const q=$("#q").value.trim().toLowerCase();
 const rows=DATA.antibodies.filter(a=>(active=="All"||a.cat==active)&&(!q||a.target.toLowerCase().includes(q)||a.cells.join(" ").toLowerCase().includes(q)||a.cat.toLowerCase().includes(q)));
 $("#rows").innerHTML=rows.map(a=>`<tr><td><b>${a.target}</b></td><td><span class="cat">${a.cat}</span></td><td class="cells">${a.cells.join(" &middot; ")}</td></tr>`).join("");
 $("#count").textContent=`${rows.length} of ${DATA.antibodies.length} antibodies`;
}
$("#q").addEventListener("input",render); render();
// cell type groups
DATA.groups.forEach(g=>{
 if(!g.cells.length) return;
 const c=ce("div","lin");
 c.innerHTML=`<h3>${g.name}</h3><ul>${g.cells.map(c=>`<li><span>${c.name}</span><span class="mk">${c.markers.slice(0,4).join(", ")}</span></li>`).join("")}</ul>`;
 $("#cell-grid").append(c);
});
</script>
</body></html>'''
html=html.replace("__DATA__",DATA).replace("__NAB__",str(inject["stats"]["antibodies"])).replace("__NCT__",str(inject["stats"]["cellTypes"])).replace("__NPAN__",str(inject["stats"]["panels"]))
# fix a stray css typo
html=html.replace("--line:#243консоль; ","")
open("index.html","w").write(html)
print("index.html bytes:",len(html))
