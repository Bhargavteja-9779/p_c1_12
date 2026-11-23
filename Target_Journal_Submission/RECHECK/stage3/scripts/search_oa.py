"""OpenAlex searches for stage-3 prior-art recheck. Saves compact raw JSON per query."""
import json, sys, time, re, urllib.request, urllib.parse, hashlib, os
RAW = os.path.join(os.path.dirname(__file__), '..', 'raw', 'openalex')
os.makedirs(RAW, exist_ok=True)
UA = {'User-Agent': 'prior-art-recheck/0.1'}
def inv(ab):
    if not ab: return ''
    pos = {}
    for w, ps in ab.items():
        for p in ps: pos[p] = w
    return ' '.join(pos[i] for i in sorted(pos))
def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 + 3 * k); err = e
    raise err
def search(q, filt=None, n=25):
    p = {'search': q, 'per_page': n, 'select': 'id,doi,title,publication_year,publication_date,primary_location,abstract_inverted_index,cited_by_count,type'}
    if filt: p['filter'] = filt
    d = get('https://api.openalex.org/works?' + urllib.parse.urlencode(p))
    out = {'query': q, 'filter': filt, 'count': d['meta']['count'], 'results': []}
    for w in d['results']:
        loc = w.get('primary_location') or {}
        src = (loc.get('source') or {}).get('display_name')
        out['results'].append({'openalex': w['id'], 'doi': w.get('doi'), 'title': w.get('title'), 'year': w.get('publication_year'),
            'date': w.get('publication_date'), 'venue': src, 'type': w.get('type'), 'cites': w.get('cited_by_count'),
            'abstract': inv(w.get('abstract_inverted_index'))})
    fn = re.sub(r'[^a-z0-9]+', '_', (q + '_' + (filt or '')).lower())[:90] + '.json'
    json.dump(out, open(os.path.join(RAW, fn), 'w'), indent=1)
    return out
if __name__ == '__main__':
    qs = json.load(open(sys.argv[1]))
    for item in qs:
        q, f = (item, None) if isinstance(item, str) else item
        o = search(q, f, int(os.environ.get('N','25')))
        print(f"### {q} | {f} | count={o['count']}")
        for r in o['results']:
            print(f"  {r['year']} | {r['doi']} | {(r['title'] or '')[:110]} | {(r['venue'] or '')[:30]} | ab={len(r['abstract'])}")
        time.sleep(0.3)
