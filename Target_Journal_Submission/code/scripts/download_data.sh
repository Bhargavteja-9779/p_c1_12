#!/usr/bin/env bash
# Downloads public datasets into code/data/raw (not stored in git).
set -euo pipefail
cd "$(dirname "$0")/../data" && mkdir -p raw && cd raw
# PreDist: district heating substations, Fraunhofer IEE / enercity, CC-BY-4.0, Zenodo record 19496480
[ -f predist_dataset.zip ] || curl -L -o predist_dataset.zip "https://zenodo.org/records/19496480/files/predist_dataset.zip?download=1"
[ -d predist ] || (mkdir predist && cd predist && unzip -q ../predist_dataset.zip)
