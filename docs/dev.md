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
