#!/usr/bin/env bash
# Unpack CARE to Compare (Zenodo 14958989) into data/raw/care/x/Care_To_Compare/farm_X/ and build per-turbine caches
# serially (score jobs run in parallel and must not race on cache files). Idempotent.
set -euo pipefail
while ! grep -q CAREDL ../logs/setup_care.log 2>/dev/null; do sleep 60; done  # wait for the download job
cd "$(dirname "$0")/.."
R=data/raw/care; Z=$R/Care_To_Compare.zip
[ -f $R/.download_complete ] || { python3 - <<'PY'
import zipfile,sys; z=zipfile.ZipFile("data/raw/care/Care_To_Compare.zip"); print(len(z.namelist()),"members")
PY
touch $R/.download_complete; }
mkdir -p $R/x && [ -f $R/x/.outer_done ] || { unzip -q -o $Z -d $R/x && touch $R/x/.outer_done; }
B=$R/x/Care_To_Compare
for f in A B C; do
  [ -f $B/farm_$f/.done ] && continue
  zf=$(find $R/x -name "Wind Farm $f.zip" | head -1)
  mkdir -p $B/farm_$f && unzip -q -o "$zf" -d $B/farm_$f && touch $B/farm_$f/.done && rm -f "$zf"
done
python3 - <<'PY'
import sys; sys.path.insert(0, ".")
from src.data import care
for f in care.FARMS:
    for a in care.assets(f):
        X = care.load_asset(f, a); print(f, a, X.shape, flush=True)
PY
rm -f $Z; touch $R/.prep_done
