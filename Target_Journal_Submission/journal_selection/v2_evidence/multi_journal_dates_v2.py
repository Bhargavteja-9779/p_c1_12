"""Received->accepted days for journals whose dates are not in Crossref, from repository copies of the
published PDF (OpenAlex non-publisher pdf_url). Articles published 2025-05-23..2026-11-23."""
import json, urllib.request, urllib.parse, csv, re, os, sys, datetime as dt
from pypdf import PdfReader
M = "January February March April May June July August September October November December".split()
pat = r"(\d{1,2})\s+(%s)\s+(\d{4})" % "|".join(M)
def find(label, txt):
    m = re.search(label + r"[^0-9]{0,40}" + pat, txt, re.I)
    return dt.date(int(m.group(3)), M.index(m.group(2).capitalize()) + 1, int(m.group(1))) if m else None
def get(url): return json.load(urllib.request.urlopen(url, timeout=60))
names = sys.argv[1:]
out = []
for name in names:
    s = get("https://api.openalex.org/sources?search=" + urllib.parse.quote(name) + "&per-page=5")["results"]
    s = [x for x in s if x["display_name"].lower() == name.lower()] or s
    src = s[0]; sid = src["id"].split("/")[-1]; print("==", src["display_name"], sid, src.get("host_organization_name"), flush=True)
    cand = []
    for page in range(1, 15):
        d = get(f"https://api.openalex.org/works?filter=primary_location.source.id:{sid},from_publication_date:2025-05-23,"
                f"type:article&per-page=200&page={page}&select=doi,publication_date,locations")
        if not d["results"]: break
        for w in d["results"]:
            p = [l["pdf_url"] for l in w["locations"] if l.get("pdf_url") and not re.search("sciencedirect|elsevier|arxiv|doi.org|researchgate", l["pdf_url"])]
            if p: cand.append((w["doi"], w["publication_date"], p[0]))
    n_ok = 0
    for doi, date, url in cand[:80]:
        fn = os.environ["PDFDIR"] + "/" + re.sub(r"\W", "_", doi[-34:]) + ".pdf"; rec = acc = None; st = "ok"
        try:
            if not os.path.exists(fn):
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
                open(fn, "wb").write(urllib.request.urlopen(req, timeout=40).read())
            txt = re.sub(r"\s+", " ", " ".join((p.extract_text() or "") for p in PdfReader(fn).pages[:2]))
            rec, acc = find("Received", txt), find("Accepted", txt)
        except Exception as e: st = "error:" + type(e).__name__
        days = (acc - rec).days if rec and acc else ""
        n_ok += days != ""
        out.append(dict(journal=src["display_name"], doi=doi, pub_date=date, received=rec or "", accepted=acc or "", days=days, status=st))
        if n_ok >= 30: break
    print(name, "candidates", len(cand), "dated", n_ok, flush=True)
    w = csv.DictWriter(open(os.environ["OUTCSV"], "w"), fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
