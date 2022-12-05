# Plano de Teste

## **SuggestClasses**

*versão 1.2*

## Histórico das alterações

   Data    | Versão |    Descrição   | Autor(a)
-----------|--------|----------------|-----------------
01/10/2022 |  1.1   | Release inicial | Gabriel Azevedo 
05/12/2022 |  1.2   | Adição do teste de aceitação | Wanessa Bezerra
 
## 1 - Introdução

Este documento descreve os requisitos a testar, os  tipos de testes definidos para cada iteração, os recursos de hardware e software a serem empregados e o cronograma dos testes ao longo do projeto. As seções referentes aos requisitos, recursos e cronograma servem para permitir ao gerente do projeto acompanhar a evolução dos testes.

Com esse documento, você deve:
- Identificar informações de projeto existentes e os componentes de software que devem ser testados.
- Listar os Requisitos a testar.
- Recomendar e descrever as estratégias de teste a serem empregadas.
- Identificar os recursos necessários e prover uma estimativa dos esforços de teste.
- Listar os elementos resultantes do projeto de testes.

## 2 - Requisitos a Testar

Esta seção contém os casos de uso identificados como objetos dos testes ao longo do desenvolvimento do projeto de testes durante a disciplina de teste de software.
O conjunto de requisitos a serem testados no projeto de testes são: testar segurança, controle de acesso, funcionalidades. Os módulos a serem testados durante o projeto de testes são os módulos de turmas, sugestão de turmas e enquetes. 

### Casos de uso:

Identificador do caso de uso | Nome do caso de uso
-----------------------------|---------------------
US00                       |       Manter cadastro de sugestão de turma
US01                       |       Manter cadastro de enquentes  

## US00
Testar os métodos de manter cadastro de sugestão de turmas. Testar as turmas sugeridas pelos docentes, além de verificar se as turmas possuem choques de horário e ser exibido ao usuário aluno uma mensagem informando o choque de horário. Testar a segurança de cadastro de sugestão de turmas uma vez que apenas o usuário administrador e os docentes poderão realizar as operações de adicionar, alterar, remover e listar as sugestões de turmas cadastradas.

## US01
Testar os métodos de manter cadastro de enquentes no sistema. Para cadastrar uma enquete, deverá ter uma função de teste para verificar e validar se a enquete contém os atributos de: nome, descrição, número de votos, data de início e fim, hora de início e fim, curso, quantidade de discentes ativos, período, status, tipo, usuário e a data de criação. Apenas o usuário administrador do sistema e o usuário docente poderão realizar as operações de adicionar, alterar, remover e listar as enquetes cadastradas.


## 3 - Tipos de teste

Esta seção deve contém os tipos de testes escolhidos para cada iteração do projeto. Para a primeira rodada de testes serão realizados os testes de unidade no sistema, e na próxima iteração os testes de integração do sistema.
Para testar os requisitos de testes de projeto, os testes de unidade se mostram a melhor escolha, ao passo que deve ser verificado várias unidades independentes que compõem os cadastros que serão testados nessa iteração.


### Métodos da Classe 

Para teste de unidades do sistema, deve-se verificar se cada classe retorna o esperado.

<br/>
<table>
    <tr>
        <th>
            Objetivo
        </th>
        <th colspan="4">
            Testar manter cadastro de turmas
        </th>
    </tr>
    <tr>
        <th>
            Técnica:
        </th>
        <th colspan="2">
            ( ) manual
        </th>
        <th colspan="2">
            (x) automática
        </th>
    </tr>
    <tr>
        <th>
            Estágio do teste
        </th>
        <th>
            Integração ( )
        </th>
        <th>
            Sistema ( )
        </th>
        <th>
            Unidade (x)
        </th>
        <th>
            Aceitação ( )
        </th>
    </tr>
    <tr>
        <th>
            Abordagem do teste
        </th>
        <th colspan="2">
            Caixa branca (x)
        </th>
        <th colspan="2">
            Caixa preta (x)
        </th>
    </tr>
    <tr>
        <th>
            Responsável(is)
        </th>
        <th colspan="4">
            Programador(es) ou equipe de testes
        </th>
    </tr>
</table>
<br/>

<br/>
<table>
    <tr>
        <th>
            Objetivo
        </th>
        <th colspan="4">
            Testar o manter cadastro de sugestão de turmas
        </th>
    </tr>
    <tr>
        <th>
            Técnica:
        </th>
        <th colspan="2">
            (x) manual
        </th>
        <th colspan="2">
            (x) automática
        </th>
    </tr>
    <tr>
        <th>
            Estágio do teste
        </th>
        <th>
            Integração ( )
        </th>
        <th>
            Sistema ( )
        </th>
        <th>
            Unidade (x)
        </th>
        <th>
            Aceitação ( )
        </th>
    </tr>
    <tr>
        <th>
            Abordagem do teste
        </th>
        <th colspan="2">
            Caixa branca (x)
        </th>
        <th colspan="2">
            Caixa preta (x)
        </th>
    </tr>
    <tr>
        <th>
            Responsável(is)
        </th>
        <th colspan="4">
            Programador(es) ou equipe de testes
        </th>
    </tr>
</table>
<br/>

<br/>
<table>
    <tr>
        <th>
            Objetivo
        </th>
        <th colspan="4">
            Testar o manter cadastro de enquetes
        </th>
    </tr>
    <tr>
        <th>
            Técnica:
        </th>
        <th colspan="2">
            ( ) manual
        </th>
        <th colspan="2">
            (x) automática
        </th>
    </tr>
    <tr>
        <th>
            Estágio do teste
        </th>
        <th>
            Integração ( )
        </th>
        <th>
            Sistema ( )
        </th>
        <th>
            Unidade (x)
        </th>
        <th>
            Aceitação ( )
        </th>
    </tr>
    <tr>
        <th>
            Abordagem do teste
        </th>
        <th colspan="2">
            Caixa branca (x)
        </th>
        <th colspan="2">
            Caixa preta (x)
        </th>
    </tr>
    <tr>
        <th>
            Responsável(is)
        </th>
        <th colspan="4">
            Programador(es) ou equipe de testes
        </th>
    </tr>
</table>
<br/>

## 4 - Recursos

Esta seção apresenta os recursos recomendados para realizar os testes do sistema, desde os recursos humanos, de ambiente de teste (hardware e software) e de ferramentas de automatização de testes necessários para execução dos testes.

### 4.1 - Recursos humanos

   Função           | Recursos mínimos recomendados |    Responsabilidades  
--------------------|-------------------------------|-----------------------
Gerente de testes   | Wanessa Bezerra               | Fornece supervisão de gerenciamento
Testador do sistema | Renata Karla                  | Executa os testes 
Implementador       | Gabriel Azevedo               | Implementa e faz o teste de unidade das classes de teste e pacotes de teste


### 4.2 - Ambiente de teste - Software e Hardware


Para realização dos testes, não necessita de um hardware extremamente potente. Um computador ou notebook com processador dual core, core i3, 4GB de ram (mínimo) e HD já consegue rodar o ambiente.
Com relação aos softwares, é necessário um browser já que o sistema está na web, um editor de código para escrever os testes, e sistema operacional Windows, Linux ou Mac.

### 4.3 - Ferramenta de teste

A ferramenta de teste utilizada é a ferramenta de testes nativa da linguagem Python, a biblioteca Unittest. A biblioteca já vem junto a liguagem, sem a necessidade de nenhuma instação posterior.


## 5 - Cronograma

Tipo de teste      | Duração | data de início | data de término
-------------------|---------|----------------|-----------------
planejar teste     |   10h   | 01/10/2022     | 03/10/2022
projetar teste     |         | dd/mm/aaaa     | dd/mm/aaaa
implementar teste  |         | dd/mm/aaaa     | dd/mm/aaaa
executar teste     |         | dd/mm/aaaa     | dd/mm/aaaa
avaliar teste      |         | dd/mm/aaaa     | dd/mm/aaaa
