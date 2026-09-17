#!/usr/bin/env python3
"""normaliza-manifesto.py — em cada idioma (en/, es/), copia o bloco <script data-inema-manifest> da landing
(<lang>/index.html) para todas as outras páginas do idioma, para que o manifesto seja idêntico (erro #28 do v2).
Uso: tools/normaliza-manifesto.py"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
RE = re.compile(r'(<script type="application/json" data-inema-manifest>)(.*?)(</script>)', re.S)
for lang in ('en', 'es'):
    src = f'{lang}/index.html'
    if not os.path.exists(src): print(f'{lang}: sem landing, pulando'); continue
    ref = RE.search(open(src, encoding='utf-8').read()).group(2)
    n = 0
    for f in glob.glob(f'{lang}/**/*.html', recursive=True):
        h = open(f, encoding='utf-8').read(); m = RE.search(h)
        if not m: print(f'{f}: sem manifesto'); continue
        if m.group(2) != ref:
            open(f, 'w', encoding='utf-8').write(h[:m.start(2)] + ref + h[m.end(2):]); n += 1
    print(f'{lang}: {n} página(s) normalizada(s)')
