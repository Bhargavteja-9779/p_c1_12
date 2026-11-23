"""Fetch records by DOI / OpenAlex id / arXiv id from OpenAlex, Crossref, arXiv. Saves raw JSON."""
import json, sys, os, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
B=os.path.join(os.path.dirname(__file__),'..','raw'); UA={'User-Agent':'prior-art-recheck/0.1 (mailto:none)'}
def get(url, js=True):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60) as r:
                b=r.read(); return json.loads(b) if js else b
        except urllib.error.HTTPError as e:
            if e.code==404: return None
            time.sleep(3+3*k)
        except Exception: time.sleep(3+3*k)
    return 'ERROR'
def inv(ab):
    if not ab: return ''
    pos={p:w for w,ps in ab.items() for p in ps}; return ' '.join(pos[i] for i in sorted(pos))
def safe(s): return re.sub(r'[^a-z0-9]+','_',s.lower())[:80]
def crossref(doi):
    d=get('https://api.crossref.org/works/'+urllib.parse.quote(doi))
    os.makedirs(B+'/crossref',exist_ok=True)
    if isinstance(d,dict): json.dump(d['message'],open(f'{B}/crossref/{safe(doi)}.json','w'))
    return d
def openalex(key):
    d=get('https://api.openalex.org/works/'+(key if key.startswith('http') and 'openalex' in key else 'doi:'+key))
    os.makedirs(B+'/openalex_works',exist_ok=True)
    if isinstance(d,dict):
        d={k:d.get(k) for k in ['id','doi','title','publication_year','publication_date','primary_location','abstract_inverted_index','type','referenced_works','authorships']}
        json.dump(d,open(f'{B}/openalex_works/{safe(key)}.json','w'))
    return d
def arxiv(aid):
    x=get('https://export.arxiv.org/api/query?id_list='+aid,js=False); time.sleep(3)
    ns={'a':'http://www.w3.org/2005/Atom'}; e=ET.fromstring(x).find('a:entry',ns)
    r={'id':aid,'title':' '.join(e.find('a:title',ns).text.split()),'date':e.find('a:published',ns).text[:10],'abstract':' '.join(e.find('a:summary',ns).text.split())}
    os.makedirs(B+'/arxiv_ids',exist_ok=True); json.dump(r,open(f'{B}/arxiv_ids/{safe(aid)}.json','w')); return r
out={}
for key in sys.argv[2:]:
    rec={'key':key}
    if re.match(r'^\d{4}\.\d{4,5}$',key):
        a=arxiv(key); rec.update(title=a['title'],year=a['date'][:4],venue='arXiv',abstract=a['abstract'],abs_src='arXiv API',doi='10.48550/arXiv.'+key)
        c=crossref('10.48550/arXiv.'+key); rec['crossref']='yes' if isinstance(c,dict) else ('404' if c is None else 'error')
        o=openalex('10.48550/arxiv.'+key)
        if isinstance(o,dict) and o.get('primary_location'): pass
    else:
        o=openalex(key); 
        if isinstance(o,dict):
            loc=o.get('primary_location') or {}
            rec.update(title=o['title'],year=o['publication_year'],venue=(loc.get('source') or {}).get('display_name'),abstract=inv(o.get('abstract_inverted_index')),abs_src='OpenAlex',doi=(o.get('doi') or '').replace('https://doi.org/',''))
        doi=rec.get('doi') or ('' if key.startswith('http') else key)
        if doi:
            c=crossref(doi); rec['crossref']='yes' if isinstance(c,dict) else ('404' if c is None else 'error')
            if isinstance(c,dict):
                rec['cr_title']=(c['message'].get('title') or [''])[0]
                rec.setdefault('title',rec['cr_title']); rec.setdefault('venue',(c['message'].get('container-title') or [''])[0])
                if not rec.get('abstract') and c['message'].get('abstract'):
                    rec['abstract']=re.sub('<[^>]+>',' ',c['message']['abstract']); rec['abs_src']='Crossref'
    out[key]=rec; time.sleep(0.2)
    print(key,'|',rec.get('crossref'),'|',(rec.get('title') or '')[:80],'| ab',len(rec.get('abstract') or ''),rec.get('abs_src'))
prev=json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
prev.update(out); json.dump(prev,open(sys.argv[1],'w'),indent=1)
