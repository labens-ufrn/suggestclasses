# Plano de Iteração

Este plano de iteração será usando como exemplo da disciplina Engenharia de Software II.

## Calendário da Iterações

Iteração | Data início | Data Final | Apresentação | Gerente
-------- | ----------- | ---------- | ------------ | -------
It0      | 21/02/2020  | 29/02/2020 | -            | Gerente 1
It1      | 02/03/2020  | 14/03/2020 | 19/03/2020   | Gerente 1
It2      | 16/03/2020  | 04/04/2020 | 03/04/2020   | Gerente 2
It3      | 06/04/2020  | 25/04/2020 | 24/04/2020   | Gerente 3
It4      | 27/04/2020  | 16/05/2020 | 15/05/2020   | Gerente 4
It5      | 18/05/2020  | 06/06/2020 | 05/06/2020   | Gerente 5
It6      | 08/06/2020  | 27/06/2020 | 26/06/2020   | Gerente 6

* Observação: Cada Iteração de ser cadastrada como Milestones no GitHub.

## Descrição das Tarefas em cada Iteração

### T01 - Iteração 0 - Planejamento

A Iteração 0 começou dia 21/02/2020 e vai até 29/02. As atividades dessa tarefa são:

- Criar repositório do projeto no GitHub com .gitignore para a linguagem do projeto;
- Definir tecnologia do projeto e colocar no README.md do repositório;
- Postar o link de tutoriais com a tecnologia do seu projeto no fórum do sigaa e colocar no README.md;
- Criação do Documento de Visão no formato Markdown ou Latex, crie um diretório "docs" no repositório (Modelo aqui!);
- Criação do Modelo Conceitual e Modelo de Dados no formato Markdown ou Latex, coloque no diretório "docs" do repositório (Modelo aqui!);
- Coloque links para a documentação no no README.md do repositório;
- Colocar Estrutura inicial do Projeto no repositório;

Nesta tarefa temos atividades diferentes para dois perfis Gerentes e Analistas:

Gerentes:

- Criar Milestones para a Iteração 0 e da Iteração 1;
- Definir e descrever as tarefas (issues) da Iteração 0 e 1 (milestones) e alocar as issues para cada membro da equipe;
- Definir que parte do documento de visão cada membro da equipe vai preparar;
- Definir que parte do documento com modelo conceitual cada membro da equipe vai preparar;
- Criar o repositório de software no GitHub;
- Fechar tarefas se concluída;

Analistas:

- Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
- Enviar commits da parte do documento de divisão que preparou;
- Enviar commits da parte do documento com Modelo Conceitual que preparou;
- Avisar ao gerente quando concluir uma tarefa;

O gerente deve enviar nesta tarefa o link do repositório e o link dos dois documentos.

### T01 - Iteração 1 - Inicialização

A Iteração 1 começou dia 02/03 e vai até 14/03. As atividades dessa tarefa são:

- Atualização do Documento de Visão (formato Markdown), adicionar requisitos funcionais, se necessário;
- Criar documento com a lista de User Stories, coloque no diretório "docs" do repositório
  - [Modelo aqui!](https://docs.google.com/document/d/1Ns2J9KTpLgNOpCZjXJXw_RSCSijTJhUx4zgFhYecEJg/edit#);
  - Deve ser detalhado pelo menos três User Stories;
  - Um User Store pode ser formado de um ou mais requisitos funcionais;
- Definir qual será o User Story (Caso de Uso) *base* para implementação, chame de US00 ou CDU00;
- Criar modelo (imagem) da Arquitetura Geral do Sistema e descreva cada parte da arquitetura
 (não é o documento Arquitetural completo);
  - [Modelo aqui!](https://docs.google.com/document/d/1i80vPaInPi5lSpI7rk4QExnO86iEmrsHBfmYRy6RDSM/edit?usp=sharing);
- Criar documento com a Contagem de Ponto de Função, coloque no diretório "docs" do repositório
  - [Modelo aqui!](https://docs.google.com/document/d/1s4bMbrpQt9RF6tymXvI0HHfQO14hMyL08UxmX1eH82s/edit?usp=sharing);
  - Faça a contagem indicativa do tamanho funcional do software;
  - Faça a contagem detalhada do tamanho funcional de pelo menos três User Stories;
 - Criar documento com o Termo de Abertura do Projeto, no google docs
   - [Modelo Aqui!](https://docs.google.com/document/d/1xGwEppR2qmQ7H3EdevWBCWferzY3RuoZim_GEz6LZ90/edit?usp=sharing);

Gerentes:

- Criar Milestones da Iteração 1;
- Definir e descrever as tarefas (issues) da Iteração 1 (milestones) e
alocar as issues para cada membro da equipe;
- Definir qual User Story cada membro da equipe vai especificar/detalhar;
   - Detalhar ou Especificar um US é cria a descrição (estória do usuário) e os testes de aceitação);
- Definir quem vai construir a Arquitetura Geral do Sistema que faz parte do documento com modelo conceitual cada membro da equipe vai preparar;
- O gerente deve fazer a contagem indicativa do tamanho funcional de Projeto;
- Definir quem vai fazer a contagem detalhada do tamanho funcional de cada User Story;
- Fechar tarefas se concluída;

Analistas:

- Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
- Enviar commits do User Story que detalhou;
- Enviar commits da contagem do User Story que detalhou;
- Avisar ao gerente quando concluir uma tarefa;

Desenvolvedor

- Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
- Enviar commits da implementação do User Story;
- Enviar commits da implementação de testes de unidade do User Story que implementou;
- Avisar ao gerente quando concluir uma tarefa;

Testador

- Trabalhar nas tarefas e realizar pequenos commits marcando com a hashtag da issue;
- Executar cada teste de aceitação do User Story, anotando o resultado em um Markdown dos
Resultados dos Testes de Aceitação;
- Cadastrar issues de bugs caso os Testes de Aceitação não passem;
- Avisar ao gerente quando concluir uma tarefa;
