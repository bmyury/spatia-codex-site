import json
# Curated antibody metadata (in-stock, Nolan CODEX inventory). target: (full name, category, [cell types resolved])
A = {
# --- T cells ---
"CD3":("CD3","T cell",["T cell (pan)"]),
"CD4":("CD4","T cell",["T-helper cell","Monocyte/Macrophage"]),
"CD8":("CD8","T cell",["Cytotoxic T cell"]),
"CD5":("CD5","T cell",["T cell","B1 B cell"]),
"CD2":("CD2","T cell",["T cell","NK cell"]),
"CD7":("CD7","T cell",["T cell","NK cell"]),
"CD45RA":("CD45RA","T cell",["Naive T cell"]),
"CD45RO":("CD45RO","T cell",["Memory T cell"]),
"FoxP3":("FoxP3","T cell",["Regulatory T cell (Treg)"]),
"CD25":("CD25 (IL-2Rα)","Activation",["Activated / regulatory T cell"]),
"CD127":("CD127 (IL-7Rα)","T cell",["Conventional T cell","ILC"]),
"T-bet":("T-bet","Signaling",["Th1 / cytotoxic cell"]),
"GATA3":("GATA3","Signaling",["Th2 cell","ILC2"]),
"CD278":("ICOS (CD278)","Checkpoint",["Activated / follicular-helper T cell"]),
"CD185":("CXCR5 (CD185)","T cell",["Follicular-helper T cell","B cell"]),
"CXCR3":("CXCR3","T cell",["Th1 / effector T cell"]),
"CCR4":("CCR4","T cell",["Th2 / skin-homing T cell","Treg"]),
"KLRG1":("KLRG1","T cell",["Terminally-differentiated effector T/NK"]),
"CD27":("CD27","T cell",["Memory T cell","B cell"]),
"TCRgd":("TCR γδ","T cell",["γδ T cell"]),
"TCRb":("TCR β","T cell",["αβ T cell"]),
"CD137":("4-1BB (CD137)","Checkpoint",["Activated T cell"]),
"OX40":("OX40 (CD134)","Checkpoint",["Activated T cell"]),
"CD154":("CD40L (CD154)","Activation",["Activated T cell"]),
# --- Checkpoints / exhaustion ---
"PD-1":("PD-1 (CD279)","Checkpoint",["Exhausted / activated T cell"]),
"PD-L1":("PD-L1 (CD274)","Checkpoint",["Tumor cell","Myeloid cell"]),
"CD273":("PD-L2 (CD273)","Checkpoint",["Dendritic cell","Macrophage"]),
"CTLA4":("CTLA-4 (CD152)","Checkpoint",["Regulatory / activated T cell"]),
"TIM3":("TIM-3","Checkpoint",["Exhausted T cell","Myeloid cell"]),
"LAG3":("LAG-3","Checkpoint",["Exhausted T cell"]),
"VISTA":("VISTA","Checkpoint",["Myeloid cell","T cell"]),
"CD276":("B7-H3 (CD276)","Checkpoint",["Tumor cell","Myeloid cell"]),
"CD85j":("ILT2 (CD85j)","Checkpoint",["Myeloid / NK inhibitory"]),
# --- B / plasma ---
"CD19":("CD19","B cell",["B cell"]),
"CD20":("CD20","B cell",["B cell"]),
"CD22":("CD22","B cell",["B cell"]),
"CD21":("CD21","B cell",["Follicular dendritic cell","Mature B cell"]),
"CD79a":("CD79a","B cell",["B cell","Plasma cell"]),
"CD79b":("CD79b","B cell",["B cell"]),
"PAX5":("PAX5","B cell",["B cell"]),
"Bcl6":("BCL-6","B cell",["Germinal-centre B cell","Tfh cell"]),
"IgD":("IgD","B cell",["Naive B cell"]),
"IgM":("IgM","B cell",["Naive / memory B cell"]),
"IgG":("IgG","Plasma",["Class-switched B / plasma cell"]),
"CD138":("CD138 (Syndecan-1)","Plasma",["Plasma cell"]),
"MUM1":("MUM-1 / IRF4","Plasma",["Plasma cell","Activated B cell"]),
"BCMA":("BCMA","Plasma",["Plasma cell"]),
"FcRH5":("FcRH5","Plasma",["Plasma / B cell"]),
"Kappa":("Ig κ light chain","Plasma",["Plasma cell (clonality)"]),
"lambda":("Ig λ light chain","Plasma",["Plasma cell (clonality)"]),
# --- NK ---
"CD56":("CD56 (NCAM1)","NK",["NK cell","Neuroendocrine"]),
"CD57":("CD57","NK",["NK / senescent cytotoxic T cell"]),
"CD16":("CD16","NK",["NK cell","Neutrophil","Macrophage"]),
"NKG2D":("NKG2D","NK",["NK cell","Cytotoxic T cell"]),
"NKp46":("NKp46 (NCR1)","NK",["NK cell"]),
"KIR":("KIR","NK",["NK cell"]),
"DNAM1":("DNAM-1 (CD226)","NK",["NK / T cell"]),
"CD94":("CD94","NK",["NK cell"]),
"SlamF7":("SLAMF7","NK",["NK / plasma cell"]),
"CD96":("CD96 (TACTILE)","NK",["NK / T cell"]),
# --- Myeloid / DC ---
"CD68":("CD68","Myeloid",["Macrophage"]),
"CD163":("CD163","Myeloid",["M2 macrophage"]),
"CD206":("CD206 (MRC1)","Myeloid",["M2 macrophage","Dendritic cell"]),
"arg-1":("Arginase-1","Myeloid",["M2 macrophage","Granulocyte"]),
"CD14":("CD14","Myeloid",["Monocyte/Macrophage"]),
"CD11b":("CD11b","Myeloid",["Macrophage","Granulocyte","DC"]),
"CD11c":("CD11c","DC",["Dendritic cell","Macrophage"]),
"CD1c":("CD1c (BDCA-1)","DC",["cDC2"]),
"CD123":("CD123","DC",["Plasmacytoid DC","Basophil"]),
"DC-lamp":("DC-LAMP","DC",["Mature dendritic cell"]),
"XCR1":("XCR1","DC",["cDC1"]),
"IRF4":("IRF4","Signaling",["cDC2 / plasma cell"]),
"CD83":("CD83","DC",["Activated / mature DC"]),
"CD86":("CD86","DC",["Activated APC"]),
"CD40":("CD40","Activation",["APC (DC/B/macrophage)"]),
"HLADR":("HLA-DR (MHC II)","Myeloid",["Antigen-presenting cell"]),
"MHCI":("HLA-ABC (MHC I)","Other",["All nucleated cells"]),
"CD169":("CD169 (Siglec-1)","Myeloid",["Sinusoidal macrophage"]),
"CD36":("CD36","Myeloid",["Macrophage","Endothelial","Platelet"]),
"CD38":("CD38","Activation",["Plasma cell","NK / activated T cell"]),
"CD39":("CD39","Activation",["Treg","Myeloid-derived suppressor cell"]),
"CD73":("CD73 (NT5E)","Stromal",["Fibroblast","Endothelial","Treg"]),
"CD107":("CD107a (LAMP-1)","Activation",["Degranulating cytotoxic cell"]),
"MMR":("CD206 (MMR)","Myeloid",["M2 macrophage"]),
"CD63":("CD63","Myeloid",["Activated mast / myeloid cell"]),
"IRF-8":("IRF8","Signaling",["cDC1 / monocyte"]),
# --- Granulocyte / mast ---
"CD15":("CD15","Granulocyte",["Neutrophil","Eosinophil"]),
"CD66":("CD66b","Granulocyte",["Neutrophil","Eosinophil"]),
"MCT":("Mast-cell tryptase","Mast",["Mast cell"]),
"CD117":("CD117 / c-KIT","Mast",["Mast cell","Progenitor"]),
# --- Epithelial / tumor ---
"panCK":("Pan-cytokeratin","Epithelial",["Epithelial / tumor cell"]),
"CK7":("Cytokeratin-7","Epithelial",["Glandular epithelium"]),
"Keratin 8":("Cytokeratin-8","Epithelial",["Luminal epithelium"]),
"Ecad":("E-cadherin","Epithelial",["Epithelial cell"]),
"p63":("p63","Epithelial",["Basal epithelial cell"]),
"Sox2":("SOX2","Epithelial",["Basal / stem epithelial cell"]),
"MUC1":("MUC1 / EMA","Epithelial",["Glandular epithelium"]),
"muc5ac":("MUC5AC","Epithelial",["Mucinous epithelium"]),
"CD49f":("CD49f (Integrin α6)","Epithelial",["Basal / stem cell"]),
"CD104":("CD104 (Integrin β4)","Epithelial",["Basal epithelial cell"]),
"Nectin-4":("Nectin-4","Tumor",["Carcinoma cell"]),
"PAX8":("PAX8","Tumor",["Müllerian / renal / thyroid epithelium"]),
"Rab25":("Rab25","Tumor",["Epithelial / tumor cell"]),
"SF-1":("SF-1","Tumor",["Adrenocortical / gonadal cell"]),
# --- EMT / tumor-functional ---
"Vimentin":("Vimentin","Stromal",["Mesenchymal / fibroblast","Immune cell"]),
"SNAIL":("SNAIL","Tumor",["EMT tumor cell"]),
"ZEB-1":("ZEB-1","Tumor",["EMT tumor / fibroblast"]),
"cMyc":("c-Myc","Tumor",["Proliferating tumor cell"]),
"Bcat":("β-catenin","Signaling",["Epithelial / Wnt-active cell"]),
"HLA-G":("HLA-G","Checkpoint",["Trophoblast / immune-evasive tumor"]),
# --- Stroma / vasculature ---
"PDPN":("Podoplanin","Stromal",["Lymphatic endothelium","Fibroblastic reticular cell"]),
"FAP":("FAP","Stromal",["Cancer-associated fibroblast"]),
"PDGFRa":("PDGFRα","Stromal",["Fibroblast"]),
"PDGFR":("PDGFRβ","Stromal",["Pericyte","Fibroblast"]),
"DDR2":("DDR2","Stromal",["Fibroblast"]),
"CD90":("CD90 (THY1)","Stromal",["Fibroblast","Mesenchymal stem cell"]),
"Coll IV":("Collagen IV","Stromal",["Basement membrane"]),
"CD31":("CD31 (PECAM1)","Endothelial",["Endothelial cell"]),
"CD34":("CD34","Endothelial",["Endothelial cell","Progenitor"]),
"VEGFR1":("VEGFR1","Endothelial",["Endothelial cell"]),
"VEGFR2":("VEGFR2","Endothelial",["Endothelial cell"]),
"MMP-9":("MMP-9","Signaling",["Remodeling myeloid / stroma"]),
"MMP12":("MMP-12","Signaling",["Macrophage (elastase)"]),
"GAS6":("GAS6","Signaling",["Stromal / efferocytic signal"]),
"CD44":("CD44","Activation",["Activated / stem-like cell"]),
"CD54":("ICAM-1 (CD54)","Activation",["Activated endothelium / APC"]),
# --- Neural ---
"L1CAM":("L1CAM","Neural",["Neuron / neural tumor"]),
# --- Proliferation / DDR / functional ---
"Ki67":("Ki-67","Proliferation/DDR",["Proliferating cell (any lineage)"]),
"PCNA":("PCNA","Proliferation/DDR",["Proliferating cell"]),
"PARP1":("PARP-1","Proliferation/DDR",["DNA-damage / tumor cell"]),
"MRE11":("MRE11","Proliferation/DDR",["DNA-damage-response cell"]),
"SLFN11":("SLFN11","Proliferation/DDR",["DNA-damage-sensitive tumor"]),
"ARID1A":("ARID1A","Proliferation/DDR",["Tumor (SWI/SNF) cell"]),
"p16":("p16 (INK4a)","Proliferation/DDR",["Senescent / HPV+ tumor cell"]),
"FoxO1":("FoxO1","Signaling",["Stress-signaling cell"]),
# --- Signaling / cytokine ---
"pstat3":("phospho-STAT3","Signaling",["IL-6/JAK-active cell"]),
"HIF1a":("HIF-1α","Signaling",["Hypoxic cell"]),
"HIF2a":("HIF-2α","Signaling",["Hypoxic cell"]),
"TGFb":("TGF-β","Signaling",["Immunosuppressive stroma"]),
"IFNg":("IFN-γ","Signaling",["Activated Th1 / NK / CD8"]),
"CXCL10":("CXCL10","Signaling",["IFN-activated stroma / myeloid"]),
"CD69":("CD69","Activation",["Tissue-resident / recently-activated lymphocyte"]),
"CD71":("CD71 (TfR)","Proliferation/DDR",["Proliferating / erythroid cell"]),
"CD235a":("CD235a (Glycophorin A)","Other",["Erythrocyte"]),
"MICA/B":("MICA/B","NK",["Stressed / tumor cell (NKG2D ligand)"]),
"CD155":("CD155 (PVR)","Checkpoint",["Tumor / myeloid cell"]),
"CD9":("CD9","Other",["Exosome / platelet / epithelial"]),
"CD30":("CD30","Activation",["Activated T/B cell","Reed-Sternberg cell"]),
}
# panels: (id, name, blurb, application, [targets])
P = [
 ("tme","Tumor Microenvironment (Immuno-Oncology)","Map tumor, stroma and the full immune contexture with checkpoint read-outs.","Solid-tumor spatial biology, IO target discovery, responder stratification.",
  ["panCK","Ecad","Ki67","Vimentin","FAP","PDGFRa","Coll IV","CD31","CD34","PDPN","CD45","CD3","CD4","CD8","FoxP3","CD20","CD68","CD163","CD206","CD11c","CD14","HLADR","CD56","Granzyme B" if False else "CD57","PD-1","PD-L1","CTLA4","TIM3","LAG3","CD276","HIF1a","MHCI"]),
 ("checkpoint","Immune Checkpoint & T-cell Exhaustion","Dedicated co-inhibitory / co-stimulatory axis with exhausted-T-cell phenotyping.","IO combination rationale, checkpoint spatial co-expression.",
  ["CD3","CD4","CD8","CD45RO","FoxP3","PD-1","PD-L1","CD273","CTLA4","TIM3","LAG3","VISTA","CD276","CD155","CD278","CD137","OX40","CD85j","Ki67"]),
 ("autoimmune","Autoimmunity & Chronic Inflammation","Resolve pathogenic T/B populations, tertiary lymphoid structures and myeloid drivers.","Rheumatology, IBD, dermatology, transplant-rejection spatial pathology.",
  ["CD3","CD4","CD8","FoxP3","CD25","CXCR3","CCR4","CD45RA","CD45RO","CD20","CD21","CD79a","CD138","Bcl6","CD185","CD68","CD163","CD14","CD11c","HLADR","CD69","CD38","ICOS" if False else "CD278","MMP-9"]),
 ("tls","Lymphoid Architecture & Tertiary Lymphoid Structures","Delineate germinal centres, FDC networks and Tfh/B interactions.","TLS scoring, vaccine / lymphoma / IO biology.",
  ["CD3","CD4","CD8","CD20","CD21","CD23" if False else "CD27","PAX5","Bcl6","MUM1","CD138","IgD","CD185","PD-1","CD68","HLADR","Ki67"]),
 ("myeloid","Myeloid & Innate Immunity","Deep macrophage-polarisation and dendritic-cell-subset resolution.","Myeloid-targeted therapy, innate-immune spatial profiling.",
  ["CD68","CD163","CD206","arg-1","CD14","CD11b","CD11c","CD1c","CD123","XCR1","DC-lamp","CD83","CD86","CD40","HLADR","CD169","MMP12","VISTA","TIM3"]),
 ("nk","NK & Cytotoxicity","Natural-killer and cytotoxic-effector phenotyping with stress-ligand context.","NK-cell therapy, innate cytotoxicity, missing-self biology.",
  ["CD56","CD57","CD16","NKG2D","NKp46","KIR","DNAM1","CD94","SlamF7","CD96","MICA/B","T-bet","CD8","CD3"]),
 ("tumor-emt","Tumour Epithelium & EMT","Carcinoma identity, proliferation, stemness and epithelial-mesenchymal transition.","Tumour-intrinsic biology, EMT / plasticity, biomarker discovery.",
  ["panCK","CK7","Ecad","p63","Sox2","MUC1","CD49f","Nectin-4","Vimentin","SNAIL","ZEB-1","cMyc","Bcat","Ki67","PCNA","p16","PARP1","HIF1a"]),
 ("stroma","Stroma, Vasculature & Angiogenesis","Cancer-associated fibroblasts, vessels and matrix remodeling.","Anti-angiogenic / anti-fibrotic programs, stromal niches.",
  ["FAP","PDGFRa","PDGFR","DDR2","CD90","Vimentin","PDPN","Coll IV","CD31","CD34","VEGFR1","VEGFR2","MMP-9","CD73","TGFb"]),
 ("gi-mucosal","GI / Mucosal (Eosinophilic Disease)","Eosinophil, mast-cell and type-2 inflammation in epithelial mucosa.","Eosinophilic esophagitis / GI, allergic & type-2 disease.",
  ["panCK","p63","Ecad","CD15","CD66","MCT","CD117","GATA3","CD3","CD4","CD8","CD20","CD68","CD163","Vimentin","PDPN","CD31","Ki67"]),
]
# clean: remove placeholder False-filtered ghosts; keep only targets present in A
panels=[]
for pid,nm,blurb,app,ts in P:
    ts=[t for t in ts if t in A]
    # resolved cell types
    cells=[]
    for t in ts:
        for c in A[t][2]:
            if c not in cells: cells.append(c)
    panels.append({"id":pid,"name":nm,"blurb":blurb,"app":app,"targets":ts,"cells":cells})
# antibody list for catalog
abs_list=[{"target":A[k][0],"key":k,"cat":A[k][1],"cells":A[k][2]} for k in A]
abs_list.sort(key=lambda x:x["target"].lower())
# all cell types
allcells={}
for k in A:
    for c in A[k][2]:
        allcells.setdefault(c,[]).append(A[k][0])
data={"antibodies":abs_list,"panels":panels,"cellTypes":[{"name":c,"markers":sorted(set(m))} for c,m in sorted(allcells.items())],
      "stats":{"antibodies":len(abs_list),"cellTypes":len(allcells),"panels":len(panels)}}
json.dump(data,open("data.json","w"),indent=0)
print("antibodies:",len(abs_list),"| cell types:",len(allcells),"| panels:",len(panels))
print("cats:",sorted(set(a["cat"] for a in abs_list)))
