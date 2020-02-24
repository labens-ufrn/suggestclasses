import os
import urllib.request


def main():
    print("Download dados sobre o CERES/UFRN ...!")
    print(os.getcwd())


def downloads_dados():
    """Download de arquivos CSV de http://dados.ufrn.br"""

    print("Download dados sobre o CERES/UFRN ...!")
    #download_departamentos()
    #download_cursos()
    download_componentes()
    download_estruturas()
    #download_curriculos()
    download_docentes()
    #download_turmas()


def download_departamentos():
    print("Download do CSV dos Departamentos do CERES/UFRN ...!")
    url = 'http://dados.ufrn.br/dataset/da6451a5-1a59-4630-bdc2-97f6be4a59c2/resource/3f2e4e32-ef1a-4396-8037' \
          '-cbc22a89d97f/download/unidades.csv'
    file_name = 'unidades.csv'
    urllib.request.urlretrieve(url, file_name)


def download_cursos():
    print("Download do CSV dos Cursos do CERES/UFRN ...!")
    url = 'http://dados.ufrn.br/dataset/08b0dc59-faa9-4281-bd1e-2a39f532489e/resource/949be3d1-e85b-4d0f-9f60' \
          '-1d9a7484bb06/download/cursos-ufrn.csv'
    file_name = 'cursos-ufrn.csv'
    urllib.request.urlretrieve(url, file_name)


def download_componentes():
    print("Download do CSV dos Componentes do CERES/UFRN ...!")
    file_name = 'componentes-curriculares-presenciais.csv'
    if os.path.exists(file_name):
        print("Arquivo componentes-curriculares-presenciais.csv já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/3fea67e8-6916-4ed0-aaa6-9a8ca06a9bdc/resource/9a3521d2-4bc5-4fda-93f0' \
          '-f701c8a20727/download/componentes-curriculares-presenciais.csv'
        urllib.request.urlretrieve(url, file_name)


def download_estruturas():
    print("Download do CSV das Estruturas Curriculares do CERES/UFRN ...!")
    file_name = 'estruturas-curriculares.csv'
    if os.path.exists(file_name):
        print("Arquivo estruturas-curriculares.csv já existe!")
    else:
        url = 'http://dados.ufrn.br/dataset/e7c24910-75c1-451b-9097-e4352488dd69/resource/94cc35b0-6560-44f3-8c67' \
              '-98cff965f23c/download/estruturas-curriculares.csv'
        urllib.request.urlretrieve(url, file_name)


def download_curriculos():
    print("Download do CSV dos Organização Curricular do CERES/UFRN ...!")
    url = 'http://dados.ufrn.br/dataset/82aca3f1-f7ee-425e-bf1e-b6a1d6811bf4/resource/3f25d054-c5d2-4bf2-8cd4' \
          '-8e0a2e4f63ce/download/curriculo-componente-graduacao.csv '
    file_name = 'curriculo-componente-graduacao.csv'
    urllib.request.urlretrieve(url, file_name)


def download_turmas():
    print("Download do CSV das Turmas 2019.1 do CERES/UFRN ...!")
    url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/1e42cd66-69d6-48d5-a346' \
          '-d46766fd2c9c/download/turmas-2019.1.csv'
    file_name = "turmas-2019.1.csv"
    urllib.request.urlretrieve(url, file_name)

    print("Download do CSV das Turmas 2019.2 do CERES/UFRN ...!")
    url = 'http://dados.ufrn.br/dataset/1938623d-fb07-41a4-a55a-1691f7c3b8b5/resource/d9c2863e-d1b2-4afd-b7dd' \
          '-09517d5ed17d/download/turmas-2019.2.csv'
    file_name = "turmas-2019.2.csv"
    urllib.request.urlretrieve(url, file_name)


def download_docentes():
    file_name = "docentes.csv"
    if os.path.exists(file_name):
        print("Arquivo docentes.csv já existe!")
    else:
        print("Download do CSV dos Docentes do CERES/UFRN ...!")
        url = 'http://dados.ufrn.br/dataset/8bf1a468-48ff-4f4d-95ee-b17b7a3a5592/resource/ff0a457e-76fa-4aca-ad99' \
              '-48aebd7db070/download/docentes.csv'
        urllib.request.urlretrieve(url, file_name)


if __name__ == "__main__":
    main()
