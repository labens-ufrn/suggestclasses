# Documento Lista de User Stories

Documento construído a partir do **Modelo BSI - Doc 004 - Lista de User Stories** que pode ser encontrado no
link: <https://docs.google.com/document/d/1Ns2J9KTpLgNOpCZjXJXw_RSCSijTJhUx4zgFhYecEJg/edit?usp=sharing>

## Descrição

Este documento descreve os User Stories criados a partir da Lista de Requisitos no [Documento de Visão](DocVisao.md). Este documento também pode ser adaptado para descrever Casos de Uso. Modelo de documento baseado nas características do processo easYProcess (YP).

## Histórico de revisões

| Data       | Versão |                           Descrição                            | Autor                          |
| :--------- | :----: | :------------------------------------------------------------: | :----------------------------- |
| 01/10/2022 | 0.0.1  |               Template e descrição do documento                | Renata Karla Araújo dos Santos |
| 01/10/2022 | 0.0.1  |                Detalhamento do User Story US00                 | Renata Karla Araújo dos Santos |
| 02/10/2022 | 0.0.2  |                Correções do User Story US00                    | Renata Karla Araújo dos Santos |
| 02/10/2022 | 0.0.2  |                Detalhamento do User Story US01                 | Renata Karla Araújo dos Santos |
| 03/10/2022 | 0.1.0  |                Detalhamento do User Story US01                 | Renata Karla Araújo dos Santos |


### User Story US00 - Manter o cadastro de Vínculo de Docente a Sugestão 

|               |                                                                                                                                                                                                                                    |
| ------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Descrição** | O sistema deve manter sugestão de turmas. Um vínculo de docente a sugestão tem: docente, sugestão, carga horária, descrição do horário, horários e a data de criação. O usuário administrador do sistema e o usuário docente podem realizar as operações de adicionar, alterar, remover e listar as sugestões de turmas cadastradas. |

| **Requisitos envolvidos** |                                           |
| ------------------------- | :---------------------------------------- |
| RF06                      | Cadastrar Sugestão de Turmas              |
| RF07                      | Alterar Sugestão de Turmas                |
| RF08                      | Consultar Sugestão de Turmas              |
| RF09                      | Vizualizar detalhes de Sugestão de Turmas |
| RF10                      | Excluir Sugestão de Turmas                |


|                         |           |
| ----------------------- | :-------- |
| **Prioridade**          | Essencial |
| **Estimativa**          | 8 h       |
| **Tempo Gasto (real):** |           |
| **Tamanho Funcional**   | 7 PF      |

| Testes de Aceitação (TA) |                                                                                                                                                                                                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Código**               | **Descrição**                                                                                                                                                                                                                                                                                                                                |
| **TA01.01**              | O usuário é redirecionado para a página de login social e tudo ocorre corretamente. Ele é redirecionado para a tela de sugestão de turmas da plataforma.                                                                                                                                                                                            |
| **TA01.02**              | O usuário é redirecionado para a página de login social e autenticação social falha. É exibida a mensagem: "Não foi possível realizar o login, Tente novamente". O usuário é redirecionado para a tela de login.                                                                                                                             |
| **TA01.03**              | O usuário solicita a exclusão de seu perfil na página de visualização de detalhes, uma notificação de confirmação é exibida em modal ou toast, a exclusão é realizada e a mensagem "Perfil excluído com sucesso" é exibida. O usuário é redirecionado para a tela principal.                                                                 |
| **TA01.04**              | O usuário solicita a exclusão de seu perfil na página de visualização de detalhes, a exclusão não ocorre e a mensagem "Tente novamente" é exibida. O usuário é redirecionado para a página de visualização de detalhes de usuário.                                                                                                           |
| **TA01.05**              | O usuário, na tela de detalhes, realiza alterações nas informações e seleciona para salvar,tudo ocorre corretamente e a mensagem "Tudo Okay!" é exibida. O usuário é redirecionado para a tela de detalhes com as novas informações.                                                                                                         |
| **TA01.06**              | O usuário, na tela de detalhes, realiza alterações nas informações e seleciona para salvar,ocorre uma falha na atualização e a mensagem "Problemas técnicos, Tente novamente..." é exbida. O usuário continua na mesma tela até solicitar para salvar novamente ou cancelar as alterações.                                                   |
| **TA01.07**              | O usuário, na tela de detalhes, realiza alterações nas informações e seleciona para salvar, o usuário preenche incorretamente alguma informação e a mensagem "Ops! Tem alguma coisa errada, verifique os dados e tente novamente". O usuário continua na mesma tela até alterar e solicitar para salvar novamente ou cancelar as alterações. |

### User Story US01 - Manter Cadastro de Enquetes

|               |                                                                                                                                                                                                                                                    |
| ------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Descrição** | O sistema deve manter um cadastro de enquetes. Uma enquete contém os seguintes atributos, nome, descrição, o número de votos, a data e a hora de início e fim, o curso, quantidade de discentes ativos, período, status, tipo, usuário e a data em que foi criado. O usuário administrador do sistema e o usuário docente podem realizar as operações de adicionar, alterar, remover e listar as enquetes cadastradas. |

| **Requisitos envolvidos** |                                            |
| ------------------------- | :----------------------------------------- |
| RF11                      | Cadastrar Enquetes                         |
| RF12                      | Alterar Enquetes                           |
| RF13                      | Consulta Enquetes                          |
| RF14                      | Visualizar Enquetes                        |
| RF15                      | Excluir Enquetes                           |

|                         |           |
| ----------------------- | :-------- |
| **Prioridade**          | Essencial |
| **Estimativa**          | 8 h       |
| **Tempo Gasto (real):** |           |
| **Tamanho Funcional**   | 7 PF      |

| Testes de Aceitação (TA) |                                                                                                                                                                                                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Código**               | **Descrição**                                                                                                                                                                                                                                                                                                                                |
| **TA01.01**              | O usuário é redirecionado para a página de login social e tudo ocorre corretamente. Ele é redirecionado para a tela de cadastro de enquetes da plataforma.                                                                                                                                                                                            |
| **TA01.02**              | O usuário é redirecionado para a página de login social e autenticação social falha. É exibida a mensagem: "Não foi possível realizar o login, Tente novamente". O usuário é redirecionado para a tela de login.                                                                                                                             |
| **TA01.03**              | O usuário solicita a exclusão de seu enquete na página de visualização de detalhes, uma notificação de confirmação é exibida em modal ou toast, a exclusão é realizada e a mensagem "Enquete excluído com sucesso" é exibida. O usuário é redirecionado para a tela principal.                                                                 |
| **TA01.04**              | O usuário solicita a exclusão da enquete na página de visualização de detalhes, a exclusão não ocorre e a mensagem "Tente novamente" é exibida. O usuário é redirecionado para a página de visualização de detalhes de usuário.                                                                                                           |
| **TA01.05**              | O usuário, na tela de detalhes, realiza alterações nas informações e seleciona para salvar,tudo ocorre corretamente e a mensagem "Tudo Okay!" é exibida. O usuário é redirecionado para a tela de detalhes com as novas informações.                                                                                                         |
| **TA01.06**              | O usuário, na tela de detalhes, realiza alterações nas informações e seleciona para salvar,ocorre uma falha na atualização e a mensagem "Problemas técnicos, Tente novamente..." é exbida. O usuário continua na mesma tela até solicitar para salvar novamente ou cancelar as alterações.                                                   |
| **TA01.07**              | O usuário, na tela de detalhes, realiza alterações nas informações e seleciona para salvar, o usuário preenche incorretamente alguma informação e a mensagem "Ops! Tem alguma coisa errada, verifique os dados e tente novamente". O usuário continua na mesma tela até alterar e solicitar para salvar novamente ou cancelar as alterações. |
