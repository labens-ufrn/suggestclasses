# Orientações para o Desenvolvimento

## Realizando o checkout de Pull Requests localmente

Baseado no [Artigo IMasters](https://imasters.com.br/devsecops/git-realizando-o-checkout-de-pull-requests-localmente)

```bash
git fetch origin pull/ID/head:NOMEBRANCH
git checkout NOMEBRANCH
```

* ID: ID do Pull Request;
* NOMEBRANCH: é um nome qualquer definido para a branch que será criada.

## Banco de Dados ignorando acentuação

Resposta do Stackoverflow [Aqui!](https://stackoverflow.com/questions/1452967/django-search-doesnt-bring-words-with-accents)

This is nothing to do with Django, but depends on the collation of your database tables.
The collation is what determines how to sort and compare characters, and you need to choose one that compares accented
and non-accented characters as equal. If you're using MySQL, a good collation would be utf8_general_ci.

## Django Secret Key Generator

* https://djecrety.ir/

## Configuração do Locale no seu container

0) Entre na linha de comando do container Postgres:
```console
docker exec -it postgres-server bash
```
1) Identificando Locales instalados
```console
locale -a
```
2) Instalando novo Locale
```console
ls /usr/share/i18n/locales
localedef -i pt_BR -f UTF-8 pt_BR.UTF-8
```
3) Configurando Locale padrão
```console
sudo localectl set-locale LANG=pt_BR.UTF-8
```
Uma alternativa ao comando anterior é inserir manualmente o Locale no arquivo /etc/locale.conf adicionando a seguinte diretiva ao arquivo:
```console
    LANG=pt_BR.UTF-8
```

