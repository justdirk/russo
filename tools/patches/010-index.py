#!/usr/bin/env python3
"""Patch 010 - index.html con le nuove foto del salone (hero: Raffaele al lavoro;
galleria rinnovata con le foto professionali). Consegnato come parti gzip+base64 in
tools/inbox/. Ogni segmento e' verificato per intervallo di righe con sha256 contro
tools/inbox/manifest.json, poi si verificano anche il gzip e l'HTML finale. In caso di
qualsiasi discrepanza non si scrive nulla e l'inbox resta. Se tutto torna, l'inbox viene rimossa."""
import base64, gzip, hashlib, json, os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INBOX = os.path.join(ROOT, 'tools', 'inbox')
man = json.load(open(os.path.join(INBOX, 'manifest.json')))
cache = {}
def lines(fn):
    if fn not in cache:
        p = os.path.join(INBOX, fn)
        if not os.path.exists(p):
            return None
        cache[fn] = [l.strip() for l in open(p).read().split('\n') if l.strip()]
    return cache[fn]
text = ''; ok = True
for fn, first, last, psha in man['parts']:
    ls = lines(fn)
    if ls is None:
        print('MISSING PART', fn); ok = False; continue
    chunk = '\n'.join(ls[first - 1:last]) + '\n'
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
