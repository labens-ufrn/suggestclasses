# Documento de Visão

Documento construído a partido do **Modelo BSI - Doc 001 - Documento de Visão** que pode ser encontrado no 
link: https://docs.google.com/document/d/1DPBcyGHgflmz5RDsZQ2X8KVBPoEF5PdAz9BBNFyLa6A/edit?usp=sharing

## Lista de Requisitos Funcionais

* Manter cadastro de Componentes Curriculares;
  * um componente curricular é de um tipo de componente;
  * um componente curricular tem:
    * código, nome, ementa, departamento, carga horária e modalidade;
    * equivalências e requisitos com outros componentes; 
    * data de criação.
* Manter cadastro de Turmas;
  * uma turma tem: código, professor, sala e horários (horário da turma);
  * uma turma é de um componente curricular;
  * uma turma tem um ou mais professores;
  * uma turma tem uma ou mais salas;
  * uma turma tem vários horários de aulas;
* Manter o cadastro de Horários de Aula;
  * um horário tem: 
    * um dia de semana, um turno, uma ordem (ordenação/identificador);
    * uma hora de início, uma hora de final;
* Manter o cadastro de Sugestões de Horário de Turma;
  * uma sugestão de horário é de uma turma;
  * uma sugestão de horário tem um horário de turma;
* Manter um cadastro de Centros
  * Um centro tem código, nome, sigla, endereço e site.
* Manter um cadastro de Departamentos
  * Um departamento tem código, nome, sigla, endereço e site.
* Manter o cadastro de Salas;
  * uma sala tem um número, um nome, capacidade, tamanho, bloco;
* Manter o cadastro de professores;
  * um professor tem: matrícula, nome, e-mail, telefone, área?
* Manter o cadastro de alunos;
  * um aluno tem: matrícula, nome, e-mail, telefone;
  * um aluno pode sugerir um horário de turma;
  * um aluno pode votar em uma sugestão de horário;
* Manter o cadastro de cursos;
  * um curso tem: código, nome, habilitação, turnos, modalidade;
* Manter cadastro de Estruturas Curriculares;
  * uma estrutura curricular tem: codigo, sigla, nome e ano_periodo;
  * uma estrutura curricular tem uma carga horária;
  * a carga horária é dividida entre horas obrigatórias, opcionais, eletivas e de atividades;
  * uma estrutura curricular é organizada em períodos;
  * cada período contém um conjunto de componentes curriculares;
  * componentes curriculares podem ser obrigatórios, opcionais ou eletivos;
* Manter Organização Curricular:
 * uma organização curricular tem id_curriculo_componente;
 * estrutura curricular;
 * componente curricular;
 * semestre
 * tipo_vinculo
 * nível
 
 ## Modelo Conceitual
