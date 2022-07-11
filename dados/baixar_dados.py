#!/usr/bin/python
import os
import urllib.request
import django
django.setup()

from suggestclasses.settings import BASE_DIR

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


def download_departamentos():
    print("Download do CSV dos Departamentos do CERES/UFRN ...!")
    file_name = 'csv/unidades.csv'
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/da6451a5-1a59-4630-bdc2-97f6be4a59c2/resource/3f2e4e32-ef1a-4396-8037' \
          '-cbc22a89d97f/download/unidades.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_cursos():
    print("Download do CSV dos Cursos do CERES/UFRN ...!")
    file_name = 'csv/cursos-ufrn.csv'
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/08b0dc59-faa9-4281-bd1e-2a39f532489e/resource/949be3d1-e85b-4d0f-9f60' \
          '-1d9a7484bb06/download/cursos-ufrn.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_componentes():
    print("Download do CSV dos Componentes do CERES/UFRN ...!")
    file_name = 'csv/componentes-curriculares-presenciais.csv'
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/3fea67e8-6916-4ed0-aaa6-9a8ca06a9bdc/resource/9a3521d2-4bc5-4fda-93f0' \
          '-f701c8a20727/download/componentes-curriculares-presenciais.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_estruturas():
    print("Download do CSV das Estruturas Curriculares do CERES/UFRN ...!")
    file_name = 'csv/estruturas-curriculares.csv'
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/e7c24910-75c1-451b-9097-e4352488dd69/resource/94cc35b0-6560-44f3-8c67' \
              '-98cff965f23c/download/estruturas-curriculares.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_curriculos():
    print("Download do CSV dos Organização Curricular do CERES/UFRN ...!")
    file_name = 'csv/curriculo-componente-graduacao.csv'
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/82aca3f1-f7ee-425e-bf1e-b6a1d6811bf4/resource/3f25d054-c5d2-4bf2-8cd4' \
          '-8e0a2e4f63ce/download/curriculo-componente-graduacao.csv '
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_turmas():
    print("Download do CSV das Turmas 2019.1 do CERES/UFRN ...!")
    file_name = "csv/turmas-2019.1.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/1e42cd66-69d6-48d5-a346' \
          '-d46766fd2c9c/download/turmas-2019.1.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

    print("Download do CSV das Turmas 2019.2 do CERES/UFRN ...!")
    file_name = "csv/turmas-2019.2.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/d9c2863e-d1b2-4afd-b7dd' \
          '-09517d5ed17d/download/turmas-2019.2.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

    print("Download do CSV das Turmas 2020.1 do CERES/UFRN ...!")
    file_name = "csv/turmas-2020.1.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/3a9fe77e-478d-4b18-b7bc' \
              '-a4df57cbdf46/download/turmas-2020.1.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

    print("Download do CSV das Turmas 2020.5 do CERES/UFRN ...!")
    file_name = "csv/turmas-2020.5.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/eba5c0bb-5199-469b-acbd' \
              '-d941d151c16f/download/turmas-2020.5.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

    print("Download do CSV das Turmas 2020.6 do CERES/UFRN ...!")
    file_name = "csv/turmas-2020.6.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/964f91df-f322-4e56-897b' \
              '-f06cca611904/download/turmas-2020.6.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

    print("Download do CSV das Turmas 2021.1 do CERES/UFRN ...!")
    file_name = "csv/turmas-2021.1.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/964f91df-f322-4e56-897b' \
              '-f06cca611904/download/turmas-2021.1.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

        print("Download do CSV das Turmas 2021.2 do CERES/UFRN ...!")
    file_name = "csv/turmas-2021.2.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/964f91df-f322-4e56-897b' \
              '-f06cca611904/download/turmas-2021.2.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

        print("Download do CSV das Turmas 2022.1 do CERES/UFRN ...!")
    file_name = "csv/turmas-2022.1.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/964f91df-f322-4e56-897b' \
              '-f06cca611904/download/turmas-2022.1.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')

def download_docentes():
    print("Download do CSV dos Docentes do CERES/UFRN ...!")
    file_name = "csv/docentes.csv"
    if os.path.exists(file_name):
        print("Arquivo " + file_name + " já existe!")
    else:
        url = 'https://dados.ufrn.br/dataset/8bf1a468-48ff-4f4d-95ee-b17b7a3a5592/resource/6a8e5461-e748-45c6-aac6' \
            '-432188d88dde/download/docentes.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_funcoes():
    print("Download do CSV das Funções Gratificadas do CERES/UFRN ...!")
    file_name = "csv/funcoes-gratificadas.csv"
    if os.path.exists(file_name):
        print('Arquivo ' + file_name + ' já existe!')
    else:
        url = 'http://dados.ufrn.br/dataset/b8c62810-0ec4-4412-ad3b-52105dc8b391/resource/f9ac99fa-011e-4403-8b2a' \
              '-c8d75888cbcf/download/funcoes-gratificadas.csv'
        urllib.request.urlretrieve(url, file_name)
        print('.................')


def download_discentes():
    print("Download do CSV dos Discentes da UFRN ...!")

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/861b96a8-5304-4e6a-a8c4' \
          '-068533ec7cb9/download/discentes-2009.csv'
    download_discentes_semestre(url, 'csv/discentes-2009.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/5fc61f78-19b4-4020-9f3c' \
          '-c298cb8a63aa/download/discentes-2010.csv'
    download_discentes_semestre(url, 'csv/discentes-2010.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/2bb3dec9-7f23-434c-a179' \
          '-21515f91abc8/download/discentes-2011.csv'
    download_discentes_semestre(url, 'csv/discentes-2011.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/fc283aa9-61a7-4cf0-91fb' \
          '-c403c0817b48/download/discentes-2012.csv'
    download_discentes_semestre(url, 'csv/discentes-2012.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/dba208c2-822f-4e26-adc3' \
          '-b61d4cb110b6/download/discentes-2013.csv'
    download_discentes_semestre(url, 'csv/discentes-2013.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/6c23a430-9a7c-4d0f-9602' \
          '-1d5d97d40e6a/download/discentes-2014.csv'
    download_discentes_semestre(url, 'csv/discentes-2014.csv')
    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/e2b5b843-4f58-497e-8979' \
          '-44daf8df8f94/download/discentes-2015.csv'
    download_discentes_semestre(url, 'csv/discentes-2015.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/7d2fa5b3-743f-465f-8450' \
          '-91719b34a002/download/discentes-2016.csv'
    download_discentes_semestre(url, 'csv/discentes-2016.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/dc732572-a51a-4d4a-a39d' \
          '-2db37cbe5382/download/discentes-2017.csv'
    download_discentes_semestre(url, 'csv/discentes-2017.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/146b749b-b9d0-49b2-b114' \
          '-ac6cc82a4051/download/discentes-2018.csv'
    download_discentes_semestre(url, 'csv/discentes-2018.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/a55aef81-e094-4267-8643' \
          '-f283524e3dd7/download/discentes-2019.csv'
    download_discentes_semestre(url, 'csv/discentes-2019.csv')

    url = 'http://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/7795c538-86fc-483f-9da9' \
          '-67b2fcc834ae/download/discentes-2020.csv'
    download_discentes_semestre(url, 'csv/discentes-2020.csv')

    url = 'https://dados.ufrn.br/dataset/554c2d41-cfce-4278-93c6-eb9aa49c5d16/resource/ac2acdb3-02c0-4334-9865' \
          '-d384eb2de3b6/download/discentes-2021.csv'
    download_discentes_semestre(url, 'csv/discentes-2021.csv')


def download_discentes_semestre(url, discentes_csv):
    file_name = discentes_csv
    if os.path.exists(file_name):
        print('Arquivo ' + discentes_csv + ' já existe!')
    else:
        urllib.request.urlretrieve(url, file_name)
        print('........' + discentes_csv + '.........')


if __name__ == "__main__":
    main()
