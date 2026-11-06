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
- **Estado do CI da `dev`:** 🟢 verde após os merges de #308, #309 e #310.
- **Ambiente local (desde 2026-11-05):** `.venv` com Python 3.12.15 (`uv`),
  `.env` local (`chmod 600`, senha aleatória do `sc_user`) e PostgreSQL 16.2
  em espaço de usuário (`pgserver` 0.1.4, `systemd --user`
  `postgresql-local.service`, `127.0.0.1:5432`). Detalhes no `AGENTS.md`.
  Suíte local na branch `test/views` (2026-11-06): **90 testes OK** em ~16 s
  com `--keepdb`; na `test/bo-dao` eram 61 testes.

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
| 2 | #309 | `chore/separar-dependencias` | `requirements-dev`/`requirements-mutation`, `mutation_settings.py`, README | 🟢 MERGED em dev (2026-11-05) |
| 3 | #310 | `test/bo-dao` | Testes de BO/DAO | 🟢 MERGED em dev (2026-11-05, `ca16e78`) |
| 4 | #311 | `test/views` | Testes de views | 🟢 Problemas conhecidos corrigidos em 2026-11-06 (90 testes OK); aguardando revisão/merge |
| 5 | #312 | `docs/agents-memory` | `AGENTS.md` (fluxo de branches) + este `MEMORY.md` | 🟡 Aberto, aguardando revisão/merge |

- **Ordem de merge:** #308 → #309 → #310 já estão na `dev`. Faltam #311 e
  #312, que são independentes entre si.
- Os problemas originais dos PRs (testes duplicados com o mesmo nome, testes
  só com `pass`, teste sem prefixo `test_`, `unittest.TestCase` em vez de
  `django.test.TestCase`, asserção que passa sempre) foram corrigidos na
  revisão de cada um.
- O PR #253 está **superado**: `git diff origin/dev origin/testes3` mostra que
  um merge dele **regrediria** `test_curriculo.py`, `test_dao.py`,
  `test_discente.py`, `requirements.txt` e `requirements-mutation.txt` (o #310
  e o #309 já estão melhores na `dev`); os testes de view do #253 são
  idênticos aos do #311. Fechar com referência a #308–#312.
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
- **`handler403` do projeto:** `core/views.py:error_403` (registrado em
  `suggestclasses/urls.py:27`) **não devolve 403**: chama `redirecionar()`, que
  faz `HttpResponseRedirect(request.GET.get('next', '/'))`. Portanto testes de
  negação de permissão devem esperar **302 com `response.url == '/'`**, não 403.
- **Isolamento de testes:** usar `django.test.TestCase` com `setUpTestData`
  (nunca `unittest.case.TestCase`, que não isola o banco). Ainda restam
  `unittest.case.TestCase` em `test_enquete_view.py` e `test_user_view.py`.
- **Cobertura de rotas (2026-11-06):** `core/urls.py` tem 154 rotas nomeadas e
  apenas 32 são exercitadas por `reverse()` nos testes (~21%); 122 sem
  cobertura, sobretudo `flow_*`, `turmas_*` e os 5 CRUDs `sugestao_*` por curso.
- **`solicitacao_turma_listar`:** é protegida por
  `@login_required(login_url='/suggestclasses/accounts/login')` (o login
  genérico do Django, não o `usuario/logar` do projeto). Anônimo recebe 302
  para `/suggestclasses/accounts/login?next=...`.
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

- [x] Revisar e mergear #308, #309 e #310 (2026-11-05).
- [x] Corrigir os problemas conhecidos do #311 (2026-11-06: 90 testes OK).
- [ ] Revisar e mergear #311 e #312 na `dev` (merge feito manualmente no GitHub).
- [ ] Remover o MutPy (`requirements-mutation.txt`, `mutation_settings.py`,
      seção do README) e avaliar uma alternativa.
- [ ] Fechar o PR #253 (superado por #308–#312; merge regrediria a `dev`).
- [ ] Avaliar as melhorias de teste apontadas em 2026-11-06: matriz
      parametrizada de smoke tests para as 122 rotas sem cobertura, migração
      dos 2 arquivos restantes de `unittest.case.TestCase` e remoção dos IDs de
      estrutura curricular fixos em `core/bo/sevices.py`.
- [ ] Apagar as 24 branches remotas antigas já mergeadas na `main` (a remoção
      em lote exige ação manual) e avaliar as não mergeadas
      (`feat/issue172`, `refactor/issue213-postgres`, `update-readme`,
      `tacianosilva-patch-2`).
- [ ] Avaliar a remoção de `matplotlib` de `requirements.txt` (o código de
      plotagem foi removido em `8422ada`).
- [ ] Abrir PR `dev` → `main` quando a `dev` estiver estável.
