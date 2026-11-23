import csv,json,re,os,time,urllib.request,urllib.parse,difflib
B='../raw/doi_verify'; os.makedirs(B,exist_ok=True)
UA={'User-Agent':'prior-art-recheck/0.1'}
def get(u):
    for k in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code==404: return None
        except Exception: pass
        time.sleep(3)
    return 'ERR'
def norm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
res={}
rows=list(csv.DictReader(open('../../../journal_selection/novelty_map.csv')))
for r in rows:
    doi=r['doi'].replace('https://doi.org/','').strip()
    if not doi: res[r['paper']]=('no DOI','',''); continue
    c=get('https://api.crossref.org/works/'+urllib.parse.quote(doi)); src='Crossref'; t=''
    if isinstance(c,dict): t=(c['message'].get('title') or [''])[0]
    else:
        d=get('https://api.datacite.org/dois/'+urllib.parse.quote(doi)); src='DataCite'
        if isinstance(d,dict): t=(d['data']['attributes'].get('titles') or [{}])[0].get('title','')
        else: src='none'
    sim=difflib.SequenceMatcher(None,norm(t)[:120],norm(r['paper'])[:120]).ratio() if t else 0
    v=f'yes ({src}, title match {sim:.2f})' if sim>0.8 else (f'CHECK ({src} title differs: {t[:80]})' if t else 'no (DOI not found in Crossref or DataCite)')
    res[r['paper']]=(v,src,t); print(v,'|',doi)
    time.sleep(0.2)
json.dump(res,open(B+'/existing_doi_check.json','w'),indent=1)
