# Plano de Iteração

Este plano de iteração será usando na disciplina de Teste de Software.

## Calendário da Iterações

Iteração | Data início | Data Final | Apresentação | Gerente
-------- | ----------- | ---------- | ------------ | -------
It10     | 29/09/2022  | 06/10/2022 | 07/10/2022   | Wanessa
It11     | 08/10/2022  | 03/11/2022 | 04/11/2022   | Renata
It12     | 28/11/2022  | 05/12/2022 | 06/12/2022   | Gabriel
It13     | 05/12/2022  | 20/12/2022 | 20/12/2022   | Wanessa

* Observação: Cada Iteração de ser cadastrada como Milestones no GitHub.

## Descrição das Tarefas em cada Iteração

### T10 - Iteração 10 - Planejamento do Plano de Testes

A Iteração 10 começou dia 29/09/2022 e vai até 06/10/2022. As atividades dessa tarefa são:

* Criar um Milestone para os Testes no github e trabalhe usando GitFlow (trabalhar com branches);
* Atualização do Documento de Visão no formato Markdown;
  * Deve conter lista de requisitos funcionais, requisitos não funcionais, perfis de usuários e tabela de riscos;
  * Coloque duas ou três entidades por membro da equipe para fazer a lista inicial dos requisitos funcionais;
* Atualização do Documento de Modelos com o Modelo Conceitual (UML) ou Modelo de Dados (MER);
* Criação de um Plano de Release e Iteração para o Projeto indicando as atividades de cada iteração e o gerente, incluindo as atividades de Testes;
* Criação da Lista de User Stories para o Projeto, deve conter pelo menos 1 User Story por membro da equipe;
  * [Modelo aqui!](https://docs.google.com/document/d/1Ns2J9KTpLgNOpCZjXJXw_RSCSijTJhUx4zgFhYecEJg/edit#);
  * Um User Store pode ser formado de um ou mais requisitos funcionais;
* Definir qual será o User Story (Caso de Uso) *base* para implementação, chame de US00;
* Criação do Plano de Testes para o Projeto;
* Coloque links para a documentação no README.md do repositório;

Nesta tarefa temos atividades diferentes para dois perfis Gerentes e Analistas:

Gerentes:

* Criar Milestones para a Iteração 10;
* Definir e descrever as tarefas (issues) da Iteração 10 (milestones) e alocar as issues para cada membro da equipe;
* Definir que parte do documento de visão cada membro da equipe vai preparar;
* Definir que parte do documento com modelo conceitual cada membro da equipe vai preparar;
* Definir qual User Story cada membro da equipe vai especificar/detalhar;
* Detalhar ou Especificar um US é cria a descrição (estória do usuário) e os testes de aceitação);
* trabalhar usando GitFlow (trabalhar com branches);
* Fechar tarefas se concluída;

Analistas:

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* trabalhar usando GitFlow (trabalhar com branches);
* Enviar commits da parte do documento de divisão que preparou;
* Enviar commits da parte do documento com Modelo Conceitual que preparou;
* Enviar commits do User Story que detalhou;
* Enviar commits da contagem do User Story que detalhou;
* Avisar ao gerente quando concluir uma tarefa;

O gerente deve enviar nesta tarefa o link do repositório e o link dos documentos.

### T11 - Iteração 11 - Inicialização Testes com TDD

A Iteração 11 começou dia 08/10/2022  e vai até 03/11/2022 . As atividades dessa tarefa são:

* Atualização do Documento de Visão (formato Markdown), adicionar requisitos funcionais, se necessário;

Gerentes:

* Criar Milestones da Iteração 11;
* Definir e descrever as tarefas (issues) da Iteração 11 (milestones) e
alocar as issues para cada membro da equipe;
* Definir quem vai construir a Arquitetura Geral do Sistema que faz parte do documento com modelo conceitual cada membro da equipe vai preparar;
* O gerente deve fazer a contagem indicativa do tamanho funcional de Projeto;
* Definir quem vai fazer a contagem detalhada do tamanho funcional de cada User Story;
* Fechar tarefas se concluída;

Analistas:

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Avisar ao gerente quando concluir uma tarefa;

Desenvolvedor

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Enviar commits da implementação do User Story;
* Enviar commits da implementação de testes de unidade do User Story que implementou;
* Avisar ao gerente quando concluir uma tarefa;

Testador

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Executar cada teste de aceitação do User Story, anotando o resultado em um Markdown dos
Resultados dos Testes de Aceitação;
* Cadastrar issues de bugs caso os Testes de Aceitação não passem;
* Avisar ao gerente quando concluir uma tarefa;

O gerente deve enviar nesta tarefa o link do repositório e o link dos documentos.

### T12 - Iteração 12 - Desenvolvimento e Ampliação da Cobertura

A Iteração 12 começou dia 28/11/2022  e vai até 05/12/2022 . As atividades dessa tarefa são:

* Atualizar o README.md do repositório colocando link para o plano de testes que deve estar na pasta docs/;
* Atualização do Documento de Visão no formato Markdown, crie um diretório "docs"no repositório;
    * Deve conter lista de requisitos funcionais, requisitos não funcionais, perfis de usuários e tabela de riscos;
    * Coloque duas ou três entidades por membro da equipe para fazer a lista inicial dos requisitos funcionais;
* Atualização do Documento de Modelos com o Modelo Conceitual (UML) ou Modelo de Dados (MER), pode usar o Mermaid.
* Atualizar o Plano de Release e Iteração para o Projeto indicando as atividades de cada iteração e o gerente, incluindo as atividades de Testes;
* Adicionar Testes de Aceitação no documento Lista de User Stories para o Projeto, deve conter pelo menos 1 User Story por membro da equipe;
* Atualizar o documento Plano de Testes;
* Executar a análise do Sonarqube nos dias de aula;
* Executar a análise de Cobertura de Testes atingindo no mínimo 50% de cobertura ou ampliando em 30% a cobertura de projeto já em desenvolvimento com testes;
* Adicionar GitHub Actions no projeto para executar automaticamente os testes e o sonarqube;
* Escrever um manual de execução do projeto
* Coloque links para a documentação no README.md do repositório;

Gerentes:

* Criar Milestones da Iteração 12;
* Definir e descrever as tarefas (issues) da Iteração 12 (milestones) e
alocar as issues para cada membro da equipe;
* Definir quem vai construir a Arquitetura Geral do Sistema que faz parte do documento com modelo conceitual cada membro da equipe vai preparar;
* O gerente deve fazer a contagem indicativa do tamanho funcional de Projeto;
* Definir quem vai fazer a contagem detalhada do tamanho funcional de cada User Story;
* Fechar tarefas se concluída;

Analistas:

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Avisar ao gerente quando concluir uma tarefa;

Desenvolvedor

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Enviar commits da implementação do User Story;
* Enviar commits da implementação de testes de unidade do User Story que implementou;
* Avisar ao gerente quando concluir uma tarefa;

Testador

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Executar cada teste de aceitação do User Story, anotando o resultado em um Markdown dos
Resultados dos Testes de Aceitação;
* Cadastrar issues de bugs caso os Testes de Aceitação não passem;
* Avisar ao gerente quando concluir uma tarefa;

O gerente deve enviar nesta tarefa o link do repositório e o link dos documentos.


### T13 - Iteração 13 - Desenvolvimento e Ampliação da Cobertura

A Iteração 13 começou dia 05/12/2022  e vai até 20/12/2022. As atividades dessa tarefa são:

* Atualizar o Plano de Release e Iteração para o Projeto indicando as atividades de cada iteração e o gerente, incluindo as atividades de Testes;
* Adicionar Testes de Aceitação no documento Lista de User Stories para o Projeto, deve conter pelo menos 1 User Story por membro da equipe;
* Atualizar o documento Plano de Testes;
* Executar a análise do Sonarqube nos dias de aula;
* Executar a análise de Cobertura de Testes atingindo no mínimo 50% de cobertura ou ampliando em 30% a cobertura de projeto já em desenvolvimento com testes;
* Adicionar GitHub Actions no projeto para executar automaticamente os testes e o sonarqube;
* Atualizar o manual de execução do projeto
* Coloque links para a documentação no README.md do repositório;

Gerentes:

* Criar Milestones da Iteração 13;
* Definir e descrever as tarefas (issues) da Iteração 13 (milestones) e
alocar as issues para cada membro da equipe;
* O gerente deve fazer a contagem indicativa do tamanho funcional de Projeto;
* Definir quem vai fazer a contagem detalhada do tamanho funcional de cada User Story;
* Fechar tarefas se concluída;

Analistas:

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Avisar ao gerente quando concluir uma tarefa;

Desenvolvedor

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Enviar commits da implementação do User Story;
* Enviar commits da implementação de testes de unidade do User Story que implementou;
* Avisar ao gerente quando concluir uma tarefa;

Testador

* Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
* Executar cada teste de aceitação do User Story, anotando o resultado em um Markdown dos
Resultados dos Testes de Aceitação;
* Cadastrar issues de bugs caso os Testes de Aceitação não passem;
* Avisar ao gerente quando concluir uma tarefa;
* Criar Relatório de Testes de Módulo/Sistema

O gerente deve enviar nesta tarefa o link do repositório e o link dos documentos.
