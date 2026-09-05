#!/usr/bin/env python3
"""Patch 009 - aggiunge a tools/sources.json il servizio fotografico professionale
del salone (mini-sito Treatwell del salone stesso, 1280x800). Merge non distruttivo:
le voci esistenti restano intatte."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'tools', 'sources.json')
CDN = 'https://cdn1.treatwell.net/images/view/%s/'
NOTE = 'servizio fotografico del salone, profilo Treatwell del salone'

NEW = {
    'sal-raffaele-lavoro': ('v2.i2152892.w1280.h800.xA7C021ED', 1200, 80),
    'sal-poltrone':        ('v2.i2152562.w1280.h800.xB302FB54', 1200, 80),
    'sal-uomo':            ('v2.i2152570.w1280.h800.x8C75D50F', 1200, 80),
    'sal-uomo-wide':       ('v2.i2152557.w1280.h800.x12D94088', 1000, 78),
    'sal-donna':           ('v2.i2152882.w1280.h800.x45E1B18A', 1200, 80),
    'sal-donna-postazioni':('v2.i2152883.w1280.h800.x09DED532', 1000, 78),
    'sal-donna-lavoro':    ('v2.i2152891.w1280.h800.xBDCDFD4D', 1000, 78),
    'sal-lavaggio':        ('v2.i2152886.w1280.h800.xFA0DE7FC', 1000, 78),
    'sal-rituale':         ('v2.i2152889.w1280.h800.xD77A3D0F', 1200, 80),
    'sal-barba':           ('v2.i2152947.w1280.h800.x910C3658', 1000, 78),
    'sal-riccio':          ('v2.i2152900.w1280.h800.xB7DC1921', 1000, 78),
    'sal-taglio-uomo':     ('v2.i12068884.w1280.h800.x43863251', 1000, 78),
}

src = json.load(open(SRC, encoding='utf-8'))
added = []
for name, (path, maxw, q) in NEW.items():
    if name in src:
        continue
    src[name] = {'url': CDN % path, 'maxw': maxw, 'q': q, 'note': NOTE}
    added.append(name)
json.dump(src, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False)
print('sources.json: aggiunte', len(added), 'voci ->', ', '.join(added) or '(nessuna)')
