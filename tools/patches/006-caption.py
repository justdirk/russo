#!/usr/bin/env python3
"""Patch 006 — remove the caption sentence under Vincenzo's 2026 portrait (keep only name and dates)."""
import hashlib, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'index.html')
EXPECTED = '24d3e733a1e9fcba4b1c76715bf78813c3af969ec2581ef4184c9551a46f3385'
OLD = '<figcaption style="text-align:center"><b>Vincenzo Russo, 1938 – 2026</b><span data-it>La fotografia con cui il salone lo ha ricordato, maggio 2026.</span><span data-en>The photograph with which the salon remembered him, May 2026.</span></figcaption>'
NEW = '<figcaption style="text-align:center"><b>Vincenzo Russo, 1938 – 2026</b></figcaption>'
s = open(P, encoding='utf-8').read()
if s.count(OLD) != 1:
    print('PATCH 006: caption not found exactly once (%d)' % s.count(OLD)); sys.exit(1)
s = s.replace(OLD, NEW)
open(P, 'w', encoding='utf-8').write(s)
h = hashlib.sha256(s.encode('utf-8')).hexdigest()
print('index.html patched;', 'sha256 OK' if h == EXPECTED else 'sha256 DIFFERS: ' + h)
