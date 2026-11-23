import json,urllib.request,urllib.parse,csv
P={"SpringerNature":"P4310319965","TaylorFrancis":"P4310320547","Wiley":"P4310320595","IET":"P4310311714"}
def get(u): return json.load(urllib.request.urlopen(u,timeout=90))
rows=[]
for name,pid in P.items():
    cur="*"
    while cur:
        u=f"https://api.openalex.org/sources?filter=host_organization_lineage:{pid},type:journal,summary_stats.2yr_mean_citedness:>4,works_count:>300&select=id,display_name,issn_l,issn,summary_stats,works_count,topics,is_oa&per-page=200&cursor={cur}"
        r=get(u)
        for s in r['results']:
            top=[t['field']['display_name'] for t in (s.get('topics') or [])[:5]]
            rows.append([name,s['display_name'],s['issn_l'],";".join(s['issn'] or []),round(s['summary_stats']['2yr_mean_citedness'],2),s['summary_stats']['h_index'],s['works_count'],"|".join(dict.fromkeys(top)),s['is_oa']])
        cur=r['meta'].get('next_cursor')
        if not r['results']: break
w=csv.writer(open('/tmp/claude-0/s/oa_sources.csv','w'));w.writerow(["pub","name","issn_l","issns","cit2y","h","works","fields","oa"]);w.writerows(rows)
print(len(rows))
