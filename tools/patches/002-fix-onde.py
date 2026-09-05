#!/usr/bin/env python3
"""work-onde's archived asset refuses connections via the '2025im_' redirect.
Retry it against the exact 14 Feb 2025 capture timestamp instead."""
import json

p = 'tools/sources.json'
s = json.load(open(p))
old = s['work-onde']['url']
s['work-onde']['url'] = ('https://web.archive.org/web/20250214141125im_/'
                        'https://www.bellicapellibyrussomilano.it/'
                        'data/gallery/1d581ef3-3678-4a9d-a8cb-cb468ac41a80.jpeg')
json.dump(s, open(p, 'w'), indent=1)
print('work-onde url:\n  was', old, '\n  now', s['work-onde']['url'])
