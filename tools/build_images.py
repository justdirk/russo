#!/usr/bin/env python3
"""Rebuild img/*.jpg from the public sources listed in tools/sources.json.
Run once; the workflow commits the results so later builds skip this step."""
import json, os, sys, io, time, urllib.request
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = json.load(open(os.path.join(ROOT, 'tools', 'sources.json')))
OUT = os.path.join(ROOT, 'img'); os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (site build; +https://github.com/justdirk/russo)'}

def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise last

def trim_bars(im, thresh=28):
    g = im.convert('L'); w, h = g.size; px = g.load()
    rows = [y for y in range(h) if max(px[x, y] for x in range(0, w, 2)) > thresh]
    cols = [x for x in range(w) if max(px[x, y] for y in range(0, h, 2)) > thresh]
    if not rows or not cols: return im
    return im.crop((min(cols), min(rows), max(cols) + 1, max(rows) + 1))

failed = []
for name, spec in SRC.items():
    dst = os.path.join(OUT, name + '.jpg')
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        print('keep ', name); continue
    try:
        im = Image.open(io.BytesIO(fetch(spec['url'])))
        im = ImageOps.exif_transpose(im).convert('RGB')
        if spec.get('crop'): im = im.crop(tuple(spec['crop']))
        if spec.get('trim'): im = trim_bars(im)
        if spec.get('portrait') and im.width > im.height: im = im.rotate(-90, expand=True)
        mw = spec.get('maxw')
        if mw and im.width > mw: im = im.resize((mw, round(im.height * mw / im.width)), Image.LANCZOS)
        im.save(dst, quality=spec.get('q', 80), optimize=True, progressive=True)
        print('built', name, im.size, os.path.getsize(dst) // 1024, 'KB')
    except Exception as e:
        failed.append(name); print('FAIL ', name, e, file=sys.stderr)

if failed:
    print('Failed:', failed, file=sys.stderr); sys.exit(1)
