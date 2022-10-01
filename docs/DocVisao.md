# Documento de Visão

Documento construído a partido do **Modelo BSI - Doc 001 - Documento de Visão** que pode ser encontrado no
link: <https://docs.google.com/document/d/1DPBcyGHgflmz5RDsZQ2X8KVBPoEF5PdAz9BBNFyLa6A/edit?usp=sharing>

## Lista de Requisitos Funcionais

* Manter um cadastro de Centros
  * Um centro tem: id de unidade, código, nome, sigla, endereço e site.
* Manter um cadastro de Departamentos
  * Um departamento tem: id de unidade, código, nome, sigla, endereço, site e centro.
* Manter o cadastro de Docentes;
  * Um docente tem: siape, nome, sexo, formação, tipo de jornada de trabalho, vínculo, categoria, classe funcional, id da unidade de lotação, lotação, departamento, admissão e usuário.
* Manter o cadastro de Cursos;
  * um curso tem: código, nome, coordenador, nível, grau, modalidade, turno, centro;
* Manter o cadastro de Salas;
  * uma sala tem um número, nome, sigla, capacidade, tamanho, bloco, centro, campus;
* Manter cadastro de Componentes Curriculares;
  * um componente curricular é de um tipo de componente;
  * um componente curricular tem:
    * código, nível, nome, ementa, carga horária, carga horária teórica, carga horária prática, carga horária do estágio, carga horária total, carga horária do docente, carga horária ead, carga horária máxima ead;
    * equivalências, requisitos com outros componentes, corequisito, modalidade e departamento;
* Manter cadastro de Estruturas Curriculares;
  * uma estrutura curricular tem codigo, nome;
  * uma estrutura curricular tem semestre de conclusão mínimo, ideal e máximo;
  * uma estrutura curricular tem uma carga horária;
  * a carga horária é dividida entre horas obrigatórias, opcionais, eletivas e de atividades;
  * uma estrutura curricular é organizada em períodos;
  * cada período contém um conjunto de componentes curriculares;
  * componentes curriculares podem ser obrigatórios, opcionais ou eletivos;
  * componentes curriculares tem período de entrada, ano de entrada, observações e o curso;
* Manter cadastro de Turmas;
  * uma turma tem: id de turma, código, docente, sala e horários (horário da turma);
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
* Manter o cadastro de Docentes;
  * um docente tem: matrícula, nome, sexo, formação, jornada de trabalho, vínculo, categoria, classe funcional, unidade de lotação, lotação.
* Manter o cadastro de alunos;
  * um aluno tem: matrícula, nome, sexo, e-mail, telefone;
  * um aluno pode sugerir um horário de turma;
  * um aluno pode votar em uma sugestão de horário;
* Manter o cadastro de cursos;
  * um curso tem: código, nome, habilitação, turnos, modalidade;
* Manter Organização Curricular:
* uma organização curricular tem id_curriculo_componente;
* estrutura curricular;
* componente curricular;
* semestre
* tipo_vinculo
* nível

* Manter cadastro de Enquete:
  * Uma enquete tem: nome, descrição, o número de votos, a data e a hora de inicio e fim, o curso

## Modelo Conceitual

Abaixo apresentamos o modelo ER inicial.

 ![Modelo ER](https://github.com/labens-ufrn/suggestclasses/blob/master/docs/modelos/Modelo%20ER%20-%20SuggestClasses.png)

Também criamos alguns modelos usando [YUML](http://yuml.me):

Os Modelos UML pode ser encontrado na página [Modelos UML](modelos/ModelosUML.md).
