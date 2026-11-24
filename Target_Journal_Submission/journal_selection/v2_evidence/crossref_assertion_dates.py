import json,urllib.request,urllib.parse,sys,csv,statistics as st,datetime as dt
out=csv.writer(open(sys.argv[1],'w')); out.writerow(['journal','issn','doi','published','received','accepted','days'])
for spec in sys.argv[2:]:
    name,issn=spec.split('|')
    u=f"https://api.crossref.org/journals/{issn}/works?filter=from-pub-date:2024-11-24,type:journal-article&sample=100&select=DOI,assertion,published,title&mailto=research@example.org"
    try: items=json.load(urllib.request.urlopen(u,timeout=90))['message']['items']
    except Exception as e: print(name,'ERR',e); continue
    ds=[]
    for it in items:
        a={x.get('name'):x.get('value') for x in it.get('assertion',[])}
        r=a.get('received'); c=a.get('accepted')
        if not(r and c): continue
        try: d=(dt.date.fromisoformat(c[:10])-dt.date.fromisoformat(r[:10])).days
        except Exception: continue
        p=it.get('published',{}).get('date-parts',[[None]])[0]
        out.writerow([name,issn,it['DOI'],'-'.join(map(str,p)),r[:10],c[:10],d]); ds.append(d)
    if ds: print(name,len(items),len(ds),st.median(ds),min(ds),max(ds),flush=True)
    else: print(name,len(items),0,flush=True)
