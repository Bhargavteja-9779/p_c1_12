import json,glob,sys
want=[w.lower() for w in sys.argv[1:]]
done=set()
for f in glob.glob('../raw/*/*.json'):
    try: d=json.load(open(f))
    except: continue
    for r in d.get('results',[]):
        k=(r.get('doi') or r.get('openalex') or '').lower()
        for w in want:
            if w in k and w not in done:
                done.add(w); print('=====',r.get('doi'),r.get('openalex'),'|',r['title'],'|',r['year'],r.get('date'),'|',r['venue'],'| Q:',d['query']); print(r['abstract'][:1800]); print()
print('missing',set(want)-done)
