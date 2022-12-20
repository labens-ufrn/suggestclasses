# Relatório de Testes de Módulo/Sistema
# Suggest Classes
Responsabilidade do Testador

## Legenda

* Teste : Código ou identificação do Teste.
* Descrição: Descrição dos passos e detalhes do teste a ser executado.
* Especificação: Informações sobre a função testada e se ela de acordo com a especificação do caso de uso.
* Resultado: Resultado do teste, modificações sugeridas ou resultados do teste. No caso de erro ou problema na execução do teste descrever o erro em detalhes e adicionar print's das telas.

### US001 – Sugestão de Turmas

| Teste      |      Descrição      |        Especificação          | Resultado            |
| :--------- | :-----------------: | :---------------------------: | :------------------- |
| Teste 01: eh_mesma_sugestao | A1 - Incluir Sugestões 1 e 2. A1.1. O sistema verifica se são iguais.  A1.2. Fim do fluxo. | Especificação ok.| Ok. |

### US002 – Sugestão view

| Teste      |      Descrição      |        Especificação          | Resultado            |
| :--------- | :-----------------: | :---------------------------: | :------------------- |
| Teste 01: solicitação_listar | A1 - Listar solicitações A1.1. O sistema executa o fluxo de solicitações de sugestões A1.2. O sistema apresenta A1.3. Fim do fluxo. | Especificação ok.| Ok. |

### US003 – Turmas view

| Teste      |      Descrição      |        Especificação          | Resultado            |
| :--------- | :-----------------: | :---------------------------: | :------------------- |
| Teste 01: get_turmas | A1 - Pegar turmas A1.1. O sistema executa o fluxo de turmas A1.2. O sistema executa a função A1.3. Fim do fluxo.| Especificação ok.| Ok. |

### US004 – Flow view

| Teste      |      Descrição      |        Especificação          | Resultado            |
| :--------- | :-----------------: | :---------------------------: | :------------------- |
| Teste 01: get_flow_turmas | A1 - Flow turmas	A1.1. O sistema executa o fluxo de turmas A1.2. O sistema executa a função A1.3. Fim do fluxo.| Especificação ok.| Ok. |

### US005 – Dao

| Teste      |      Descrição      |        Especificação          | Resultado            |
| :--------- | :-----------------: | :---------------------------: | :------------------- |
| Teste 01: get_cursos | A1 - get Cursos A1.1. O sistema executa o fluxo de cursos A1.2. O sistema executa a função A1.3. Fim do fluxo.| Especificação ok.| Ok. |
| Teste 02: get_cursos_by_centro | A1 - get Cursos	do centro A1.1. O sistema executa o fluxo de cursos A1.2. O sistema executa a função verifica e retorna A1.3. Fim do fluxo.| Especificação ok.| Ok. |
| Teste 02: get_cursos_by_codigo | A1 - get Cursos	por código A1.1. O sistema executa o fluxo de cursos A1.2. O sistema executa a função verifica o código e retorna A1.3. Fim do fluxo | Especificação ok.| Ok. |




## Relatório de Bugs e Providências
Responsabilidade do Gerente

|      Teste        |           Providência            |        Tarefas/tipo            |
| :---------------- | :------------------------------: | :----------------------------- |
| Teste 01: test_discente | Corrigir a falha no arquivo test_docente.py na definição de função de test_get_chefes, detectada ao executar o teste de mutação. | Tarefa: Bug em test_docente.py. |
| Teste 02: test_curriculo  | Melhoria nos testes de curriculo, pois foi identificado um mutante sobrevivente após rodar o teste de mutação com o MutPy. | Tarefa: Melhoria em curriculo.py. |
| Teste 03: test_sugestao | Corrigir a falha no arquivo test_sugestao.py na função test_choques_solicitacao, detectada ao executar coverage run -m unittest discover. | Tarefa: Bug em test_sugestao.py. |
