"""List candidate journals (Springer Nature, T&F, Wiley, IET) with OpenAlex 2-yr mean citedness > 4.
2-yr mean citedness is only a PROXY for Impact Factor; JCR values are verified separately."""
import json,subprocess,csv,time
P={"SpringerNature":"P4310319965","TaylorFrancis":"P4310320547","Wiley":"P4310320595","IET":"P4310311714"}
def get(u):
    out=subprocess.run(["curl","-s","-m","90",u],capture_output=True,text=True).stdout
    return json.loads(out)
rows=[]
for name,pid in P.items():
    page=1; n=0
    while True:
        u=(f"https://api.openalex.org/sources?filter=host_organization_lineage:{pid},type:journal,"
           f"summary_stats.2yr_mean_citedness:%3E4&select=id,display_name,issn_l,issn,summary_stats,works_count"
           f"&per-page=200&page={page}")
        try: r=get(u)
        except Exception as e: print(name,"stopped at page",n,e); break
        n+=1; time.sleep(0.3)
        if 'results' not in r: print(name,r); break
        for s in r['results']:
            rows.append([name,s['display_name'],s['issn_l'],";".join(s['issn'] or []),
                         round(s['summary_stats']['2yr_mean_citedness'],2),s['summary_stats']['h_index'],s['works_count']])
        page+=1
        if len(r.get('results',[]))<200: break
w=csv.writer(open('oa_sources.csv','w'));w.writerow(["pub","name","issn_l","issns","cit2y","h","works"]);w.writerows(rows)
print(len(rows))
