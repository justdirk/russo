#!/usr/bin/env python3
"""Patch 008 — index.html with legible type (Instrument Serif display, Archivo numerals),
delivered as gzip+base64 parts in tools/inbox/. Every part is verified line-range by sha256
against tools/inbox/manifest.json, then the gzip and the final HTML are verified too. On any
mismatch nothing is written and the inbox is kept. On success the inbox is removed."""
import base64, gzip, hashlib, json, os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INBOX = os.path.join(ROOT, 'tools', 'inbox')
man = json.load(open(os.path.join(INBOX, 'manifest.json')))
text = ''; ok = True
for fn, first, last, psha in man['parts']:
    p = os.path.join(INBOX, fn)
    if not os.path.exists(p):
        print('MISSING PART', fn); ok = False; continue
    ls = [l.strip() for l in open(p).read().split('\n') if l.strip()][first - 1:last]
    chunk = '\n'.join(ls) + '\n'
    if hashlib.sha256(chunk.encode()).hexdigest() != psha:
        print('PART CHECKSUM MISMATCH', fn, first, last); ok = False
    text += chunk
if not ok:
    sys.exit(1)
gz = base64.b64decode(''.join(text.split()), validate=True)
if hashlib.sha256(gz).hexdigest() != man['gz_sha256']:
    print('GZIP SHA MISMATCH'); sys.exit(1)
raw = gzip.decompress(gz)
if hashlib.sha256(raw).hexdigest() != man['sha256'] or len(raw) != man['bytes']:
    print('HTML SHA MISMATCH'); sys.exit(1)
open(os.path.join(ROOT, man['name']), 'wb').write(raw)
print('wrote', man['name'], len(raw), 'bytes, sha256 OK')
shutil.rmtree(INBOX)
