import json,glob,csv,sys,os
ex=set(r['doi'].lower().replace('https://doi.org/','') for r in csv.DictReader(open('../../../journal_selection/novelty_map.csv')) if r['doi'])
seenf='seen.txt'; seen=set(open(seenf).read().split()) if os.path.exists(seenf) else set()
files=sys.argv[1:]
new=[]
for f in files:
    d=json.load(open(f)); print('###',d['query'],d.get('filter'),'count=',d['count'])
    for r in d['results']:
        k=(r['doi'] or r['openalex']).lower().replace('https://doi.org/','')
        if k in ex or k in seen: continue
        seen.add(k); new.append(k)
        print(f"  {r['year']}|{k}|{(r['title'] or '')[:100]}|{(r['venue'] or '')[:25]}|ab={len(r['abstract'])}")
open(seenf,'a').write('\n'.join(new)+'\n')
