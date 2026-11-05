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
  `test_enquete_view`). A correção está no PR #308.
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
por Wanessa Bezerra) em PRs menores para a `dev`:

| Ordem | PR | Branch | Conteúdo | Status |
|---|---|---|---|---|
| 1 | #308 | `fix/ci-django52-compat` | CI na `dev` + Python 3.12, `django-filter` 25.1, `assertEqual`, redirects com barra final | 🟡 Aberto, aguardando revisão |
| 2 | #309 | `chore/separar-dependencias` | `requirements-dev`/`requirements-mutation`, `mutation_settings.py`, README | 🟡 Aberto, aguardando revisão |
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
- A branch remota `fix/ci-django52` é a primeira tentativa do PR #308, com um
  commit misturado. Ela foi substituída por `fix/ci-django52-compat` e pode ser
  apagada.

---

## 🧠 Aprendizados & Decisões

- **Testes de views:** usar sempre `reverse('<nome>')` de `core/urls.py`;
  caminhos fixos com `/core/...` dão 404, porque o app fica em
  `/suggestclasses/`.
- **Banco de testes:** o papel do PostgreSQL precisa de `CREATEDB` e `INHERIT`
  (ver `AGENTS.md`).
- **Testes de mutação:** `django-mutpy` 0.1.2 / MutPy 0.6.1 só funcionam até
  o Python 3.11 e não são mais mantidos. Não há job de mutação no CI.
  Hipótese a avaliar: migrar para `mutmut` ou `cosmic-ray`.
- **Identidade git:** este clone não tem `user.name`/`user.email`
  configurados; os commits do agente usam variáveis `GIT_AUTHOR_*` e
  `GIT_COMMITTER_*`.

---

## 📋 Pendências

- [ ] Revisar e mergear #308 → #309 → #310 → #311 → docs na `dev`.
- [ ] Corrigir os problemas conhecidos de #310 e #311 antes do merge.
- [ ] Decidir sobre `selenium`/`webdriver-manager` (não usados) e sobre
      reverter `'core'` → `'core.apps.CoreConfig'` (#309).
- [ ] Fechar o PR #253 e apagar a branch `fix/ci-django52`.
- [ ] Avaliar a remoção de `matplotlib` de `requirements.txt` (o código de
      plotagem foi removido em `8422ada`).
- [ ] Abrir PR `dev` → `main` quando a `dev` estiver estável.
