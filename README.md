# Claude → Codex: migre ou fique agnóstico

Curso prático INEMA.CLUB (formato v2, com camada de aprendizagem) sobre migrar um setup Claude Code pro Codex CLI ou, melhor, deixar o trabalho independente de modelo: contexto, regras, skills, decisões e handoffs em Markdown portátil, com Claude, Codex e modelo local como executores.

**Curso no ar:** https://inematds.github.io/curso-claude-codex/

| Idioma | URL |
|---|---|
| Português (original) | https://inematds.github.io/curso-claude-codex/ |
| English | https://inematds.github.io/curso-claude-codex/en/ |
| Español | https://inematds.github.io/curso-claude-codex/es/ |

As versões EN e ES são espelhos completos (`en/`, `es/`, com assets próprios), geradas por `tools/traduz.py` a partir do PT com verificação de esqueleto de tags. O progresso do aluno é separado por idioma (`inema-course` = `claude-codex-en` / `claude-codex-es`). Toda página tem o seletor PT / EN / ES no nav.

## Estrutura

| Trilha | Cor | Conteúdo |
|---|---|---|
| 1 · Fundamentos | emerald | por que separar o cérebro do modelo, vocabulário, três níveis, anatomia do workspace, donos da informação, audit antes de implement |
| 2 · Mão na massa | blue | os scripts do kit `agente-claude-codex`: doctor/audit, CLAUDE.md → AGENTS.md, núcleo portátil, polyskill, readback, handoff/prime |
| 3 · Projetos | purple | migrar o primeiro projeto real, MCP e hooks, memória curada, terceiro executor (dsh-sandbox), workspace de cliente, a mentalidade |

18 módulos, 108 tópicos, ~10h. Currículo completo em `CURRICULO.md`.

## Fontes

- Kit e scripts: https://github.com/inematds/agente-claude-codex
- Diagnóstico real da máquina (2026-09-14) que serve de caso nos projetos.
- Newsletter "Como migrar do Claude para o Codex — ou ficar independente de modelo" e a prompt library "Model-agnostic workspaces" (07 SEP 2026), lidas e reescritas como material didático.

## Traduzir de novo (depois de editar o PT)

```bash
tools/traduz.py --lang en --all --force     # reescreve en/ a partir do PT (claude -p; --engine codex também funciona)
tools/traduz.py --lang es --all --force
tools/traduz.py --lang en --switcher-pt     # reinjeta o seletor de idioma nas páginas PT
```

## Rodar local

Abra `index.html` no navegador. Tudo é self-contained (HTML + Tailwind CDN + `assets/learn.js`); funciona em `file://`. Progresso, notas e dúvidas ficam no `localStorage` do navegador e podem ser exportados em .json pelo painel "Jornada".
