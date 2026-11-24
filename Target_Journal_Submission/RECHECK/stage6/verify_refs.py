"""Re-verify every BibTeX entry with a DOI against Crossref (DataCite fallback): title similarity, year, first author."""
import re, json, csv, sys, urllib.request, urllib.parse, difflib, glob
def bib_entries(path):
    txt = open(path).read(); i = 0
    while True:
        j = txt.find("@", i)
        if j < 0: return
        b = txt.find("{", j); key_end = txt.find(",", b); depth = 0; k = b
        while k < len(txt):
            depth += txt[k] == "{"; depth -= txt[k] == "}"
            if depth == 0: break
            k += 1
        body = txt[key_end + 1:k]; f = {}
        for m in re.finditer(r"(\w+)\s*=\s*", body):
            p = m.end()
            if p < len(body) and body[p] == "{":
                d, q = 0, p
                while q < len(body):
                    d += body[q] == "{"; d -= body[q] == "}"
                    if d == 0: break
                    q += 1
                f.setdefault(m.group(1).lower(), body[p + 1:q])
            else:
                f.setdefault(m.group(1).lower(), re.match(r"[^,]*", body[p:]).group(0).strip().strip('"'))
        yield txt[b + 1:key_end].strip(), f
        i = k + 1
def norm(s): return re.sub(r"[^a-z0-9 ]", "", re.sub(r"[{}\\]", "", s.lower()))
rows = []
for path in glob.glob("../../manuscript/*.bib"):
    for key, f in bib_entries(path):
        doi = f.get("doi", ""); st = {}; 
        if doi:
            try:
                d = json.load(urllib.request.urlopen("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=30))["message"]
                t = (d.get("title") or [""])[0]; y = (d.get("issued", {}).get("date-parts") or [[None]])[0][0]
                a = (d.get("author") or [{}])[0].get("family", ""); src = "crossref"
            except Exception:
                try:
                    d = json.load(urllib.request.urlopen("https://api.datacite.org/dois/" + urllib.parse.quote(doi), timeout=30))["data"]["attributes"]
                    t = d["titles"][0]["title"]; y = d.get("publicationYear"); a = (d.get("creators") or [{}])[0].get("familyName", ""); src = "datacite"
                except Exception as e:
                    t = y = a = ""; src = "NOT_FOUND"
            sim = difflib.SequenceMatcher(None, norm(f.get("title", "")), norm(t)).ratio() if t else 0
            st = dict(found_title=t, found_year=y, found_first_author=a, source=src, title_sim=round(sim, 3),
                      year_ok=str(y) == f.get("year", "").strip(), author_ok=bool(a) and norm(a) in norm(f.get("author", "")))
        else:
            st = dict(source="NO_DOI")
        rows.append(dict(bib=path.split("/")[-1], key=key, doi=doi, title=f.get("title", ""), year=f.get("year", ""), **st))
w = csv.DictWriter(open("reference_verification_v2.csv", "w"), fieldnames=sorted({k for r in rows for k in r}, key=lambda k: list(rows[0]).index(k) if k in rows[0] else 99))
w.writeheader(); w.writerows(rows)
bad = [r for r in rows if r.get("source") in ("NOT_FOUND", "NO_DOI") or r.get("title_sim", 1) < 0.8 or not r.get("year_ok", True) or not r.get("author_ok", True)]
print(len(rows), "entries;", len(bad), "need attention")
for r in bad: print(r["key"], r.get("source"), r.get("title_sim"), r.get("year"), r.get("found_year"), r.get("found_first_author"), "|", r["title"][:70], "|", str(r.get("found_title"))[:70])
