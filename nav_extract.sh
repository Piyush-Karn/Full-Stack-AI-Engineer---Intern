#!/usr/bin/env bash


URL="https://www.amfiindia.com/spages/NAVAll.txt"
OUTFILE="nav.tsv"

curl -s "$URL" \
  | tail -n +2 \
  | cut -d\; -f3,4 \
  | tr ';' '\t' \
  > "$OUTFILE"

echo "Extracted $(wc -l < "$OUTFILE") entries to $OUTFILE"
