# Base Image
FROM python:3.11-slim

LABEL description="SuggestClasses - Sistema de Sugest\u00E3o de Turmas"
LABEL maintainer="labens.dct.ufrn.br"

# Define o diretório de trabalho no contêiner
WORKDIR /code

# Cria um usuário não-root e adiciona permissões para acessar a pasta /code
RUN adduser --disabled-password appuser && chown -R appuser /code

# Altera para o usuário não-root
USER appuser

# Define a variável de ambiente PYTHONPATH
ENV PYTHONPATH=/code

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta que será usada para acessar a aplicação (altere conforme necessário)
EXPOSE 8003


