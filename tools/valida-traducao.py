#!/usr/bin/env python3
"""valida-traducao.py — confere en/ e es/ contra o PT: esqueleto de tags HTML reais (ignorando o seletor de
idioma), ids estruturais, tópicos, manifesto idêntico por idioma, courseId, lang, e compila os scripts inline.
Uso: tools/valida-traducao.py   (sai 1 se algo falhar)"""
import glob, hashlib, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, 'tools'); import traduz
SW = re.compile(r'<span class="text-neutral-600">\|</span><span class="inline-flex items-center gap-1.5" data-lang-switch>.*?</a></span>', re.S)
def sk(s): return [re.sub(r'\slang="[^"]*"', '', t) for t in traduz.skeleton(SW.sub('', s))]
bad = []; total = 0; man = {}
for lang in ('en', 'es'):
    for page in traduz.PAGES:
        f = f'{lang}/{page}'; total += 1
        if not os.path.exists(f): bad.append(f'{f}: FALTA'); continue
        a = open(page, encoding='utf-8').read(); b = open(f, encoding='utf-8').read()
        if sk(a) != sk(b): bad.append(f'{f}: esqueleto de tags difere do PT')
        for x in ('id="theme-toggle"', 'id="conteudo"', 'inema.pro', 'learn.js', 'data-lang-switch'):
            if x not in b: bad.append(f'{f}: falta {x}')
        if 'modulo-' in f and b.count('data-inema-topic=') != 6: bad.append(f'{f}: {b.count("data-inema-topic=")} tópicos')
        if f'content="claude-codex-{lang}"' not in b or f'"course": "claude-codex-{lang}"' not in b: bad.append(f'{f}: courseId errado')
        if f'<html lang="{lang}"' not in b: bad.append(f'{f}: lang errado')
        if '{{' in b: bad.append(f'{f}: placeholder')
        m = re.search(r'data-inema-manifest>(.*?)</script>', b, re.S); man.setdefault(lang, set()).add(hashlib.md5(m.group(1).encode()).hexdigest() if m else 'none')
        # links relativos resolvem
        d = os.path.dirname(f)
        for h in re.findall(r'(?:href|src|data-src)="([^"#]+\.(?:html|css|js|jpg|png))"', b):
            if h.startswith('http'): continue
            if not os.path.exists(os.path.normpath(os.path.join(d, h))): bad.append(f'{f}: link quebrado {h}')
for lang, s in man.items():
    if len(s) != 1: bad.append(f'{lang}: manifesto não idêntico em todas as páginas ({len(s)} variantes)')
r = subprocess.run(['node', 'tools/checa-js.js'] + glob.glob('en/**/*.html', recursive=True) + glob.glob('es/**/*.html', recursive=True), capture_output=True, text=True)
if r.returncode: bad.append('scripts inline: ' + r.stdout.strip().replace('\n', ' | '))
print(f'{total - len([x for x in bad if x.endswith("FALTA")])}/{total} páginas presentes; problemas: {len(bad)}')
print('\n'.join(bad) if bad else 'tudo ok'); sys.exit(1 if bad else 0)
