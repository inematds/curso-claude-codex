#!/usr/bin/env python3
"""traduz.py — traduz as páginas HTML do curso para EN/ES preservando a estrutura.

Estratégia: o arquivo é cortado em blocos de ~N linhas; cada bloco vai pro LLM com a ordem
"traduza só o texto visível, mantenha tags/atributos/ids/classes/comandos". A resposta é aceita
apenas se o esqueleto de tags for idêntico ao original (senão tenta de novo). Depois: lang,
courseId por idioma, e um seletor PT | EN | ES no nav.

Uso:
  tools/traduz.py --lang en --src index.html --dst en/index.html [--engine claude|codex] [--chunk 110]
  tools/traduz.py --lang es --all            # todas as 22 páginas, em paralelo (--jobs 5)
Requer: claude (ou codex) no PATH. Não toca nos originais.
"""
import argparse, concurrent.futures as cf, json, os, re, subprocess, sys, time, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = {
    'en': dict(nome='English', lang='en', course='claude-codex-en', sw=['PT', 'EN', 'ES']),
    'es': dict(nome='Spanish (neutral, Latin America)', lang='es', course='claude-codex-es', sw=['PT', 'EN', 'ES']),
}
PAGES = ['index.html'] + [f'curso/trilha{t}/index.html' for t in (1, 2, 3)] + \
        [f'curso/trilha{t}/modulo-{t}-{m}.html' for t in (1, 2, 3) for m in range(1, 7)]

TAG_RE = re.compile(r'<[^>]+>')
HTML_TAGS = set('a abbr article aside b blockquote body br button code dd details div dl dt em figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe img input label li link main meta nav ol option p pre script section select small span strong style summary svg table tbody td th thead title tr ul video source path g rect text circle line defs marker pattern filter feGaussianBlur feMerge feMergeNode linearGradient stop polyline polygon ellipse tspan'.split())
def skeleton(s):
    # sequência de tags HTML REAIS (ignora placeholders como <seu-projeto> dentro de code) com atributos estruturais
    # (ignora o que pode mudar na tradução: alt, title, aria-label, content, placeholder)
    out = []
    for t in TAG_RE.findall(s):
        m = re.match(r'</?([A-Za-z][A-Za-z0-9]*)', t)
        if not m or m.group(1) not in HTML_TAGS: continue
        t = re.sub(r'\s(alt|title|aria-label|content|placeholder)="[^"]*"', '', t)
        out.append(re.sub(r'\s+', ' ', t).strip())
    return out

def prompt_for(lang, chunk):
    L = LANGS[lang]
    return f"""You are translating a Brazilian-Portuguese HTML course page fragment into {L['nome']}.
RULES (strict):
- Translate ONLY human-visible text: text between tags, and the values of alt, title, aria-label, placeholder and <meta name="description"> content.
- Keep EVERY tag, attribute, id, class, data-* value, href, src, JSON key, JavaScript and CSS exactly as is. Do not add, remove or reorder tags. Do not add comments.
- Inside <pre>/<code>: keep commands, paths, flags and file names unchanged; translate only comments after '#' or '//' and prose that is clearly a description.
- Keep product names (Claude Code, Codex, AGENTS.md, CLAUDE.md, polyskill, INEMA.CLUB, PRO, handoff, prime, readback, drift) untranslated; translate everything else naturally, not word-by-word.
- Inside <script>, never put an unescaped apostrophe inside a single-quoted string: write it as \\' (e.g. 'That\\'s it').
- Keep emoji, numbers, dates and HTML entities. Keep line breaks: output must have the same number of lines as the input.
- Output the translated fragment ONLY, no explanations, no code fences.

FRAGMENT:
{chunk}"""

def call_llm(engine, prompt):
    if engine == 'claude':
        r = subprocess.run(['claude', '-p', '--output-format', 'text', prompt], capture_output=True, text=True, timeout=600)
        return r.stdout
    r = subprocess.run(['codex', 'exec', '--skip-git-repo-check', prompt], capture_output=True, text=True, timeout=600)
    lines = [l for l in r.stdout.splitlines() if not re.match(r'^(hook:|tokens used|[0-9,]+)$', l)]
    return '\n'.join(lines)

def clean(out):
    out = out.strip('\n')
    out = re.sub(r'^```[a-z]*\n', '', out); out = re.sub(r'\n```$', '', out)
    return out

def translate_chunk(engine, lang, chunk, tries=5):
    # tenta `engine`; a partir da 3ª tentativa alterna pro outro motor (claude <-> codex). Resposta vazia/curta
    # (ex.: aviso de limite de uso) conta como falha e espera com backoff.
    sk = skeleton(chunk); other = 'codex' if engine == 'claude' else 'claude'
    for i in range(tries):
        eng = engine if i < 2 else (other if i % 2 == 0 else engine)
        try: out = clean(call_llm(eng, prompt_for(lang, chunk)))
        except Exception: out = ''
        if len(out) > len(chunk) * 0.5 and skeleton(out) == sk and abs(out.count('\n') - chunk.count('\n')) <= max(2, chunk.count('\n') // 20):
            return out, i + 1
        time.sleep(10 * (i + 1))
    return None, tries

def split_chunks(text, n):
    lines = text.split('\n'); chunks = []; buf = []
    in_script = False
    for l in lines:
        buf.append(l)
        if '<script' in l and '</script>' not in l: in_script = True
        if '</script>' in l: in_script = False
        # corta em fronteira "segura": fim de bloco, fora de script
        if len(buf) >= n and not in_script and re.search(r'</(section|div|p|li|header|nav|footer|table|figure|h[1-4])>\s*$', l):
            chunks.append('\n'.join(buf)); buf = []
    if buf: chunks.append('\n'.join(buf))
    return chunks

def switcher(lang_of_file, rel_root):
    # rel_root: caminho do arquivo até a raiz do curso (ex.: '' na landing, '../../' em módulo). Página irmã: mesmo caminho em outro idioma.
    def link(code):
        return f'<a href="{{HREF}}" class="text-neutral-400 hover:text-neutral-100 text-xs font-semibold">{code}</a>'
    return None

def add_switcher(html, lang, page):
    depth = page.count('/')
    up = '../' * depth
    def href(target):
        base = up + ('../' if lang != 'pt' else '')          # até a raiz do repo
        return (base + page) if target == 'pt' else (base + f'{target}/' + page)
    items = []
    for code in ('pt', 'en', 'es'):
        cls = 'text-yellow-400' if code == lang else 'text-neutral-400 hover:text-neutral-100'
        items.append(f'<a href="{href(code)}" class="{cls} text-xs font-semibold" title="{ {"pt":"Português","en":"English","es":"Español"}[code] }">{code.upper()}</a>')
    block = '<span class="text-neutral-600">|</span><span class="inline-flex items-center gap-1.5" data-lang-switch>' + '<span class="text-neutral-600">/</span>'.join(items) + '</span>'
    if 'data-lang-switch' in html:  # bloco termina em </a></span> (o último item é <a>); nunca avançar além disso
        return re.sub(r'<span class="text-neutral-600">\|</span><span class="inline-flex items-center gap-1.5" data-lang-switch>.*?</a></span>', block, html, count=1, flags=re.S)
    # insere depois do link PRO no nav
    return re.sub(r'(<a href="https://inema.pro"[^>]*>PRO</a>)', r'\1' + block, html, count=1)

def fix_js_quotes(html):
    # apóstrofos que a tradução coloca dentro de strings JS com aspas simples (ex.: explain: { 1: 'That's it' })
    def fix_line(m):
        pre, body, post_ = m.group(1), m.group(2), m.group(3)
        body = re.sub(r"(?<!\\)'", "\\'", body)
        return f"{pre}'{body}'{post_}"
    def fix_script(m):
        js = m.group(1)
        js = re.sub(r"^(\s*(?:\d+|answer|q|explain|label|title|text)\s*:\s*)'(.*)'(\s*,?\s*)$", fix_line, js, flags=re.M)
        return '<script>' + js + '</script>'
    return re.sub(r'<script>(.*?)</script>', fix_script, html, flags=re.S)

def post(html, lang, page):
    L = LANGS[lang]
    html = fix_js_quotes(html)
    html = html.replace('<html lang="pt-BR"', f'<html lang="{L["lang"]}"', 1)
    html = html.replace('<meta name="inema-course" content="claude-codex">', f'<meta name="inema-course" content="{L["course"]}">', 1)
    html = html.replace('"course": "claude-codex"', f'"course": "{L["course"]}"', 1)
    return add_switcher(html, lang, page)

def do_file(engine, lang, page, chunk_n, force=False):
    src = os.path.join(ROOT, page); dst = os.path.join(ROOT, lang, page)
    if os.path.exists(dst) and not force: return page, 'existe', 0
    text = open(src, encoding='utf-8').read()
    chunks = split_chunks(text, chunk_n); out = []; retries = 0
    for c in chunks:
        if not re.search(r'[A-Za-zÀ-ú]{3,}', TAG_RE.sub(' ', c)):  # sem texto visível (só tags/script)
            out.append(c); continue
        t, n = translate_chunk(engine, lang, c); retries += n - 1
        if t is None: return page, f'FALHOU (bloco de {c.count(chr(10))+1} linhas sem esqueleto igual)', retries
        out.append(t)
    html = post('\n'.join(out), lang, page)
    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'w', encoding='utf-8').write(html)
    return page, f'ok ({len(chunks)} blocos)', retries

def copy_assets(lang):
    for d in ['assets'] + [f'curso/trilha{t}/assets' for t in (1, 2, 3)]:
        s = os.path.join(ROOT, d); t = os.path.join(ROOT, lang, d)
        if os.path.isdir(s): shutil.copytree(s, t, dirs_exist_ok=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--lang', required=True, choices=LANGS); ap.add_argument('--src'); ap.add_argument('--dst')
    ap.add_argument('--all', action='store_true'); ap.add_argument('--engine', default='claude'); ap.add_argument('--chunk', type=int, default=110)
    ap.add_argument('--jobs', type=int, default=5); ap.add_argument('--force', action='store_true'); ap.add_argument('--switcher-pt', action='store_true', help='só injeta o seletor de idioma nas páginas PT')
    a = ap.parse_args()
    if a.switcher_pt:
        for p in PAGES:
            f = os.path.join(ROOT, p); h = open(f, encoding='utf-8').read(); open(f, 'w', encoding='utf-8').write(add_switcher(h, 'pt', p))
        print('seletor injetado nas páginas PT'); return
    copy_assets(a.lang)
    pages = PAGES if a.all else [a.src]
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for page, st, rt in ex.map(lambda p: do_file(a.engine, a.lang, p, a.chunk, a.force), pages):
            print(f'[{a.lang}] {page}: {st}; retries={rt}', flush=True)
    print(f'tempo: {int(time.time()-t0)}s')

if __name__ == '__main__': main()
