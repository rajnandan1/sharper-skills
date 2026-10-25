#!/bin/sh
# One command for a release audit. Writes audit/runs/<date>/report.md.
#   sh audit/run.sh            full run: fetch, matrices, transcripts, behavioural runs, report
#   sh audit/run.sh --quick    skips the behavioural runs
set -e
cd "$(dirname "$0")/.."
RUN=audit/runs/$(date +%Y-%m-%d-%H%M); mkdir -p "$RUN"
python3 audit/fetch.py --all audit/sources/sources.json audit/runs/sources/
for c in audit/sources/*.claims.json; do
  id=$(basename "$c" .claims.json)
  python3 audit/matrix.py --source "audit/runs/sources/$id.txt" --claims "$c" --skills skills --out "$RUN/$id" || true
done
python3 audit/transcripts.py --mode debug --skills debugging-by-constraints signal-first-plan --out "$RUN/transcripts-debug"
python3 audit/transcripts.py --mode lens --skills higher deeper wider --out "$RUN/transcripts-lens"
if [ "$1" != "--quick" ]; then
  python3 audit/behave.py --family debugging --skills skills --out "$RUN/behave"
  python3 audit/behave.py --family lenses --skills skills --out "$RUN/behave"
fi
python3 audit/report.py "$RUN" > "$RUN/report.md"
echo "report: $RUN/report.md"
