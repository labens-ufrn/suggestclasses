 ![GitHub](https://github.com/labens-ufrn/suggestclasses/workflows/Python%20application/badge.svg)
 ![GitHub](https://img.shields.io/github/license/labens-ufrn/suggestclasses)
 ![GitHub top language](https://img.shields.io/github/languages/top/labens-ufrn/suggestclasses)
 ![GitHub All Releases](https://img.shields.io/github/downloads/labens-ufrn/suggestclasses/total)
 [![GitHub forks](https://img.shields.io/github/forks/labens-ufrn/suggestclasses)](https://github.com/labens-ufrn/suggestclasses/network)
 [![GitHub stars](https://img.shields.io/github/stars/labens-ufrn/suggestclasses)](https://github.com/labens-ufrn/suggestclasses/stargazers)
 ![GitHub issues](https://img.shields.io/github/issues/labens-ufrn/suggestclasses)
 [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Flabens-ufrn%2Fsuggestclasses)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Flabens-ufrn%2Fsuggestclasses)


# SuggestClasses by LABENS/UFRN
Sistema de Sugestão de Horários para o BSI/UFRN.

## Lista de Requisitos Funcionais

O sistema SuggestClasses terá o cadastro de sugestões de horários para turmas de componentes curriculares de um curso em um certo período. Também manterá o horário aprovado das turmas e exibirá relatórios de horários para professores, alunos, por sala e por período.

Os requisitos funcionais detalhados estão na página wiki [Requisitos Funcionais](https://github.com/labens-ufrn/suggestclasses/wiki).

Na página [Documentação](docs/docs.md) temos os detalhes do projeto e a lista de documentos.

## Migrations

Ao modificar os models (em models.py), execute:

```shell script
$ python manage.py makemigrations core
$ python manage.py migrate
```

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

Configurações para os testes:

```shell script
pip install nose
pip install coverage
export DJANGO_SETTINGS_MODULE=mysite.settings
```

### Executar os Testes de Unidade e Cobertura

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

## Arquivo .env com a SECRET_KEY

Here's one way to do it that is compatible with deployment on Heroku:
Create a gitignored file named .env containing:

```shell script
    export DJANGO_SECRET_KEY='replace-this-with-the-secret-key'
```

Then edit settings.py to remove the actual SECRET_KEY and add this instead:

```shell script
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```

Then when you want to run the development server locally, use:

```shell script
    source .env
    python manage.py runserver
```

When you finally deploy to Heroku, go to your app Settings tab and add DJANGO_SECRET_KEY to the Config Vars.



# Outras Configurações

* Arquivo _.editorconfig_ de estilo de codificação adicionado.

##  Tabela com horários de aula

Matutino | Vespertino | Noturno
-------- | ---------- | -------
M1 – 07h00 às 07h50 | T1 – 13h00 às 13h50 | N1 – 18h45 às 19h35
M2 – 07h50 às 08h40 | T2 – 13h50 às 14h40 | N2 – 19h35 às 20h25
M3 – 08h55 às 09h45 | T3 – 14h55 às 15h45 | N3 – 20h35 às 21h25
M4 – 09h45 às 10h35 | T4 – 15h45 às 16h35 | N4 – 21h25 às 22h15
M5 – 10h50 às 11h40 | T5 – 16h50 às 17h40 |
M6 – 11h40 às 12h30 | T6 – 17h40 às 18h30 |

# Links

* https://www.techiediaries.com/django/django-3-tutorial-and-crud-example-with-mysql-and-bootstrap/
* https://learndjango.com/tutorials/django-favicon-tutorial
* https://automationpanda.com/2017/09/14/django-projects-in-pycharm-community-edition/
* http://craigthomas.ca/blog/2014/06/02/python-code-inspection-with-sonarqube/
* https://docs.sonarqube.org/display/PLUG/Python+Unit+Tests+Execution+Reports+Import
* https://stackoverflow.com/questions/34114427/django-upgrading-to-1-9-error-appregistrynotready-apps-arent-loaded-yet
* https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
* https://stackoverflow.com/questions/32612690/bootstrap-4-glyphicons-migration
* https://engineering.contaazul.com/versionamento-de-software-na-era-%C3%A1gil-8b53f6c08192
* https://studygyaan.com/django/how-to-use-message-framework-django-templates
* https://realpython.com/django-redirects/
* https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail
* https://casesup.com/category/knowledgebase/howtos/python-django-handling-custom-error-page
* https://coderbook.com/@marcus/how-to-restrict-access-with-django-permissions/
* https://www.agiliq.com/blog/2018/05/django-unit-testing/
* https://coderbook.com/@marcus/how-to-change-name-of-django-application/
* https://stackoverflow.com/questions/16797623/how-do-i-rename-a-django-project-in-pycharm
* https://django-project-skeleton.readthedocs.io/en/latest/structure.html
* https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request/35796330
* https://github.com/hjwp/Test-Driven-Django-Tutorial
* https://material.io/resources/icons/?style=baseline
* https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
