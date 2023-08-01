#!/usr/bin/env bash
set -euo pipefail

while read UUID; do
  (
    set -x
    curl -s "https://netrunnerdb.com/decklist/export/text/$UUID" > "$UUID"
  )
done
