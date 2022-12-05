# Documento de Visão

Documento construído a partido do **Modelo BSI - Doc 001 - Documento de Visão** que pode ser encontrado no
link: <https://docs.google.com/document/d/1DPBcyGHgflmz5RDsZQ2X8KVBPoEF5PdAz9BBNFyLa6A/edit?usp=sharing>

## Perfis de Usuários

O sistema poderá ser utilizado por diversos usuários. Temos os seguintes perfis:

* Perfil Aluno
	Este usuário utiliza o sistema para verificar suas sugestões de horários para turmas de componentes curriculares de um curso em um certo período, horário aprovado     das turmas, etc.

* Perfil Professor
	Este usuário utiliza o SuggestClasses para o cadastro de sugestões de horários para turmas de componentes curriculares de um curso em um certo período, horário         aprovado das turmas, etc.

## Lista de Requisitos Funcionais

* Manter o cadastro de Centros;
  * um centro tem: id de unidade, código, nome, sigla, endereço e site;
* Manter o cadastro de Departamentos;
  * um departamento tem: id de unidade, código, nome, sigla, endereço, site e centro.
  * um departameto pertence a um centro;
* Manter o cadastro de Docentes;
  * um docente tem: siape, nome, sexo, formação, tipo de jornada de trabalho, vínculo, categoria, classe funcional, id da unidade de lotação, lotação, departamento, admissão e usuário;
  * um docente pertence a um departamento;
* Manter o cadastro de Cursos;
  * um curso tem: código, nome, coordenador, nível, grau, modalidade, turno, centro;
  * um curso faz parte de um centro;
  * um curso tem um coordenador que é docente;
* Manter o cadastro de Salas;
  * uma sala tem: número, nome, sigla, capacidade, tamanho, bloco, centro, campus;
  * as salas fazem parte de um centro;
* Manter o cadastro de Componentes Curriculares;
  * um componente curricular é de um tipo de componente;
  * um componente curricular tem:
    * código, nível, nome, ementa, carga horária, carga horária teórica, carga horária prática, carga horária do estágio, carga horária total, carga horária do docente, carga horária ead, carga horária máxima ead;
    * equivalências, requisitos com outros componentes, corequisito, modalidade e departamento;
* Manter o cadastro de Estruturas Curriculares;
  * uma estrutura curricular tem codigo, nome;
  * uma estrutura curricular tem semestre de conclusão mínimo, ideal e máximo;
  * uma estrutura curricular tem uma carga horária;
  * a carga horária é dividida entre horas obrigatórias, opcionais, eletivas e de atividades;
  * uma estrutura curricular é organizada em períodos;
  * cada período contém um conjunto de componentes curriculares;
  * componentes curriculares podem ser obrigatórios, opcionais ou eletivos;
  * componentes curriculares tem período de entrada, ano de entrada, observações e cursos;
* Manter o cadastro de Organização Curricular;
  * uma organização curricular tem:
    * código, estrutura curricular, componente curricular, semestre, tipo de vínculo, nível.
* Manter o cadastro de Horários de Aula;
  * um horário tem:
    * um dia de semana, um turno, uma ordem (ordenação/identificador);
    * uma hora de início, uma hora de final;
* Manter o cadastro de Turmas;
  * uma turma tem: código, professor, sala e horários (horário da turma);
  * uma turma é de um componente curricular;
  * uma turma tem um ou mais professores;
  * uma turma tem uma ou mais salas;
  * uma turma tem vários horários de aulas;
  * uma turma tem local, ano, périodo, data inicio, data fim, descrição do horário, total de solicitações, capacidade de alunos, tipo, distância, data de consolidação, agrupadora, id de turma agrupadora, quantidade de aulas lançadas, situação da turma, convênio e modalidade dos participantes;
* Manter o cadastro de Sugestões de Horário de Turma;
  * uma sugestão de horário é de uma turma;
  * uma sugestão de horário tem um horário de turma;
  * Uma sugestão de horário de turma tem: código, docente, componente curricular, campus da turma, local, ano, período, descrição do horário, horários, total de solicitações, capacidade de alunos, tipo, semestre, tipo vínculo, curso, criador, data em que foi criado;
* Manter o cadastro de Função Gratificada;
  * uma função gratificada tem: siape, nome, situação do servidor, id de unidade, lotação, sigla, início, fim, id da unidade de designação, unidade designação, atividade, observações;
* Manter o cadastro de Discentes;
  * um aluno tem: matrícula, nome, sexo, ano de ingresso, período de ingresso, tipo de discente, status, sigla, nível de ensino, id do curso, nome do curso, modalidade da educação, id da unidade, nome da unidade, id da unidade gestora e usuário;
  * um aluno pode sugerir um horário de turma;
  * um aluno pode votar em uma sugestão de horário;
* Manter o cadastro de Solicitação de Turma;
  * uma solicitação de turma tem usuário;
  * uma solicitação de turma tem um solicitador;
  * uma solicitação de turma tem uma sugestão de turma;
  * uma solicitação de turma tem a data em que foi criada;
* Manter o cadastro de Vínculo do Docente;
  * O vínculo precisa ter: docente, turma, carga horária, horários e a data em que foi criada;
* Manter o cadastro de Período Letivo;
  * um período letivo tem nome, ano e período;
  * um período letivo tem data de início, fim e consolidação;
  * um período letivo tem status e observações;
* Manter o cadastro de Enquete;
  * Uma enquete tem: nome, descrição, o número de votos, a data e a hora de inicio e fim, o curso, quantidade de discentes ativos, período, status, tipo, o usuário e a data em que foi criado;
* Manter o cadastro de Voto de Turma;
  * uma votação de turma tem enquete, discente e componente curricular;
  * uma votação de turma tem horários, tipo e a data de criação;
* Manter o cadastro de Vínculo de Docente a Sugestão;
  * um vínculo de docente a sugestão tem: docente, sugestão, carga horária, descrição do horário, horários e a data de criação;
* Manter o cadastro de Histórico;
  * um histórico tem discentes;
  * um histórico tem componentes curriculares;
  * um histórico semestre e a data de criação.

## Lista de Requisitos não-Funcionais

* RNF01 - Deve ser acessível via navegador
* RNF02 - Deve rodar em Windows e Linux
* RNF03 - Deve ser feito o log de ações dos usuários

## Modelo Conceitual

Abaixo apresentamos o modelo ER inicial.

 ![Modelo ER](https://github.com/labens-ufrn/suggestclasses/blob/doc-visao/docs/modelos/Modelo%20ER%20-%20SuggestClasses2.png)

