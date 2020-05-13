#!/usr/bin/python
import os
import urllib.request
import django
import requests
from tqdm import tqdm
django.setup()

from mysite.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')


def main():
    print("Download dados sobre o CERES/UFRN ...!")
    print('>> Salvando dados em: ' + os.path.join(BASE_DIR, 'dados'))
    os.chdir(DADOS_PATH)
    downloads_dados()


def downloads_dados():
    """Download de arquivos CSV de http://dados.ufrn.br"""

    print("Download dados sobre o CERES/UFRN ...!")
    download_departamentos()
    download_cursos()
    download_componentes()
    download_estruturas()
    download_curriculos()
    download_docentes()
    download_turmas()
    download_funcoes()
    download_discentes()

#Função progressbar para os downloads
def progress(url, file_name):
    chunk_size = 1024
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get("content-Length", 0))
    progress = tqdm(r.iter_content(chunk_size=chunk_size),
                    total=total_size/chunk_size,
                     unit='KB'
                    )
    with open(file_name, 'wb') as f:
        for data in progress:
            f.write(data)


def download_departamentos():
    print("Download do CSV dos Departamentos do CERES/UFRN ...!")
    file_name = 'unidades.csv'
    url = 'http://dados.ufrn.br/dataset/da6451a5-1a59-4630-bdc2-97f6be4a59c2/resource/3f2e4e32-ef1a-4396-8037' \
          '-cbc22a89d97f/download/unidades.csv'
    if os.path.exists(file_name):
        print("Arquivo → unidades.csv já existe!")
    else:
        progress(url,file_name)
        print("Download completo!")
        print('.................')


def download_cursos():
    print("Download do CSV dos Cursos do CERES/UFRN ...!")
    file_name = 'cursos-ufrn.csv'
    url = 'http://dados.ufrn.br/dataset/08b0dc59-faa9-4281-bd1e-2a39f532489e/resource/949be3d1-e85b-4d0f-9f60' \
          '-1d9a7484bb06/download/cursos-ufrn.csv'
    if os.path.exists(file_name):
        print("Arquivo cursos-ufrn.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_componentes():
    print("Download do CSV dos Componentes do CERES/UFRN ...!")
    file_name = 'componentes-curriculares-presenciais.csv'
    url = 'http://dados.ufrn.br/dataset/3fea67e8-6916-4ed0-aaa6-9a8ca06a9bdc/resource/9a3521d2-4bc5-4fda-93f0' \
          '-f701c8a20727/download/componentes-curriculares-presenciais.csv'
    if os.path.exists(file_name):
        print("Arquivo componentes-curriculares-presenciais.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_estruturas():
    print("Download do CSV das Estruturas Curriculares do CERES/UFRN ...!")
    file_name = 'estruturas-curriculares.csv'
    url = 'http://dados.ufrn.br/dataset/e7c24910-75c1-451b-9097-e4352488dd69/resource/94cc35b0-6560-44f3-8c67' \
              '-98cff965f23c/download/estruturas-curriculares.csv'
    if os.path.exists(file_name):
        print("Arquivo estruturas-curriculares.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_curriculos():
    print("Download do CSV dos Organização Curricular do CERES/UFRN ...!")
    file_name = 'curriculo-componente-graduacao.csv'
    url = 'http://dados.ufrn.br/dataset/82aca3f1-f7ee-425e-bf1e-b6a1d6811bf4/resource/3f25d054-c5d2-4bf2-8cd4' \
          '-8e0a2e4f63ce/download/curriculo-componente-graduacao.csv '
    if os.path.exists(file_name):
        print("Arquivo curriculo-componente-graduacao.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_turmas():
    print("Download do CSV das Turmas 2019.1 do CERES/UFRN ...!")
    file_name = "turmas-2019.1.csv"
    url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/1e42cd66-69d6-48d5-a346' \
          '-d46766fd2c9c/download/turmas-2019.1.csv'
    if os.path.exists(file_name):
        print("Arquivo turmas-2019.1.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')

    print("Download do CSV das Turmas 2019.2 do CERES/UFRN ...!")
    file_name = "turmas-2019.2.csv"
    url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/d9c2863e-d1b2-4afd-b7dd' \
          '-09517d5ed17d/download/turmas-2019.2.csv'
    if os.path.exists(file_name):
        print("Arquivo turmas-2019.2.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')

    print("Download do CSV das Turmas 2020.1 do CERES/UFRN ...!")
    file_name = "turmas-2020.1.csv"
    url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/3a9fe77e-478d-4b18-b7bc' \
              '-a4df57cbdf46/download/turmas-2020.1.csv'
    if os.path.exists(file_name):
        print("Arquivo turmas-2020.1.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_docentes():
    print("Download do CSV dos Docentes do CERES/UFRN ...!")
    file_name = "docentes.csv"
    url = 'http://dados.ufrn.br/dataset/8bf1a468-48ff-4f4d-95ee-b17b7a3a5592/resource/ff0a457e-76fa-4aca-ad99' \
              '-48aebd7db070/download/docentes.csv'
    if os.path.exists(file_name):
        print("Arquivo docentes.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_funcoes():
    print("Download do CSV das Funções Gratificadas do CERES/UFRN ...!")
    file_name = "funcoes-gratificadas.csv"
    url = 'http://dados.ufrn.br/dataset/b8c62810-0ec4-4412-ad3b-52105dc8b391/resource/f9ac99fa-011e-4403-8b2a' \
              '-c8d75888cbcf/download/funcoes-gratificadas.csv'
    if os.path.exists(file_name):
        print("Arquivo funcoes-gratificadas.csv já existe!")
    else:
        progress(url,file_name)
        print('.................')


def download_discentes():
    print("Download do CSV dos Discentes da UFRN ...!")
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/5fc61f78-19b4-4020-9f3c' \
          '-c298cb8a63aa/download/discentes-2010.csv'
    download_discentes_semestre(url, 'discentes-2010.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/2bb3dec9-7f23-434c-a179' \
          '-21515f91abc8/download/discentes-2011.csv'
    download_discentes_semestre(url, 'discentes-2011.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/fc283aa9-61a7-4cf0-91fb' \
          '-c403c0817b48/download/discentes-2012.csv'
    download_discentes_semestre(url, 'discentes-2012.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/dba208c2-822f-4e26-adc3' \
          '-b61d4cb110b6/download/discentes-2013.csv'
    download_discentes_semestre(url, 'discentes-2013.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/6c23a430-9a7c-4d0f-9602' \
          '-1d5d97d40e6a/download/discentes-2014.csv'
    download_discentes_semestre(url, 'discentes-2014.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/e2b5b843-4f58-497e-8979' \
          '-44daf8df8f94/download/discentes-2015.csv'
    download_discentes_semestre(url, 'discentes-2015.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/7d2fa5b3-743f-465f-8450' \
          '-91719b34a002/download/discentes-2016.csv'
    download_discentes_semestre(url, 'discentes-2016.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/dc732572-a51a-4d4a-a39d' \
          '-2db37cbe5382/download/discentes-2017.csv'
    download_discentes_semestre(url, 'discentes-2017.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/146b749b-b9d0-49b2-b114' \
          '-ac6cc82a4051/download/discentes-2018.csv'
    download_discentes_semestre(url, 'discentes-2018.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/a55aef81-e094-4267-8643' \
          '-f283524e3dd7/download/discentes-2019.csv'
    download_discentes_semestre(url, 'discentes-2019.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/7795c538-86fc-483f-9da9' \
          '-67b2fcc834ae/download/discentes-2020.csv'
    download_discentes_semestre(url, 'discentes-2020.csv')


def download_discentes_semestre(url, discentes_csv):
    file_name = discentes_csv
    if os.path.exists(file_name):
        print('Arquivo ' + discentes_csv + ' já existe!')
    else:
        print('........' + discentes_csv + '.........')
        progress(url,file_name)
        print("Download Completo")

if __name__ == "__main__":
    main()
