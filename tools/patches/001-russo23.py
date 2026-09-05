#!/usr/bin/env python3
"""One-off rename: Russo Belli Capelli -> Russo 23. Applied once by the workflow, then deleted."""
import os
REPL = [('<title>Russo Belli Capelli — Parrucchiere e Barbiere a Milano, via Meda</title>', '<title>Russo 23 — Parrucchiere e Barbiere a Milano, via Meda 23</title>'), ('<meta property="og:site_name" content="Russo Belli Capelli · Milano">', '<meta property="og:site_name" content="Russo 23 · Milano">'), ('<meta property="og:title" content="Russo Belli Capelli — Parrucchiere e Barbiere a Milano, via Meda">', '<meta property="og:title" content="Russo 23 — Parrucchiere e Barbiere a Milano, via Meda 23">'), ('RUSSO <span class="mk2">BELLI CAPELLI</span><small>MILANO · VIA MEDA 23 · DAL 1998</small>', 'RUSSO <span class="mk2">23</span><small>BELLI CAPELLI · VIA MEDA 23 · MILANO</small>'), ('<h1 class="word">RUSSO<span class="sm">belli capelli</span></h1>', '<h1 class="word">RUSSO <span class="num">23</span><span class="sm">belli capelli · via Meda</span></h1>'), ('.mark .mk2{font-weight:400;letter-spacing:.11em}', '.mark .mk2{font-weight:400;color:var(--brass)}\nh1.word .num{font-weight:400;color:var(--brass)}'), ('"name":"Russo Belli Capelli",\n      "alternateName":["Belli Capelli by Russo","Bellicapelli di Russo Raffaele","Raffaele Russo parrucchiere Milano"],', '"name":"Russo 23",\n      "alternateName":["Russo Parrucchieri","Belli Capelli by Russo","Bellicapelli di Russo Raffaele","Raffaele Russo parrucchiere Milano"],')]
p = 'index.html'; s = open(p, encoding='utf-8').read()
for a, b in REPL:
    if a not in s: raise SystemExit('patch anchor missing: ' + a[:60])
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
r = 'README.md'
if os.path.exists(r):
    t = open(r, encoding='utf-8').read().replace('# Russo Belli Capelli — sito', '# Russo 23 — sito').replace('salone **Russo Belli Capelli**', 'salone **Russo 23** (Belli Capelli by Russo)')
    open(r, 'w', encoding='utf-8').write(t)
print('renamed to Russo 23')
