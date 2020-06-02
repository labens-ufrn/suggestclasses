# Python Django Tutorial: Deploying Your Application

Tutorial de deploy de aplicação django em servidor web linux.

Baseado no vídeo: https://www.youtube.com/watch?v=Sa_kQheCnds&t=3652s

Colocar o passo a passo abaixo:

## Passo 1:

Configuração das pastas de arquivos estáticos:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# User_Uploaded_Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Copiar os arquivos estáticos para a pasta `STATIC_ROOT`:

```shell script
python manage.py collectstatic
```

## Passo 2:

## Passo 3:

## Passo 4:
