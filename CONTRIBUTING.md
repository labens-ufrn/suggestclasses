# CONTRIBUTING

Contribuições sempre serão bem vindas, sejam pequenas ou grandes. Leia o código de conduta antes de abrir qualquer issue ou pull request.

## Issues

As issues são um espaço aberto para requisitar novas funcionalidades, mudança ou conserto. Também pode ser usadas como espaço para tirar dúvidas ou discutir ideias.

### Labels

Usamos algumas classificações para categorizar as issues, esses labels foram criados usango github-labels (https://github.com/idvogados/github-labels), veja:

- **Prioridade: Crítico, Alta, Média, Baixa**
  - Prioridades das issues de acordo com a necessidade de implementação.
- **Status: Abandonado, Bloqueado, Em Progresso, Aceitamos PR, Precisa Ser Revisado, Precisa De Mais Informações, NÃO MERGEAR!, Duplicado, Fora do Plano, Pronto para implementar, Ajuda bem vinda, Aprovado**
  - O status descreve a situação atual da issue ou do pull request.
- **Tipo: Mudança Titânica, Bug :bug:, Documentação, Funcionalidade, Refatoração, Testando, Manuntenção, CI, Questão, Discussão, Épico, Performance, Externo**
  - O tipo descreve características da tarefa em desenvolviment.
- **Esforço: de Esfoço 1 até 10**
  - Indica uma estimativa de esforço ou dificuldade para a realização da tarefa.

## Contribuir

Você pode contribuir tanto sugerindo novas ideias em nossas issues, como também criando um "fork" do repositório e submetendo sua PR para melhorar nosso conteúdo e código.

## Estrutura

O projeto é um Sistema Web que utiliza **Python 3** e o **framework Django 3.0.6** e banco de dados **MySql**. A camada view de páginas web é feito utilizando apenas o essencial, **Javascript**, **HTML**, **CSS** e a linguagem de **templates do Django**.

Nosso documentação se concentra na pasta `docs/` deste repositório, aqui uma descrição da estrutura:

| Arquivo/Pasta  	|   Descrição	|
|---	|---	|
|  `contrib/`	| Contém arquivos de configuração do ambiente de desenvolvimento.|
|  `core/`	    | Aplicativo Django, código base de todo o sistema. 	|
|  `dados/` 	| Contém scripts para downloads dos dados e povoamento da base de dados.	|
|  `docs/` 	    | Contém arquivos de documentação e imagens da modelagem do Sistema. |
|  `suggestclasses/` 	| Arquivos de configuração do Projeto Django.|

Ainda tem dúvida? Abre uma [Issue](https://github.com/labens-ufrn/suggestclasses/issues) que a gente responde!

## Desenvolvimento

Para rodar e fazer alterações locais na sua máquina, primeiro você deve fazer um *Fork* deste repositório e depois cloná-lo para sua máquina:

``` bash
git clone https://github.com/<seu_usuario>/suggestclasses
```

Depois, siga os passos descritos na página [README.md](https://github.com/labens-ufrn/suggestclasses/blob/master/README.md)!

## Contribuir

Deseja contribuir? Ficamos muito felizes! Aqui vai alguma dicas e regras que você deve ter em mente.

### Filosofia do projeto

Lembre que o objetivo desse portal é ser simples! Por favor evite adicionar complexidas que podem ser desnecessárias, principalmente a adição de bibliotecas.

### Boas práticas

Já está pronto para abrir uma *Pull Request*? Ótimo! Aqui vai algumas dicas de boas práticas para ajudar o processo de revisão:

1. Crie uma [Branch](https://git-scm.com/book/pt-br/v1/Ramifica%C3%A7%C3%A3o-Branching-no-Git-B%C3%A1sico-de-Branch-e-Merge) no seu *Fork*, com um nome descritivo!
2. Seja claro nos seus comitivos! Não precisa ser longo, uma frase descritiva do seu trabalho está ótimo!
3. Siga nossos conselhos de como preencher sua **PR**, vai nos ajudar a entender o que você fez!
4. Se você fez baseado numa issue, referencie ela!
5. Esteja aberto a sugestões, assim como estaremos também!

## Dúvidas ou sugestões?

Dúvidas e sugestões são sempre bem vindas! Estamos sempre respondendo issues!
