"""For each candidate journal, take a random sample (Crossref `sample=100`) of research articles published
in the last 18 months and compute received->accepted days from publisher-deposited Article History.
Writes per-article rows to acceptance_scan_articles.csv and per-journal stats to acceptance_scan_summary.csv.
Limitation: only accepted (published) papers are visible -> survivorship bias; rejected papers are unseen."""
import json,subprocess,csv,sys,time,os
import pandas as pd, numpy as np
from datetime import datetime
FROM="2025-05-23"
def parse(v):
    for f in ("%d %B %Y","%Y-%m-%d","%d %b %Y","%B %d, %Y"):
        try: return datetime.strptime(v.strip(),f)
        except Exception: pass
    return None
def fetch(issn):
    u=(f"https://api.crossref.org/works?filter=issn:{issn},from-pub-date:{FROM},type:journal-article"
       f"&sample=100&select=DOI,title,assertion&mailto=")
    u=u.replace("&mailto=","")
    for k in range(3):
        try:
            out=subprocess.run(["curl","-s","-m","120",u],capture_output=True,text=True).stdout
            return json.loads(out)['message']['items']
        except Exception: time.sleep(3)
    return None
cand=pd.read_csv(sys.argv[1]); outA='acceptance_scan_articles.csv'; outS='acceptance_scan_summary.csv'
done=set(pd.read_csv(outS).issn_l) if os.path.exists(outS) else set()
fa=open(outA,'a',newline=''); fs=open(outS,'a',newline='')
wa=csv.writer(fa); ws=csv.writer(fs)
if not done: wa.writerow(["journal","issn_l","title","doi","received","accepted","days"]); ws.writerow(["pub","journal","issn_l","cit2y","n_sampled","n_dated","median","p75","p90","max"])
for _,r in cand.iterrows():
    if r.issn_l in done: continue
    items=fetch(r.issn_l); time.sleep(0.5)
    if items is None: ws.writerow([r.pub,r['name'],r.issn_l,r.cit2y,-1,0,"","","",""]); continue
    days=[]
    for it in items:
        a={x.get('name'):x.get('value') for x in it.get('assertion',[])}
        if 'received' in a and 'accepted' in a:
            rv,ac=parse(a['received']),parse(a['accepted'])
            if rv and ac:
                d=(ac-rv).days; days.append(d)
                wa.writerow([r['name'],r.issn_l,(it.get('title') or [''])[0][:200],it['DOI'],rv.date(),ac.date(),d])
    if days:
        x=np.array(days); ws.writerow([r.pub,r['name'],r.issn_l,r.cit2y,len(items),len(x),np.median(x),np.percentile(x,75),np.percentile(x,90),x.max()])
    else: ws.writerow([r.pub,r['name'],r.issn_l,r.cit2y,len(items),0,"","","",""])
    fa.flush(); fs.flush()
