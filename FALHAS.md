# Falhas (mais recente no topo)

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-16 | traduz.py: regex do seletor de idioma (`.*?</span></span>`) engolia ~90 linhas (nav, TOC) ao substituir um seletor existente; 9 páginas EN/ES truncadas passaram no checador de esqueleto porque o corte era depois da checagem | terminar a regex em `</a></span>` (fim real do bloco) e checar `id="theme-toggle"`/`data-inema-toc` depois do pós-processamento | prompt |
| 2026-09-16 | traduz.py: placeholders `<seu-projeto>` em code box eram tratados como tag HTML no comparador; 13 módulos práticos por idioma rejeitados | comparar só tags HTML reais (lista de nomes) | prompt |
| 2026-09-16 | apóstrofo em string JS traduzida (`'That's it'`) quebrava o `registerCheck` | escapar `'` nas linhas `N: '...'` dos scripts + regra no prompt | prompt |
