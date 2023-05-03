# MariaDB

Aqui você pode encontrar a configuração do MariaDB ou MySQL.

## Criação do Banco de Dados (dev e test) e Usuário

Utilzamos o SGBD MariaDB/MySql.

```sql
CREATE DATABASE scdb_dev character set UTF8 collate utf8_bin;
CREATE DATABASE scdb_test character set UTF8 collate utf8_bin;
CREATE USER 'sc_user'@'%' IDENTIFIED BY 'password';
GRANT ALL ON scdb_dev.* TO 'sc_user'@'%';
GRANT ALL ON scdb_test.* TO 'sc_user'@'%';
```

### Dependências para usar o MariaDB e MySQL

Windows

No site <https://www.lfd.uci.edu/~gohlke/pythonlibs/> busca o Mysqlclient compatível com a sua versão Python instalada.

Instalação com o PIP:

```shell script
pip install nome_do_arquivo_baixado.whl
```

Linux

```shell script
sudo apt install python3-dev default-libmysqlclient-dev
```

## Virtualenv e variáveis de ambiente

Adicionar em ~/.profile as variáveis de ambiente:

```shell script
MARIA_HOME=/usr/bin/mysql
PATH=$PATH:$MARIA_HOME/bin
PYTHONHOME=/usr/bin
```

Windows

Caso não tenha a Virtualenv instalada:

```shell script
pip install virtualenv
```

Criação do Ambiente Virtual com virtualenv:

```shell script
virtualenv nome_da_virtualenv
```

Para ativar: ```cd nome_da_virtualenv\Scripts\activate```.
Para desativar: ```cd nome_da_virtualenv\Scripts\deactivate```.

Linux

Criação do Ambiente Virtual com virtualenv:

```shell script
virtualenv -p python3 venv
```

Para ativar: ```source venv/bin/activate```.
Para desativar: ```deactivate```.
