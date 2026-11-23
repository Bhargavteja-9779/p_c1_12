import csv,json,re,time,urllib.request,urllib.parse,difflib
from new_rows import NEW
cand=json.load(open('../raw/candidates.json')); chk=json.load(open('../raw/doi_verify/existing_doi_check.json'))
UA={'User-Agent':'prior-art-recheck/0.1'}
def datacite(doi):
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request('https://api.datacite.org/dois/'+urllib.parse.quote(doi),headers=UA),timeout=60))
        json.dump(d,open('../raw/doi_verify/datacite_'+re.sub(r'[^a-z0-9]','_',doi.lower())+'.json','w'))
        return d['data']['attributes']['titles'][0]['title']
    except Exception: return None
def field(r):
    s=(r['paper']+' '+r['venue']+' '+r['problem']).lower()
    if 'district heating' in s or 'predist' in s or 'substation' in s or 'hausstation' in s: return 'DH substations'
    if 'wind' in s: return 'Wind SCADA'
    if 'hvac' in s or 'building' in s or 'radiator' in s: return 'Building HVAC FDD'
    return 'Other condition monitoring'
out=[]
for i,r in enumerate(csv.DictReader(open('../../../journal_selection/novelty_map.csv')),1):
    clo=r['closeness_0to5']; what=f"{r['problem']}. Method: {r['method']}. Data: {r['data']}. Evaluation: {r['evaluation_protocol']}."
    if 'egyai.2026.100824' in r['doi']:
        clo='3'; what+=' [stage3: OpenAlex referenced_works of this paper include the PreDist Zenodo record v1 (10.5281/zenodo.17522255), so it probably uses PreDist as one of its six datasets; abstract reports cross-substation transfer within a network and asymmetric transfer across networks. Closeness raised 2->3. Full text needed.]'
    src='prior session (journal_selection): input candidates / OpenAlex abstract' if not r['problem'].startswith('not stated') else 'none (abstract not available)'
    out.append({'id':f'E{i:02d}','doi':r['doi'].replace('https://doi.org/',''),'title':r['paper'],'year':r['year'],'venue':r['venue'],'field':field(r),
        'closeness':clo,'what_they_do':what,'how_we_differ':r['how_ours_differs'],'source_of_abstract':src,'doi_verified':chk[r['paper']][0],
        'search_query':'prior session queries (journal_selection/novelty_map_summary.md)'})
for j,(k,f,c,w,h,q) in enumerate(NEW,1):
    rec=cand[k]; doi=rec.get('doi') or ''
    if k.startswith('https://openalex.org/'): doi=''; dv='no DOI (OpenAlex record '+k.split('/')[-1]+')'
    elif rec.get('crossref')=='yes':
        sim=difflib.SequenceMatcher(None,re.sub(r'\W','',rec.get('cr_title','').lower()),re.sub(r'\W','',rec['title'].lower())).ratio()
        dv=f'yes (Crossref, title match {sim:.2f})'
    else:
        t=datacite(doi); time.sleep(0.2)
        dv=f'yes (DataCite)' if t else 'no (not found in Crossref or DataCite)'
    src=rec.get('abs_src') or 'none'
    if not rec.get('abstract'): src='none (abstract not retrieved)'
    if k.startswith('https://openalex.org/') and rec.get('abstract'): src='OpenAlex (repository record)'
    out.append({'id':f'N{j:02d}','doi':doi,'title':rec['title'],'year':rec.get('year'),'venue':rec.get('venue') or '','field':f,'closeness':'NA' if c is None else c,
        'what_they_do':w,'how_we_differ':h,'source_of_abstract':src,'doi_verified':dv,'search_query':q})
# duplicate check
dois=[o['doi'].lower() for o in out if o['doi']]; assert len(dois)==len(set(dois)),[d for d in dois if dois.count(d)>1]
titles=[o['title'].lower() for o in out]; assert len(titles)==len(set(titles))
with open('../novelty_map_v2.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out)); 
from collections import Counter; print(Counter(str(o['closeness']) for o in out)); print(Counter(o['doi_verified'].split(' (')[0] for o in out))
