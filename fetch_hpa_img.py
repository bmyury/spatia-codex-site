import json, requests, re, os, time
d=json.load(open("enrich.json"))
H={"User-Agent":"Mozilla/5.0"}
done=0; ok=0
state=json.load(open("imgmap.json")) if os.path.exists("imgmap.json") else {}
for k,rec in d.items():
    if k in state: continue
    ensg=rec.get("ensembl",""); gene=rec.get("gene","")
    if not ensg or not gene: state[k]={"img":"","page":""}; continue
    page=f"https://www.proteinatlas.org/{ensg}-{gene}"
    url=f"{page}/tissue"
    img=""
    try:
        h=requests.get(url,headers=H,timeout=30).text
        cands=re.findall(r'(?:src|data-src)="//(images\.proteinatlas\.org/\d+/[0-9A-Za-z_]+_(?:selected_)?medium\.jpg)"',h)
        cands=[c for c in cands if "_rna_" not in c]
        if cands:
            iu="https://"+cands[0]
            b=requests.get(iu,headers=H,timeout=30).content
            if len(b)>6000 and b[:2]==b"\xff\xd8":
                open(f"img/{k.replace('/','_')}.jpg","wb").write(b); img=f"img/{k.replace('/','_')}.jpg"; ok+=1
    except Exception as e: pass
    state[k]={"img":img,"page":page}
    done+=1
    if done%15==0:
        json.dump(state,open("imgmap.json","w")); print(f"  {done} done, {ok} images",flush=True)
    time.sleep(0.1)
json.dump(state,open("imgmap.json","w"))
print(f"DONE: {ok} HPA images fetched of {len(state)} markers")
