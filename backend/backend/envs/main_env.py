import environ
from typing import Any


class MainEnv:

    DEBUG: bool
    SECRET_KEY: str
    DATABASE_URL: Any
    ALLOWED_HOSTS: list

    def __init__(self) -> None:
        self.__env = environ.Env(
            DEBUG=(bool, True),
            SECRET_KEY=(
                str, 'django-insecure-jizyjlj_lvn@%m+g43c(s2$7*%4h0kqslhw85zcs#^jgsqjp36'),
            DATABASE_URL=(str, 'sqlite:///db.sqlite3'),
            ALLOWED_HOSTS=(list, ['*'])
        )
        environ.Env.read_env()
        self.DEBUG = self.__env('DEBUG')
        self.SECRET_KEY = self.__env('SECRET_KEY')
        self.DATABASE_URL = self.__env.db()
        self.ALLOWED_HOSTS = self.__env.list('ALLOWED_HOSTS')