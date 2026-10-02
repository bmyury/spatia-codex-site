import json, requests, time, re, gzip, os
d=json.load(open("data.json"))
keys=[a["key"] for a in d["antibodies"]]
GENE={
"CD3":"CD3E","CD4":"CD4","CD8":"CD8A","CD5":"CD5","CD2":"CD2","CD7":"CD7","CD45RA":"PTPRC","CD45RO":"PTPRC","FoxP3":"FOXP3","CD25":"IL2RA","CD127":"IL7R","T-bet":"TBX21","GATA3":"GATA3","CD278":"ICOS","CD185":"CXCR5","CXCR3":"CXCR3","CCR4":"CCR4","KLRG1":"KLRG1","CD27":"CD27","TCRgd":"TRGC1","TCRb":"TRBC1","CD137":"TNFRSF9","OX40":"TNFRSF4","CD154":"CD40LG","PD-1":"PDCD1","PD-L1":"CD274","CD273":"PDCD1LG2","CTLA4":"CTLA4","TIM3":"HAVCR2","LAG3":"LAG3","VISTA":"VSIR","CD276":"CD276","CD85j":"LILRB1",
"CD19":"CD19","CD20":"MS4A1","CD22":"CD22","CD21":"CR2","CD79a":"CD79A","CD79b":"CD79B","PAX5":"PAX5","Bcl6":"BCL6","IgD":"IGHD","IgM":"IGHM","IgG":"IGHG1","CD138":"SDC1","MUM1":"IRF4","BCMA":"TNFRSF17","FcRH5":"FCRL5","Kappa":"IGKC","lambda":"IGLC1",
"CD56":"NCAM1","CD57":"B3GAT1","CD16":"FCGR3A","NKG2D":"KLRK1","NKp46":"NCR1","KIR":"KIR2DL3","DNAM1":"CD226","CD94":"KLRD1","SlamF7":"SLAMF7","CD96":"CD96",
"CD68":"CD68","CD163":"CD163","CD206":"MRC1","arg-1":"ARG1","CD14":"CD14","CD11b":"ITGAM","CD11c":"ITGAX","CD1c":"CD1C","CD123":"IL3RA","DC-lamp":"LAMP3","XCR1":"XCR1","IRF4":"IRF4","CD83":"CD83","CD86":"CD86","CD40":"CD40","HLADR":"HLA-DRA","MHCI":"HLA-A","CD169":"SIGLEC1","CD36":"CD36","CD38":"CD38","CD39":"ENTPD1","CD73":"NT5E","CD107":"LAMP1","MMR":"MRC1","CD63":"CD63","IRF-8":"IRF8",
"CD15":"FUT4","CD66":"CEACAM8","MCT":"TPSAB1","CD117":"KIT",
"panCK":"KRT8","CK7":"KRT7","Keratin 8":"KRT8","Ecad":"CDH1","p63":"TP63","Sox2":"SOX2","MUC1":"MUC1","muc5ac":"MUC5AC","CD49f":"ITGA6","CD104":"ITGB4","Nectin-4":"NECTIN4","PAX8":"PAX8","Rab25":"RAB25","SF-1":"NR5A1",
"Vimentin":"VIM","SNAIL":"SNAI1","ZEB-1":"ZEB1","cMyc":"MYC","Bcat":"CTNNB1","HLA-G":"HLA-G",
"PDPN":"PDPN","FAP":"FAP","PDGFRa":"PDGFRA","PDGFR":"PDGFRB","DDR2":"DDR2","CD90":"THY1","Coll IV":"COL4A1","CD31":"PECAM1","CD34":"CD34","VEGFR1":"FLT1","VEGFR2":"KDR","MMP-9":"MMP9","MMP12":"MMP12","GAS6":"GAS6","CD44":"CD44","CD54":"ICAM1","L1CAM":"L1CAM",
"Ki67":"MKI67","PCNA":"PCNA","PARP1":"PARP1","MRE11":"MRE11","SLFN11":"SLFN11","ARID1A":"ARID1A","p16":"CDKN2A","FoxO1":"FOXO1","pstat3":"STAT3","HIF1a":"HIF1A","HIF2a":"EPAS1","TGFb":"TGFB1","IFNg":"IFNG","CXCL10":"CXCL10","CD69":"CD69","CD71":"TFRC","CD235a":"GYPA","MICA/B":"MICA","CD155":"PVR","CD9":"CD9","CD30":"TNFRSF8",
}
# search synonyms for literature query (string already includes the target symbol)
def syn(k,target,gene):
    s={k,target.split(" ")[0],gene}
    s.add(target.replace(" ","").replace("/",""))
    return [x for x in s if x and len(x)>1]
MOD='("imaging mass cytometry" OR Hyperion OR CODEX OR PhenoCycler OR CyCIF OR "cyclic immunofluorescence" OR MIBI OR "multiplexed ion beam")'
EPMC="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
HPA="https://www.proteinatlas.org/api/search_download.php"
cache=json.load(open("enrich.json")) if os.path.exists("enrich.json") else {}
abmap={a["key"]:a for a in d["antibodies"]}
for i,k in enumerate(keys):
    if k in cache: continue
    a=abmap[k]; gene=GENE.get(k,"")
    rec={"gene":gene,"ensembl":"","tissue":"","refs":[]}
    # HPA
    if gene:
        try:
            r=requests.get(HPA,params={"search":gene,"format":"tsv","columns":"g,eg,rnats,rnatsm,rnascsm"},timeout=25)
            raw=r.content; txt=gzip.decompress(raw).decode("utf-8","ignore") if raw[:2]==b"\x1f\x8b" else r.text
            for ln in txt.splitlines()[1:]:
                f=ln.split("\t")
                if f and f[0]==gene:
                    rec["ensembl"]=f[1] if len(f)>1 else ""
                    rec["tissue"]=(f[3].strip('"') if len(f)>3 else "") or (f[4].strip('"').split(";")[0] if len(f)>4 else "")
                    break
        except Exception as e: rec["hpa_err"]=str(e)[:40]
    # Europe PMC refs
    terms=" OR ".join(f'"{s}"' if " " in s else s for s in syn(k,a["target"],gene))
    q=f'({terms}) AND {MOD} AND (OPEN_ACCESS:y) AND (HAS_FT:y)'
    try:
        r=requests.get(EPMC,params={"query":q,"format":"json","pageSize":5,"resultType":"lite","sort":"CITED desc"},timeout=30).json()
        for x in r.get("resultList",{}).get("result",[])[:4]:
            rec["refs"].append({"pmid":x.get("pmid",""),"pmcid":x.get("pmcid",""),"title":x.get("title","")[:180],
              "journal":x.get("journalTitle","")[:40],"year":x.get("pubYear",""),"doi":x.get("doi","")})
        rec["hits"]=r.get("hitCount",0)
    except Exception as e: rec["ref_err"]=str(e)[:40]
    cache[k]=rec
    if i%15==0:
        json.dump(cache,open("enrich.json","w"))
        print(f"  {i}/{len(keys)} {k} gene={gene} ensg={rec['ensembl']} refs={len(rec['refs'])} hits={rec.get('hits',0)}",flush=True)
    time.sleep(0.15)
json.dump(cache,open("enrich.json","w"))
nref=sum(1 for k in cache if cache[k]["refs"])
nens=sum(1 for k in cache if cache[k]["ensembl"])
print(f"DONE {len(cache)} markers | with refs: {nref} | with ensembl: {nens}")
