# SuggestClasses by LABENS/UFRN

Sistema de Sugestão de Horários para o BSI/UFRN.

## Lista de Requisitos Funcionais

O sistema SuggestClasses terá o cadastro de sugestões de horários para turmas de componentes curriculares de um curso em um certo período. Também manterá o horário aprovado das turmas e exibirá relatórios de horários para professores, alunos, por sala e por período.

Os requisitos funcionais detalhados estão na página wiki [Requisitos Funcionais](https://github.com/labens-ufrn/suggestclasses/wiki).

Na página [Documentação](docs/docs.md) temos os detalhes do projeto e a lista de documentos.

## Pré-requisitos

O sistema atualmente utiliza o SGBD [PostgreSQL](https://www.postgresql.org/) para armazenar os dados, e é desenvolvido com o [Django]() framework e [Python 3](https://www.python.org). Utilizamos o [Docker](https://www.docker.com) e [docker-compose](https://docs.docker.com/compose/) para deploy e execução no servidor. Inicialmente o SGBD era o [MariaDB](https://mariadb.org) e sua configuração está [aqui!](docs/mariadb.md).

### Criação do Banco de Dados

Utilzamos o SGBD PostgreSQL para armazenar os dados. Você pode utilizar o **Docker** para executar o [PostgreSQL + pgAdmin](https://github.com/tacianosilva/bsi-tasks/tree/master/database/docker/postgres).

Crie o usuário de acesso ao banco de dados:

```sql
CREATE ROLE sc_user WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxx';
```

Crie os bancos de dados:
```sql
CREATE DATABASE scdb_dev
    WITH
    OWNER = sc_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'pt_BR.utf8'
    LC_CTYPE = 'pt_BR.utf8'
    TABLESPACE = pg_default
    TEMPLATE= template0
    CONNECTION LIMIT = -1;
```

Defina as permissions e privilégios do Usuário:
```sql
GRANT ALL PRIVILEGES ON DATABASE scdb_dev TO sc_user;
GRANT ALL ON SCHEMA public TO sc_user;
```

## Ambiente Virtual

Criação do Ambiente Virtual com [python3-venv](https://docs.python.org/pt-br/3/library/venv.html):

```console
python3 -m venv .venv
```

Para ativar: ```source venv/bin/activate```.
Para desativar: ```deactivate```.

Copie os exemplos destes arquivos no diretório raiz do projeto:

```console
cp .env.sample .env
cp path.env.sample path.env
```

Edite o arquivo `path.env` para informar as variáveis:
```console
export DJANGO_SETTINGS_MODULE=suggestclasses.settings
export PYTHONPATH=${PYTHONPATH}:/home/<seu_diretorio>/suggestclasses
```

Após editar os valores, execute os comandos:
```console
source .env
source path.env
```

### Execução do Projeto

Ative o ambiente virtual e instale as depedências.
```console
source .venv/bin/activate
pip install -r requirements.txt
```

Atualize os arquivos estáticos.
```console
python manage.py collectstatic
```

Se houver modificações nos models (em models.py), execute a criação das migrações. Depois execute as migrações.
```console
python3 manage.py makemigrations core
python3 manage.py migrate
```

Crie um super usuário de administração do Django.

```console
python manage.py createsuperuser
```

Execute o sistema.
```console
python manage.py runserver
```

Lembre-se: O SGBD deve estar em execução e configure o acesso no arquivo `.env`.

## Povoamento

O sistema é baseado nos dados abertos da UFRN, desta forma é necessário povoar o banco de dados
com informações de Horários, Centro, Salas, Departamentos, Componentes, etc.

Lembre-se de deixar todas as variáveis de ambiente definidas. Execute o comando `source path.env` no Linux ou `activate path.env` no Windows para carregar as variáveis.

A ordem é importante e deve ser seguida conforme descrito abaixo.

### Criar Grupos e Permissões

Deve-se rodar, na raiz do projeto, o script ```povoar_grupos.py``` na pasta **dados**.

```python dados/povoar_grupos.py```

### Criar base de horários da UFRN

Deve-se rodar, na raiz do projeto, o script ```povoar_horarios.py``` na pasta **dados**.

```python dados/povoar_horarios.py```

### Criar o restante da base de Dados

Os scripts seguintes farão o povoamento do restante da base.

```shell script
python dados/baixar_dados.py
python dados/povoar.py
python dados/povoar_organizacao_curricular.py
```

Para atualizar a base, devem-ser deletados os csv's antigos e executar novamente os scripts.

## Testes

Rodar os testes mantendo o banco de testes:

```shell script
python manage.py test --keepdb core/
```

Devemos acrescentar nas classes de testes:

```pythonstub
import django
django.setup()
```

Configurações executar os testes:

```shell script
export DJANGO_SETTINGS_MODULE=suggestclasses.settings
python manage.py test
```

### Executar os Testes de Unidade e Cobertura

#### Utilizando o Cobetura

Primeiro defina a varíavel de ambiente: ```export DJANGO_SETTINGS_MODULE=projectname.settings```.

Depois instale o **coverage** e rode para ele gerar o arquivo `coverage.xml`.

```pythonstub
pip install coverage
coverage run -m unittest discover
coverage xml
```

Se usar `coverage html`, ele gera o relatório em html.

#### Utilizando Nose (desativado)

```shell script
pip install nose
pip install coverage
export DJANGO_SETTINGS_MODULE=suggestclasses.settings
```

```shell script
nosetests --with-xunit
nosetests --with-coverage --cover-package=core --cover-branches --cover-xml
```

## Executar o Sonar

```shell script
sonar-scanner \
  -Dsonar.projectKey=suggestclasses \
  -Dsonar.organization=labens-github \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=02254c57898053f6e25acfb70756ef6f840d4d35
```

## Rodando o projeto usando Docker e Docker Compose

Tenha certeza que o Docker e o Docker Compose estão instalados em sua máquina. Caso contrário, [Instalando o Docker](https://docs.docker.com/get-docker/) e [Instalando Docker Compose](https://docs.docker.com/compose/install/).

Rode os seguintes comandos para criar as imagens.

```shell
docker build .
docker-compose build
```

Para rodar o projeto rode o seguinte comando.

```shell
docker-compose up
```

Se preferir iniciar apenas o container do mariadb para rodar o projeto do suggestclasses fora de um container, use o comando.

```shell
docker-compose up -d mariadb
```

Para desativar os containers, digite o seguinte comando.

```shell
docker-compose down
```

## Outras Configurações

* Arquivo _.editorconfig_ de estilo de codificação adicionado.

## Tabela com horários de aula

Matutino | Vespertino | Noturno
-------- | ---------- | -------
M1 – 07h00 às 07h50 | T1 – 13h00 às 13h50 | N1 – 18h45 às 19h35
M2 – 07h50 às 08h40 | T2 – 13h50 às 14h40 | N2 – 19h35 às 20h25
M3 – 08h55 às 09h45 | T3 – 14h55 às 15h45 | N3 – 20h35 às 21h25
M4 – 09h45 às 10h35 | T4 – 15h45 às 16h35 | N4 – 21h25 às 22h15
M5 – 10h50 às 11h40 | T5 – 16h50 às 17h40 |
M6 – 11h40 às 12h30 | T6 – 17h40 às 18h30 |

# Links

* <https://www.techiediaries.com/django/django-3-tutorial-and-crud-example-with-mysql-and-bootstrap/>
* <https://learndjango.com/tutorials/django-favicon-tutorial>
* <https://automationpanda.com/2017/09/14/django-projects-in-pycharm-community-edition/>
* <http://craigthomas.ca/blog/2014/06/02/python-code-inspection-with-sonarqube/>
* <https://docs.sonarqube.org/display/PLUG/Python+Unit+Tests+Execution+Reports+Import>
* <https://stackoverflow.com/questions/34114427/django-upgrading-to-1-9-error-appregistrynotready-apps-arent-loaded-yet>
* <https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html>
* <https://stackoverflow.com/questions/32612690/bootstrap-4-glyphicons-migration>
* <https://engineering.contaazul.com/versionamento-de-software-na-era-%C3%A1gil-8b53f6c08192>
* <https://studygyaan.com/django/how-to-use-message-framework-django-templates>
* <https://realpython.com/django-redirects/>
* <https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail>
* <https://casesup.com/category/knowledgebase/howtos/python-django-handling-custom-error-page>
* <https://coderbook.com/@marcus/how-to-restrict-access-with-django-permissions/>
* <https://www.agiliq.com/blog/2018/05/django-unit-testing/>
* <https://coderbook.com/@marcus/how-to-change-name-of-django-application/>
* <https://stackoverflow.com/questions/16797623/how-do-i-rename-a-django-project-in-pycharm>
* <https://django-project-skeleton.readthedocs.io/en/latest/structure.html>
* <https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request/35796330>
* <https://github.com/hjwp/Test-Driven-Django-Tutorial>
* <https://material.io/resources/icons/?style=baseline>
* <https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/>
* <https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs/30969768#30969768>
* <https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html>
* <https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html>
* <https://bootstrapious.com/p/bootstrap-sidebar>
* <https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html>
* https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html
