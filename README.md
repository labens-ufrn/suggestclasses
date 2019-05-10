# SuggestClasses by LABENS
Sistema de Sugestão de Horários para o BSI/UFRN.

## Testes

Rodar os testes mantendo o banco de testes:

```
python manage.py test --keepdb core/
```

### Configurações

```
pip install nose
pip install coverage
export DJANGO_SETTINGS_MODULE=mysite.settings
```

Devemos acrescentar nas classes de testes: 

```
import django
django.setup()
```

### Testes de Unidade e Cobertura

```
nosetests --with-xunit 
nosetests --with-coverage --cover-package=core --cover-branches --cover-xml
```

### Sonar

```
sonar-scanner \
  -Dsonar.projectKey=suggestclasses \
  -Dsonar.organization=labens-github \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=02254c57898053f6e25acfb70756ef6f840d4d35
```

### Links

* http://craigthomas.ca/blog/2014/06/02/python-code-inspection-with-sonarqube/
* https://docs.sonarqube.org/display/PLUG/Python+Unit+Tests+Execution+Reports+Import
* https://stackoverflow.com/questions/34114427/django-upgrading-to-1-9-error-appregistrynotready-apps-arent-loaded-yet