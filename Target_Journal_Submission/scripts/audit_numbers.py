#!/usr/bin/env python3
"""G11 integrity audit: every number in the manuscript must match a value in a result file.
Usage: python scripts/audit_numbers.py [paper/manuscript.md]
A manuscript number matches if some result value rounds to it at the number's printed precision, directly, as a
percentage (x100), or as an integer count. Numbers that are not results (years, section/figure/table numbers,
reference numbers, DOIs, hyper-parameters stated in the method) must be listed in paper/audit_allow.txt as
'<number> | <reason>' lines; the allow-list is itself part of the audit output. Exit code 1 on any mismatch."""
import csv, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paper = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "manuscript.md")
SRC = [p for g in ("code/results/**/*.csv", "code/results/**/*.json", "literature/*.csv", "journal_selection/*.csv",
                   "RECHECK/stage1/*.csv", "results/*.json", "results/*.csv", "tables/*.csv")
       for p in glob.glob(os.path.join(ROOT, g), recursive=True)]
vals = set()


def add(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return
    if v == v and abs(v) != float("inf"):
        vals.add(v)


def walk(o):
    if isinstance(o, dict):
        [walk(v) for v in o.values()]
    elif isinstance(o, list):
        [walk(v) for v in o]
    else:
        add(o)


for p in SRC:
    try:
        if p.endswith(".json"):
            walk(json.load(open(p)))
        else:
            for row in csv.reader(open(p, errors="ignore")):
                for c in row:
                    for tok in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", c):
                        add(tok)
    except Exception as e:
        print("WARN cannot read", p, e)

allow = {}
ap = os.path.join(os.path.dirname(paper), "audit_allow.txt")
if os.path.exists(ap):
    for line in open(ap):
        if "|" in line and not line.startswith("#"):
            n, why = line.split("|", 1); allow[n.strip()] = why.strip()

text = open(paper).read()
text = re.sub(r"\(?(?:https?://|doi:|10\.\d{4,}/)\S+", " ", text)          # links / DOIs
text = re.sub(r"\[[0-9,\s\-–]+\]", " ", text)                                # [12], [3-5] citations
text = re.sub(r"(?i)\b(?:table|fig\.?|figure|section|eq\.?|equation|h\d[a-z]?|rq)\s*\d+[a-z]?", " ", text)
bad, ok = [], 0
for m in re.finditer(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.]*\d)", text):
    tok = m.group(0)
    if tok in allow:
        continue
    d = len(tok.split(".")[1]) if "." in tok else 0
    t = float(tok)
    hit = any(round(v, d) == t or round(100 * v, d) == t for v in vals)
    if d == 0 and not hit:
        hit = any(abs(v - t) < 1e-9 for v in vals)
    if hit:
        ok += 1
    else:
        ctx = text[max(0, m.start() - 50): m.end() + 30].replace("\n", " ")
        bad.append((tok, ctx))
print(f"audit: {ok} numbers matched result files, {len(allow)} allow-listed, {len(bad)} UNMATCHED")
for tok, ctx in bad:
    print(f"  UNMATCHED {tok!r}: ...{ctx}...")
sys.exit(1 if bad else 0)
