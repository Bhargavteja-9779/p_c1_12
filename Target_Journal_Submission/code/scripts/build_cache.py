"""Parse all raw PreDist CSVs into harmonised parquet cache."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.data import predist as P
for m in (1, 2):
    for s in P.substations(m):
        d = P.load_substation(m, s)
print("cached")
