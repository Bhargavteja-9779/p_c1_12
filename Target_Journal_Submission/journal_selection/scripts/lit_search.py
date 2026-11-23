"""OpenAlex literature search helper: python lit_search.py "query" [n] [from_year] -> prints and appends to lit_raw.csv"""
import subprocess,json,urllib.parse,sys,csv,os
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 25; fy=sys.argv[3] if len(sys.argv)>3 else "2015"
u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+f"&filter=publication_year:>{int(fy)-1}"
   f"&per-page={n}&sort=relevance_score:desc&select=id,doi,title,publication_year,primary_location,cited_by_count,abstract_inverted_index")
d=json.loads(subprocess.run(["curl","-s","-m","60",u],capture_output=True,text=True).stdout)
new=not os.path.exists("lit_raw.csv"); w=csv.writer(open("lit_raw.csv","a"))
if new: w.writerow(["query","openalex","doi","year","venue","cites","title","abstract"])
for x in d.get('results',[]):
    v=((x.get('primary_location') or {}).get('source') or {}).get('display_name')
    ii=x.get('abstract_inverted_index') or {}; ab=' '.join(k for _,k in sorted((p,k) for k,vv in ii.items() for p in vv))
    w.writerow([q,x['id'],x['doi'],x['publication_year'],v,x['cited_by_count'],x['title'],ab[:3000]])
    print(x['publication_year'],'|',v,'|',x['cited_by_count'],'|',(x['title'] or '')[:140])
