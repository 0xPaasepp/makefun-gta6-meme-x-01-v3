#!/bin/sh
# tests for the gta6-meme-x-01 v3 entry (LEONIDA AIRLINES boarding pass).
# 1. meme.py is deterministic (two runs -> identical sha256)
# 2. meme.png is 1080x1080
# 3. main.ts runs with the placeholder POST.json and exits 0
set -u
cd "$(dirname "$0")/.."

fail=0
say() { printf '%s\n' "$*"; }

say "== determinism =="
python3 meme.py
sha256sum meme.png | awk '{print $1}' > /tmp/v3-test-run1.sha
python3 meme.py
sha256sum meme.png | awk '{print $1}' > /tmp/v3-test-run2.sha
if cmp -s /tmp/v3-test-run1.sha /tmp/v3-test-run2.sha; then
  say "PASS determinism: $(cat /tmp/v3-test-run1.sha)"
else
  say "FAIL determinism: $(cat /tmp/v3-test-run1.sha) != $(cat /tmp/v3-test-run2.sha)"
  fail=1
fi

say "== size =="
if python3 -c "from PIL import Image; im = Image.open('meme.png'); assert im.size == (1080, 1080), im.size"; then
  say "PASS size: meme.png is 1080x1080"
else
  say "FAIL size: meme.png is not 1080x1080"
  fail=1
fi

say "== main.ts =="
rm -rf /tmp/v3-test-out
mkdir -p /tmp/v3-test-out
if MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=/tmp/v3-test-out node main.ts; then
  if cmp -s POST.json /tmp/v3-test-out/POST.json; then
    say "PASS main.ts: exit 0, POST.json copied byte-for-byte"
  else
    say "FAIL main.ts: output POST.json differs from source"
    fail=1
  fi
else
  say "FAIL main.ts: non-zero exit"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  say "ALL TESTS PASSED"
else
  say "TESTS FAILED"
fi
exit "$fail"
