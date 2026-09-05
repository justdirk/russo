#!/usr/bin/env python3
"""Patch 005 — complete book cover. IBS answered 429 on the first attempt, so try several
public sources in turn (IBS, laFeltrinelli — same platform —, then Amazon), politely and with
retries. Writes img/libro-copertina.jpg and derives img/vincenzo-premiazione.jpg (top part of
the cover, 536x515 at the IBS size). Leaves the old files in place if every source fails."""
import io, os, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(ROOT, 'img')

def get_pil():
    try:
        from PIL import Image
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
        import importlib, site
        importlib.invalidate_caches()
        try:
            site.addsitedir(site.getusersitepackages())
        except Exception:
            pass
        importlib.invalidate_caches()
        from PIL import Image
    return Image

SOURCES = [
    ('https://www.ibs.it/images/9788876022715_0_0_536_0_75.jpg', 'https://www.ibs.it/'),
    ('https://www.lafeltrinelli.it/images/9788876022715_0_0_536_0_75.jpg', 'https://www.lafeltrinelli.it/'),
    ('https://www.ibs.it/images/9788876022715_0_0_424_0_75.jpg', 'https://www.ibs.it/'),
    ('https://images-eu.ssl-images-amazon.com/images/P/8876022716.jpg', 'https://www.amazon.it/'),
]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Accept': 'image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
}

def fetch(url, referer):
    for attempt in range(3):
        try:
            h = dict(HEADERS); h['Referer'] = referer
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
                return r.read()
        except Exception as e:
            print('  attempt', attempt + 1, 'failed:', e)
            time.sleep(8 * (attempt + 1))
    return None

Image = get_pil()
for url, ref in SOURCES:
    print('trying', url)
    data = fetch(url, ref)
    if not data:
        continue
    try:
        im = Image.open(io.BytesIO(data)).convert('RGB')
    except Exception as e:
        print('  not an image:', e); continue
    if im.width < 300 or im.height <= im.width:
        print('  unexpected size', im.size); continue
    im.save(os.path.join(IMG, 'libro-copertina.jpg'), quality=82, optimize=True, progressive=True)
    # the photograph occupies the top 65% of the cover
    im.crop((0, 0, im.width, round(im.height * 515 / 793))).save(
        os.path.join(IMG, 'vincenzo-premiazione.jpg'), quality=86, optimize=True, progressive=True)
    print('cover', im.size, 'written from', url)
    break
else:
    print('COVER: every source failed, old files kept')
    sys.exit(1)
