#!/usr/bin/env python3
"""Patch 003 — photographs.

1. Decode Raffaele's two photographs, delivered as base64 in tools/inbox/, into img/
   (each verified against the sha256 in tools/inbox/manifest.json).
2. Replace the cropped book cover with the complete cover from IBS and derive
   vincenzo-premiazione.jpg from it. If IBS cannot be reached the old files are kept.
3. Remove tools/inbox and the old tools/retry.txt trigger.
The workflow deletes this file after it has run successfully.
"""
import base64, hashlib, io, json, os, shutil, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INBOX = os.path.join(ROOT, 'tools', 'inbox')
IMG = os.path.join(ROOT, 'img')
os.makedirs(IMG, exist_ok=True)

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
    from PIL import Image

# 1. inbox -> img/
ok = True
if os.path.isdir(INBOX):
    man = json.load(open(os.path.join(INBOX, 'manifest.json')))
    for name, info in man.items():
        text = ''
        good = True
        for fn, first, last, psha in info['parts']:
            p = os.path.join(INBOX, fn)
            if not os.path.exists(p):
                print('MISSING PART', fn); good = False; continue
            # use non-empty lines first..last (1-based, inclusive); normalise whitespace
            ls = [l.strip() for l in open(p).read().split('\n') if l.strip()][first - 1:last]
            chunk = '\n'.join(ls) + '\n'
            if hashlib.sha256(chunk.encode()).hexdigest() != psha:
                print('PART CHECKSUM MISMATCH', fn); good = False
            text += chunk
        if not good:
            ok = False; continue
        try:
            raw = base64.b64decode(''.join(text.split()), validate=True)
        except Exception as e:
            print('DECODE FAILED', name, e); ok = False; continue
        h = hashlib.sha256(raw).hexdigest()
        if h != info['sha256']:
            print('SHA MISMATCH', name, len(raw), 'bytes, expected', info['bytes'], '->', h); ok = False; continue
        open(os.path.join(IMG, name + '.jpg'), 'wb').write(raw)
        print('wrote', name, len(raw) // 1024, 'KB')
    if ok:
        shutil.rmtree(INBOX)
    else:
        print('inbox kept for inspection')
else:
    print('no inbox')

# 2. complete book cover from IBS
COVER = 'https://www.ibs.it/images/9788876022715_0_0_536_0_75.jpg'
try:
    req = urllib.request.Request(COVER, headers={'User-Agent': 'Mozilla/5.0 (site build; +https://github.com/justdirk/russo)'})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    cover = Image.open(io.BytesIO(data)).convert('RGB')
    if cover.width < 500 or cover.height < cover.width:
        raise ValueError('unexpected cover size %s' % (cover.size,))
    cover.save(os.path.join(IMG, 'libro-copertina.jpg'), quality=82, optimize=True, progressive=True)
    cover.crop((0, 0, 536, 515)).save(os.path.join(IMG, 'vincenzo-premiazione.jpg'), quality=86, optimize=True, progressive=True)
    print('cover', cover.size, 'and premiazione written')
except Exception as e:
    print('COVER FETCH FAILED (old files kept):', e)

# 3. old retry trigger
rt = os.path.join(ROOT, 'tools', 'retry.txt')
if os.path.exists(rt):
    os.remove(rt)

if not ok:
    raise SystemExit(1)
