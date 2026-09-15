# Currículo — Claude → Codex: migre ou fique agnóstico

courseId: `claude-codex` · emoji do curso: 🧠 · nome curto no nav: **Claude → Codex**
Fonte do conteúdo: `~/projetos/agente-claude-codex` (kit, PLANO.md, README.md, prompts/, scripts/), `~/projetos/wifi/DIAGNOSTICO-CLAUDE-CODEX-2026-09-14.md`, e os 3 textos-base (newsletter "Como migrar do Claude para o Codex", "O que o prompt acrescenta", prompt library "Model-agnostic workspaces").

Tese do curso: **não migre o cérebro; separe o cérebro do modelo.** Claude, Codex, Gemini ou modelo local viram executores sobre uma camada portátil de contexto + conhecimento + Markdown + processos + handoffs + memória + ferramentas.

Público: quem já usa Claude Code (ou Codex) e quer usar os dois, ou não ficar preso a nenhum. Nível: iniciante a intermediário. Cada módulo: 6 tópicos, ~30 min. Total: 3 trilhas × 6 módulos = 18 módulos, 108 tópicos.

## Trilha 1 — Fundamentos (emerald, 🧠)
Por que e o quê. Define todo termo na primeira aparição (erro #31).

| Mód | Emoji | Título | Subtítulo punchy | Tópicos (6) |
|---|---|---|---|---|
| 1.1 | 🧠 | Por que separar o cérebro do modelo | Não migre. Separe. | 1 O lock-in invisível (CLAUDE.md, memória, sessões JSONL) · 2 O que é durável e o que é descartável · 3 Modelos mudam, sua estrutura fica · 4 O Diagrama de Venn (o que é comum vs específico) · 5 Custo de não fazer nada · 6 O princípio central (contexto + conhecimento + Markdown + processos + handoffs + memória + ferramentas) |
| 1.2 | 🗣️ | O vocabulário: runtime, harness, skill, MCP, hook, handoff | As palavras do curso inteiro | 1 Modelo vs runtime vs harness · 2 Instruções (CLAUDE.md / AGENTS.md) e ordem de leitura · 3 Skill (SKILL.md) e onde cada runtime procura · 4 MCP: ferramentas e dados, não memória · 5 Hooks, plugins, subagentes: o que é nativo · 6 Handoff e prime: o resumo que viaja |
| 1.3 | 🗺️ | Os três níveis de migração | Um clique, um comando, pessoal | 1 Nível 1: importar no app Codex (e por que o CLI não tem import) · 2 Nível 2: um comando (o kit agente-claude-codex) · 3 Nível 3: a camada pessoal durável · 4 A grande faxina (Marie Kondo das pastas) · 5 O que é realmente específico do modelo (só CLAUDE.md/AGENTS.md) · 6 Quando vale construir seu próprio harness (modelos locais) |
| 1.4 | 📁 | Anatomia de um workspace portátil | AGENTS.md, context/, tasks/, handoffs/ | 1 README.md vs AGENTS.md (humano vs agente) · 2 context/overview.md e current-state.md · 3 context/sources.md e decisions/ · 4 tasks/current.md: dono e critério de pronto · 5 handoffs/latest.md · 6 .agents/skills/ e scripts/: nomes são convenção, nada auto-carrega |
| 1.5 | 🏷️ | Donos da informação | Fato, preferência, hipótese, decisão | 1 Os quatro tipos e por que misturá-los quebra · 2 Origem, escopo, data, estado, regra de atualização · 3 Provenance vence timestamp (superseded_by) · 4 Promover fato: de memória bruta a overview aprovado · 5 Índices rebuildáveis a partir das fontes · 6 Segredos e material bruto ficam fora |
| 1.6 | 🔍 | Audit antes de implement | Analisar → planejar → simular | 1 Por que os mega-prompts começam em MODE: audit · 2 Prompt A (migrar setup existente) por dentro · 3 Prompt B (workspace portátil) por dentro · 4 Matriz reutilizável / adaptador / nativo / não resolvido · 5 Evidência: passou, falhou, não rodado · 6 Arquivo existir não é prova; o agente ter lido e usado é |

## Trilha 2 — Mão na massa (blue, 🛠️)
Prática com o kit `agente-claude-codex`. Todo módulo tem ≥1 exemplo copy-run real (erro #30). Comandos reais dos scripts.

| Mód | Emoji | Título | Subtítulo punchy | Tópicos (6) |
|---|---|---|---|---|
| 2.1 | 🩺 | Diagnóstico do ambiente | doctor.sh e audit.sh | 1 Clonar o kit · 2 doctor.sh: ok / aviso / falta · 3 audit.sh: inventário somente leitura · 4 Ler a matriz de skills (72/15/2/1 nesta máquina) · 5 Sandbox do Codex e AppArmor (a falha real) · 6 O relatório em relatorios/ e o que fazer com ele |
| 2.2 | ✂️ | CLAUDE.md → AGENTS.md | Portátil de um lado, resíduo do outro | 1 O que é portátil numa instrução (regras, caminhos, versionamento) · 2 O que é resíduo Claude (AskUserQuestion, plugins, hooks) · 3 adapt-instructions.sh e os .proposto.md · 4 @AGENTS.md: o Claude importando o portátil · 5 Ordem de leitura explícita no topo · 6 Armadilha: renomear referências a CLAUDE.md de outros projetos |
| 2.3 | 🧱 | Instalar o núcleo portátil | init-core.sh sem sobrescrever | 1 init-core.sh: criado vs mantido · 2 Preencher overview.md com fatos datados · 3 tasks/current.md: objetivo, dono, critério, próxima ação · 4 Primeira decisão em context/decisions/ · 5 scripts/check.sh: verificação mínima · 6 Clone isolado: o projeto funciona sozinho? |
| 2.4 | 🧩 | Skills canônicas com polyskill | Uma fonte, N runtimes | 1 Por que cópias manuais divergem (dsh-skills como exemplo) · 2 polyskill import: SKILL.md vira definition.md + polyskill.yaml · 3 build: dist/claude e dist/codex · 4 install --both com backup ao lado · 5 drift: [ok] ou [DRIFT] · 6 Skills que dependem de MCP: portar só depois do codex mcp add |
| 2.5 | ✅ | Readback: provar em sessão nova | Cinco perguntas, dois runtimes | 1 As 5 perguntas (objetivo, regra+fonte, decisão, próxima ação, conflitos) · 2 readback-test.sh: claude -p e codex exec · 3 Ler a resposta: cita os arquivos certos? · 4 O caso real: Codex apontou 3 inconsistências no próprio kit · 5 Falhas e correções (sandbox, contagem) registradas em FALHAS.md · 6 Quando marcar passou / falhou / não rodado |
| 2.6 | 🔁 | Handoff e prime: o ciclo diário | Sessão → handoff → Markdown → prime → sessão | 1 O que entra num handoff (decisões, pendências, próximos passos, caminhos) · 2 O template de handoffs/latest.md · 3 Prime: a nova sessão lê antes de agir · 4 Cross-runtime: Claude escreve, Codex retoma · 5 Sessões JSONL viram histórico, não fonte · 6 Regra de ouro: handoff antes de fechar, sempre |

## Trilha 3 — Projetos (purple, 🚀)
Seis projetos passo a passo sobre o sistema real desta máquina (diagnóstico de 2026-09-14). Cada projeto: objetivo, passos com comandos, critério de aceite, riscos.

| Mód | Emoji | Título | Subtítulo punchy | Tópicos (6) |
|---|---|---|---|---|
| 3.1 | 🚀 | Projeto 1: migrar seu primeiro projeto real | Fase 0 e Fase 2 do plano | 1 Escolher o piloto (os 13 trusted sem AGENTS.md) · 2 Base global: ~/.codex/AGENTS.md a partir do CLAUDE.md global · 3 Faxina: CLAUDE.md de 300+ linhas vira AGENTS.md enxuto + context/ · 4 Rodar os 5 scripts em ordem · 5 Readback nos dois runtimes · 6 Aceite e handoff |
| 3.2 | 🔌 | Projeto 2: MCP e hooks entre Claude e Codex | Ferramentas viajam, eventos não | 1 Inventário: magnific e metricool no Claude, zero no Codex · 2 codex mcp add sem copiar segredo (keys em .env referenciadas) · 3 Skills de adaptador destravadas (heygen, printing-press) · 4 Hooks: SessionStart não existe no Codex; PostToolUse e Stop existem · 5 fable-mindset vira texto no AGENTS.md · 6 Subagentes viram skills de papel |
| 3.3 | 🗃️ | Projeto 3: memória curada | O agente propõe, você aprova | 1 A memória do Claude (869 arquivos) é matéria-prima, não fonte · 2 O vault do openpcbotv3 (MEMORY.md, USER.md) como overview global · 3 Fluxo propõe → aprova · 4 Consolidação com superseded_by: nunca apaga, esconde · 5 Claude, Codex e dsh lendo o mesmo USER.md por instrução · 6 Arquivar sessões antigas depois que o ciclo roda |
| 3.4 | 🐳 | Projeto 4: terceiro executor | dsh-sandbox e modelo local | 1 O que é o dsh-sandbox (DeepSeek em container, modos local/remoto) · 2 Skills copiadas à mão = drift garantido · 3 Destino --dsh no sync-skills.sh · 4 Dar contexto ao dsh: skill de prime · 5 Segurança: 269 segredos em ~/projetos, nunca remoto-projetos · 6 Expectativa: modelo local cita os arquivos certos, prosa pior |
| 3.5 | 👥 | Projeto 5: workspace de cliente | Venn, escopo e canários | 1 North Star e Harbor: o Diagrama de Venn · 2 Repo privado por cliente, snapshot de contexto com ID/fonte/data · 3 Nada de cliente em instrução global ou memória universal · 4 Add-on de cliente do Prompt B · 5 Canários sintéticos: recusa do modelo não é isolamento · 6 Expandir só depois do piloto passar |
| 3.6 | 🧭 | Projeto 6: a mentalidade | Tudo isso é iterativo | 1 Cada mudança melhora um modelo e quebra outro · 2 Acompanhar o que cada provedor exige · 3 Modelos fechados podem não precisar de skills; locais sim · 4 Você administra contexto, estado, ferramentas, processos e validação, não prompts · 5 O changelog de falhas (uma linha, menor correção, prompt ou infra) · 6 Resumo em uma frase e o que fazer amanhã |
