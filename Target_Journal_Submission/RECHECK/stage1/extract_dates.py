"""Download repository PDFs of Energy and AI articles and parse 'Received'/'Accepted' dates from page 1."""
import csv, re, os, io, urllib.request, datetime as dt
from pypdf import PdfReader
M = "January February March April May June July August September October November December".split()
pat = r"(\d{1,2})\s+(%s)\s+(\d{4})" % "|".join(M)
def find(label, txt):
    m = re.search(label + r"[^0-9]{0,40}" + pat, txt, re.I)
    return dt.date(int(m.group(3)), M.index(m.group(2).capitalize()) + 1, int(m.group(1))) if m else None
out = []
for r in csv.DictReader(open("egyai_oa_locations.csv")):
    if not r["pdf"] or "arxiv.org" in r["pdf"]: continue
    fn = "pdfs/" + re.sub(r"\W", "_", r["doi"][-30:]) + ".pdf"
    st = "ok"
    try:
        if not os.path.exists(fn):
            req = urllib.request.Request(r["pdf"], headers={"User-Agent": "Mozilla/5.0 (research script)"})
            open(fn, "wb").write(urllib.request.urlopen(req, timeout=60).read())
        txt = " ".join((p.extract_text() or "") for p in PdfReader(fn).pages[:2])
        txt = re.sub(r"\s+", " ", txt)
        rec, acc = find("Received", txt), find("Accepted", txt)
    except Exception as e:
        rec = acc = None; st = "error:" + type(e).__name__
    days = (acc - rec).days if rec and acc else ""
    out.append(dict(doi=r["doi"], pub_date=r["date"], pdf=r["pdf"], received=rec or "", accepted=acc or "", days=days, status=st))
    print(r["doi"], rec, acc, days, st, flush=True)
w = csv.DictWriter(open("egyai_dates_from_pdfs.csv", "w"), fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
