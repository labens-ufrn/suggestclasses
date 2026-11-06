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
- **Estado do CI da `dev`:** 🟢 verde após os merges de #308, #309, #310, #311,
  #312 e #313.
- **Ambiente local (desde 2026-11-05):** `.venv` com Python 3.12.15 (`uv`),
  `.env` local (`chmod 600`, senha aleatória do `sc_user`) e PostgreSQL 16.2
  em espaço de usuário (`pgserver` 0.1.4, `systemd --user`
  `postgresql-local.service`, `127.0.0.1:5432`). Detalhes no `AGENTS.md`.
  Suíte local na `dev` após o #313 (2026-11-06): **75 testes OK** em ~16 s com
  `--keepdb`. A contagem caiu de 90 para 75 porque o #313 substituiu 18 testes
  copiados por 2 testes parametrizados com `subTest`, que cobrem 44 rotas.

---

## 🌿 Fluxo de Branches (desde 2026-11-05)

- `main`: branch de release.
- `dev`: branch de integração do desenvolvimento, criada a partir da `main`
  (`0111d22`) em 2026-11-05.
- Feature branches saem da `dev` e abrem PR para a `dev`; cada PR é revisado
  antes do merge. Commits seguem Conventional Commits.

---

## 🔀 Pull Requests

Divisão do PR #253 (`testes3` → `main`, "Testes e bug", aberto em 2022-12-10
por Wanessa Bezerra) em PRs menores para a `dev`, todos na milestone **Iteração 14: Modernização e
Integração na dev** (#15, criada em 2026-11-05, sem prazo).

| Ordem | PR | Branch | Conteúdo | Status |
|---|---|---|---|---|
| 1 | #308 | `fix/ci-django52-compat` | CI na `dev` + Python 3.12, `django-filter` 25.1, `assertEqual`, redirects com barra final | 🟢 MERGED em dev (2026-11-05, `ea9fc74`) |
| 2 | #309 | `chore/separar-dependencias` | `requirements-dev`/`requirements-mutation`, `mutation_settings.py`, README | 🟢 MERGED em dev (2026-11-05) |
| 3 | #310 | `test/bo-dao` | Testes de BO/DAO | 🟢 MERGED em dev (2026-11-05, `ca16e78`) |
| 4 | #311 | `test/views` | Testes de views (perfil, geografia, sugestão, solicitações) | 🟢 MERGED em dev (2026-11-06, `01c8da8`) |
| 5 | #312 | `docs/agents-memory` | `AGENTS.md` (fluxo de branches) + este `MEMORY.md` | 🟢 MERGED em dev (2026-11-06, `99f4692`) |
| 6 | #313 | `refactor/test-parametrizacao` | Testes de fluxogramas e turmas parametrizados (44 rotas) | 🟢 MERGED em dev (2026-11-06, `5dc6745`) |

- **Todos os PRs da divisão do #253 foram mergeados na `dev`.** Não há PR
  aberto no momento.
- Os problemas originais dos PRs (testes duplicados com o mesmo nome, testes
  só com `pass`, teste sem prefixo `test_`, `unittest.TestCase` em vez de
  `django.test.TestCase`, asserção que passa sempre) foram corrigidos na
  revisão de cada um.
- **O PR #253 foi fechado sem merge em 2026-11-06**, com o laudo publicado no
  próprio PR. `git diff origin/dev origin/testes3 --stat` mostrava
  16 arquivos, 231 inserções e **497 deleções** em relação à `dev`: mergear
  removeria os gatilhos de `dev` do workflow, faria downgrade de
  `Django==5.2.17` para `5.2.16`, reverteria `'core.apps.CoreConfig'` para
  `'core'`, apagaria os avisos de depreciação do MutPy e **apagaria este
  `MEMORY.md`**. O diagnóstico que ele produziu virou as issues #314–#321.
- A issue #256 ("Testes em Sugestão de Geografia Views", de 2022) foi
  **fechada em 2026-11-06** como resolvida pelo #311.
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
- **Cobertura de rotas (2026-11-06, após o #313):** `core/urls.py` tem 154
  rotas nomeadas; 53 são exercitadas por `reverse()` nos testes (~34%) e **101
  não têm cobertura**, sobretudo os CRUDs `sugestao_*` por curso, `enquete_*`
  e `ajax_*`. Rastreado na issue #317.
- **`solicitacao_turma_listar`:** é protegida por
  `@login_required(login_url='/suggestclasses/accounts/login')` (o login
  genérico do Django, não o `usuario/logar` do projeto). Anônimo recebe 302
  para `/suggestclasses/accounts/login?next=...`.
- **Banco de testes:** o papel do PostgreSQL precisa de `CREATEDB` e `INHERIT`
  (ver `AGENTS.md`).
- **Testes de mutação (decisão de 2026-11-05):** o MutPy **não funciona mais**
  e a remoção está rastreada na issue #319. Fato (PyPI): `mutpy` 0.6.1
  (2019-11-17) declara suporte até Python 3.7 e `django-mutpy` 0.1.2
  (2017-08-18) até Python 3.6; o Django 5.2 exige Python >= 3.10. A depreciação
  está documentada no README e no `requirements-mutation.txt` (#309). Não há
  job de mutação no CI. Hipótese a avaliar: migrar para `mutmut` ou
  `cosmic-ray`.
- **`selenium`/`webdriver-manager`:** mantidos em `requirements-dev.txt` por
  decisão da revisão do #309, embora ainda não sejam usados no código.
- **`INSTALLED_APPS`:** manter `'core.apps.CoreConfig'` (revertida a troca por
  `'core'` na revisão do #309).
- **Identidade git:** este clone não tem `user.name`/`user.email`
  configurados; os commits do agente usam variáveis `GIT_AUTHOR_*` e
  `GIT_COMMITTER_*`.
- **Parametrização de smoke tests (padrão adotado no #313):** em vez de copiar
  um teste por rota, usar uma tabela curada `(nome_da_rota, status_esperado)` e
  um laço com `self.subTest(rota=nome)`. O status esperado é explícito por
  rota (um laço "tudo 200" cego aceitaria redirect como falso positivo) e, para
  status 200, exigir `response.templates` evita aceitar página de erro com 200.
  `subTest` mantém a rota visível no relatório de falha.
- **Análise de PR antigo (lição do #253):** comparar por conteúdo
  (`git diff origin/dev origin/<branch> --stat` e `git show <ref>:<arquivo>`),
  não por número de commits ou por `git log --cherry-pick`. O #253 tinha 25
  commits "exclusivos", mas todo o conteúdo já estava na `dev` em versões
  melhores; mergear teria regredido 7 arquivos.

---

## 🐛 Issues Abertas (criadas em 2026-11-06)

Todas na milestone **Iteração 14: Modernização e Integração na dev**, com
evidência, impacto, proposta e critério de aceite no corpo.

| Issue | Título | Labels |
|---|---|---|
| #314 | Links `'/core/...'` em 5 módulos de views apontam para rotas inexistentes (83 ocorrências) | `Tipo: Bug`, `Prioridade: Alta` |
| #315 | `handler403` devolve 302 para `/` em vez de 403 | `Tipo: Discussão`, `Prioridade: Médio` |
| #316 | Migrar `test_enquete_view` e `test_user_view` para `django.test.TestCase` | `Tipo: Testando`, `Prioridade: Médio` |
| #317 | Cobrir as 101 rotas sem teste com matriz de permissão parametrizada | `Tipo: Épico`, `Tipo: Testando`, `Prioridade: Médio` |
| #318 | Remover IDs de estrutura curricular fixos de `core/bo/sevices.py` (13 ocorrências) | `Tipo: Refatoração`, `Prioridade: Médio` |
| #319 | Remover o MutPy do repositório | `Tipo: Manuntenção`, `Prioridade: Baixa` |
| #320 | Remover `matplotlib` de `requirements.txt` | `Tipo: Manuntenção`, `Prioridade: Baixa` |
| #321 | Padronizar o login: `usuario/logar` x `accounts/login` | `Tipo: Bug`, `Prioridade: Baixa` |

---

## 📋 Pendências

- [x] Revisar e mergear #308, #309 e #310 (2026-11-05).
- [x] Corrigir os problemas conhecidos do #311 (2026-11-06: 90 testes OK).
- [x] Mergear #311, #312 e #313 na `dev` (2026-11-06: `01c8da8`, `99f4692`,
      `5dc6745`).
- [x] Fechar o PR #253 e a issue #256 (2026-11-06).
- [x] Criar as issues #314–#321 com o diagnóstico levantado na revisão
      (2026-11-06).
- [ ] Remover o MutPy (#319) e o `matplotlib` (#320).
- [ ] Corrigir os links `'/core/...'` (#314) e o `handler403` (#315).
- [ ] Migrar os 2 arquivos restantes de `unittest.case.TestCase` (#316).
- [ ] Ampliar a cobertura das 101 rotas sem teste (#317).
- [ ] Remover os IDs de estrutura curricular fixos em `core/bo/sevices.py`
      (#318).
- [ ] Padronizar o login (#321).
- [ ] Apagar as 24 branches remotas antigas já mergeadas na `main` (a remoção
      em lote exige ação manual) e avaliar as não mergeadas
      (`feat/issue172`, `refactor/issue213-postgres`, `update-readme`,
      `tacianosilva-patch-2`).
- [ ] Abrir PR `dev` → `main` quando a `dev` estiver estável.
