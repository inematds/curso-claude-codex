# Claude → Codex: migre ou fique agnóstico

Curso prático INEMA.CLUB (formato v2, com camada de aprendizagem) sobre migrar um setup Claude Code pro Codex CLI ou, melhor, deixar o trabalho independente de modelo: contexto, regras, skills, decisões e handoffs em Markdown portátil, com Claude, Codex e modelo local como executores.

**Curso no ar:** https://inematds.github.io/curso-claude-codex/

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

## Rodar local

Abra `index.html` no navegador. Tudo é self-contained (HTML + Tailwind CDN + `assets/learn.js`); funciona em `file://`. Progresso, notas e dúvidas ficam no `localStorage` do navegador e podem ser exportados em .json pelo painel "Jornada".
