# MEMORY.md - Memória do Projeto e Estado do Sistema

Este arquivo mantém o contexto atual do SuggestClasses: decisões tomadas,
aprendizados, pull requests em andamento e pendências. Leia também o
`AGENTS.md` (ambiente, banco de dados, testes e CI).

---

## 📌 Contexto Atual

- **Repositório:** `labens-ufrn/suggestclasses` (GitHub), Django 5.2.x +
  PostgreSQL, app principal `core/`, montado sob o prefixo `/suggestclasses/`.
- **CI:** GitHub Actions (`.github/workflows/pythonapp.yml`), com serviço
  PostgreSQL e `coverage` + Sonar.
- **Estado do CI da `main` (2026-11-05):** 🔴 **falhando** (run `42028905271`):
  `django-filter==22.1` é incompatível com Django 5.2
  (`AttributeError: 'super' object has no attribute '_set_choices'` em
  `test_enquete_view`). Já corrigido na `dev` pelo PR #308; chega à `main` no
  próximo merge `dev` → `main`.
- **Estado do CI da `dev`:** 🟢 verde após o merge do #308 (run `42035803062`).
- **Ambiente local:** não há `.venv` nem `.env` criados neste clone
  (verificado em 2026-11-05); os testes deste ciclo foram validados apenas
  pelo CI.

---

## 🌿 Fluxo de Branches (desde 2026-11-05)

- `main`: branch de release.
- `dev`: branch de integração do desenvolvimento, criada a partir da `main`
  (`0111d22`) em 2026-11-05.
- Feature branches saem da `dev` e abrem PR para a `dev`; cada PR é revisado
  antes do merge. Commits seguem Conventional Commits.

---

## 🔀 Pull Requests em Andamento

Divisão do PR #253 (`testes3` → `main`, "Testes e bug", aberto em 2022-12-10
por Wanessa Bezerra) em PRs menores para a `dev`, todos na milestone **Iteração 14: Modernização e
Integração na dev** (#15, criada em 2026-11-05, sem prazo). O #308 tem os labels
`Tipo: Bug :bug:`, `Tipo: CI`, `dependencies`, `python`, `Prioridade: Alta` e
`Status: Precisa Ser Revisado`.

| Ordem | PR | Branch | Conteúdo | Status |
|---|---|---|---|---|
| 1 | #308 | `fix/ci-django52-compat` | CI na `dev` + Python 3.12, `django-filter` 25.1, `assertEqual`, redirects com barra final | 🟢 MERGED em dev (2026-11-05, `ea9fc74`) |
| 2 | #309 | `chore/separar-dependencias` | `requirements-dev`/`requirements-mutation`, `mutation_settings.py`, README | 🟢 Revisado e aprovado (2026-11-05) |
| 3 | #310 | `test/bo-dao` | Testes de BO/DAO | 🟡 Aberto, **com problemas conhecidos** |
| 4 | #311 | `test/views` | Testes de views | 🟡 Aberto, **com problemas conhecidos** |
| 5 | — | `docs/agents-memory` | `AGENTS.md` (fluxo de branches) + este `MEMORY.md` | 🟡 Aberto, aguardando revisão |

- **Ordem de merge obrigatória:** #308 primeiro, porque ele inclui `dev` nos
  gatilhos do workflow. Antes disso, os outros PRs não rodam CI; depois do
  merge do #308, atualizar as branches (`gh pr update-branch <n>`) para
  disparar o CI.
- Os problemas de cada PR estão descritos no corpo dele (testes duplicados
  com o mesmo nome, testes só com `pass`, teste sem prefixo `test_`,
  `unittest.TestCase` em vez de `django.test.TestCase`, asserção que passa
  sempre).
- O PR #253 continua aberto; fechá-lo depois dos merges, com referência aos
  novos PRs.
- As branches `fix/ci-django52` (primeira tentativa do #308) e
  `fix/ci-django52-compat` foram apagadas em 2026-11-05.

---

## 🧠 Aprendizados & Decisões

- **Revisão:** o GitHub não permite que o autor aprove o próprio PR. Como os
  PRs são abertos com a conta `tacianosilva`, a aprovação formal precisa vir de
  outro membro; senão, o merge é feito após revisão por comentário. A `dev` não
  tem proteção de branch.
- **Token do `gh`:** sem o escopo `workflow`; `gh pr update-branch` falha em PRs
  que alteram `.github/workflows/`. Nesses casos, mesclar a `dev` localmente e
  fazer `git push`, ou rodar `gh auth refresh -s workflow`.

- **Testes de views:** usar sempre `reverse('<nome>')` de `core/urls.py`;
  caminhos fixos com `/core/...` dão 404, porque o app fica em
  `/suggestclasses/`.
- **Banco de testes:** o papel do PostgreSQL precisa de `CREATEDB` e `INHERIT`
  (ver `AGENTS.md`).
- **Testes de mutação (decisão de 2026-11-05):** o MutPy **não funciona mais**
  e será removido em outro momento. Fato (PyPI): `mutpy` 0.6.1 (2019-11-17)
  declara suporte até Python 3.7 e `django-mutpy` 0.1.2 (2017-08-18) até
  Python 3.6; o Django 5.2 exige Python >= 3.10. A depreciação está documentada
  no README e no `requirements-mutation.txt` (#309). Não há job de mutação no
  CI. Hipótese a avaliar: migrar para `mutmut` ou `cosmic-ray`.
- **`selenium`/`webdriver-manager`:** mantidos em `requirements-dev.txt` por
  decisão da revisão do #309, embora ainda não sejam usados no código.
- **`INSTALLED_APPS`:** manter `'core.apps.CoreConfig'` (revertida a troca por
  `'core'` na revisão do #309).
- **Identidade git:** este clone não tem `user.name`/`user.email`
  configurados; os commits do agente usam variáveis `GIT_AUTHOR_*` e
  `GIT_COMMITTER_*`.

---

## 📋 Pendências

- [x] Revisar e mergear #308 (2026-11-05).
- [ ] Revisar e mergear #309 → #310 → #311 → docs na `dev`.
- [ ] Corrigir os problemas conhecidos de #310 e #311 antes do merge.
- [ ] Remover o MutPy (`requirements-mutation.txt`, `mutation_settings.py`,
      seção do README) e avaliar uma alternativa.
- [ ] Fechar o PR #253.
- [ ] Apagar as 24 branches remotas antigas já mergeadas na `main` (a remoção
      em lote exige ação manual) e avaliar as não mergeadas
      (`feat/issue172`, `refactor/issue213-postgres`, `update-readme`,
      `tacianosilva-patch-2`).
- [ ] Avaliar a remoção de `matplotlib` de `requirements.txt` (o código de
      plotagem foi removido em `8422ada`).
- [ ] Abrir PR `dev` → `main` quando a `dev` estiver estável.
