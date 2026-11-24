"""List Energy and AI articles (2025-06..2026-11) whose OpenAlex record has a non-ScienceDirect PDF copy."""
import json, urllib.request, csv, sys
src = "2666-5468"
rows = []
for page in range(1, 30):
    url = (f"https://api.openalex.org/works?filter=primary_location.source.issn:{src},"
           f"from_publication_date:2025-06-01,type:article&per-page=200&page={page}"
           "&select=id,doi,title,publication_date,locations")
    d = json.load(urllib.request.urlopen(url, timeout=60))
    if not d["results"]: break
    for w in d["results"]:
        pdfs = [l.get("pdf_url") for l in w["locations"] if l.get("pdf_url") and "sciencedirect" not in l["pdf_url"] and "elsevier" not in l["pdf_url"]]
        rows.append(dict(doi=w["doi"], date=w["publication_date"], title=w["title"], n_alt_pdf=len(pdfs), pdf=pdfs[0] if pdfs else ""))
w = csv.DictWriter(open("egyai_oa_locations.csv", "w"), fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows), "articles;", sum(r["n_alt_pdf"] > 0 for r in rows), "with non-ScienceDirect PDF")
