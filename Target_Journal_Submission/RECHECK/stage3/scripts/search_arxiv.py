import urllib.request, urllib.parse, sys, json, os, re, time, xml.etree.ElementTree as ET
RAW=os.path.join(os.path.dirname(__file__),'..','raw','arxiv'); os.makedirs(RAW,exist_ok=True)
ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
for q in json.load(open(sys.argv[1])):
    url='https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':q,'max_results':int(os.environ.get('N','15')),'sortBy':os.environ.get('SORT','relevance')})
    for k in range(4):
        try: x=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'prior-art-recheck/0.1'}),timeout=60).read(); break
        except Exception as e: time.sleep(5+5*k)
    root=ET.fromstring(x); tot=root.find('o:totalResults',ns).text
    res=[]
    for e in root.findall('a:entry',ns):
        res.append({'openalex':None,'doi':'https://doi.org/10.48550/arxiv.'+e.find('a:id',ns).text.split('/abs/')[-1].split('v')[0],'arxiv_id':e.find('a:id',ns).text,'title':' '.join(e.find('a:title',ns).text.split()),'year':e.find('a:published',ns).text[:4],'date':e.find('a:published',ns).text[:10],'venue':'arXiv','abstract':' '.join(e.find('a:summary',ns).text.split())})
    out={'query':q,'source':'arXiv API','count':int(tot),'results':res}
    json.dump(out,open(os.path.join(RAW,re.sub(r'[^a-z0-9]+','_',q.lower())[:90]+'.json'),'w'),indent=1)
    print('###',q,'count=',tot)
    for r in res: print('  ',r['date'],r['arxiv_id'].split('/abs/')[-1],r['title'][:110])
    time.sleep(3.5)
