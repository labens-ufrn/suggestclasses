import configparser
import os

from mysite.settings import BASE_DIR

CONFIG_PATH = os.path.join(BASE_DIR, 'core/config/')


def get_config():
    config = configparser.RawConfigParser()
    config.read(CONFIG_PATH + 'suggestclasses.ini')
    return config


def main():
    print("Lendo dados sobre o CERES/UFRN ...!")
    print(os.getcwd())
    print(CONFIG_PATH)
    config = get_config()
    print(config.get('PeriodoAtual', 'periodo'))


if __name__ == "__main__":
    main()
