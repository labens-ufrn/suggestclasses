# Python Django Tutorial: Deploying Your Application

Tutorial de Deploy da Aplicação Django em Servidor Apache2 no Ubuntu.

Baseado no vídeo: https://www.youtube.com/watch?v=Sa_kQheCnds&t=3652s

## Passo 1: Copiar Arquivos Estáticos

Configuração das pastas de arquivos estáticos:

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# User_Uploaded_Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Copiar os arquivos estáticos para a pasta `STATIC_ROOT`:

```commandline
python manage.py collectstatic
```

## Passo 2: Módulo WSGI no Apache2

Instalar Apache2 se necessário.

```commandline
sudo apt install apache2
```

Instalar Módulo do WSGI para Python 3.

```commandline
sudo apt install libapache2-mod-wsgi-py3
```

## Passo 3: Configuração do Virtual Host no Apache

```commandline
cd /etc/apache2/sites-available/
sudo cp 000-default.conf suggestclasses.conf
```

Edite o arquivo suggestclasses.conf [Arquivo completo aqui](suggestclasses.conf) e
acrescente no final do arquivo dentro da tag `<VirtualHost *:80>`.

```xml
    Alias /static /home/taciano/dev/workspace/suggestclasses/static
	<Directory /home/taciano/dev/workspace/suggestclasses/static>
		Require all granted
	</Directory>

	Alias /media /home/taciano/dev/workspace/suggestclasses/media
	<Directory /home/taciano/dev/workspace/suggestclasses/media>
		Require all granted
	</Directory>

	<Directory /home/taciano/dev/workspace/suggestclasses/mysite>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	WSGIScriptAlias / /home/taciano/dev/workspace/suggestclasses/mysite/wsgi.py
	WSGIDaemonProcess sc_app python-path=/home/taciano/dev/workspace/suggestclasses:/home/taciano/dev/python/envP38/lib/python3.8/site-packages python-home=/home/taciano/dev/python/envP38
	WSGIProcessGroup sc_app
```

```commandline
sudo a2ensite suggestclasses
sudo a2dissite 000-default.conf
```

## Passo 4: Adicionando Permissões nos arquivos do projeto

Devemos adicionar permissões em arquivos que o sistema vai manipular.
No nosso caso, não temos o **db.sqlite3**, mas isso deve ser feito em arquivos manipulados.

```commandline
sudo chown :www-data suggestclasses/db.sqlite3
sudo chmod 664 suggestclasses/db.sqlite3
sudo chown :www-data suggestclasses/
sudo chmod 775 suggestclasses/

sudo chown -R :www-data suggestclasses/media/
sudo chmod -R 775 suggestclasses/media
sudo chown :www-data suggestclasses/static/
```

## Passo 5: Permissões no Firewall do Servidor

```commandline
sudo ufw allow http/tcp
sudo ufw allow 80
```

## Passo 6: Restart Apache Server

```commandline
sudo service apache2 restart
```
