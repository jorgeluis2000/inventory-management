import dj_database_url
from decouple import config
from typing import Any


class MainEnv:

    DEBUG: bool
    ENV_DEFAULT: bool
    SECRET_KEY: str
    DATABASE_URL: Any
    ALLOWED_HOSTS: list

    def __init__(self) -> None:
        self.DEBUG = config('DEBUG', default=True, cast=bool)
        self.SECRET_KEY = config('SECRET_KEY', default='django-insecure-jizyjlj_lvn@%m+g43c(s2$7*%4h0kqslhw85zcs#^jgsqjp36')
        self.DATABASE_URL = dj_database_url.parse(config('DATABASE_URL', default='postgres://admin:admin123@django-db:5432/inventory_management'))
        self.ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['*'], cast=list)
        
        
    
    def __configEnv(self):
        self.DEBUG = config('DEBUG', default=True, cast=bool)
        self.SECRET_KEY = config('SECRET_KEY', default='django-insecure-jizyjlj_lvn@%m+g43c(s2$7*%4h0kqslhw85zcs#^jgsqjp36')
        self.DATABASE_URL = dj_database_url.parse(config('DATABASE_URL'))
        self.ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['*'], cast=list)
    
    def __configOsEnv(self):
        self.DATABASE_URL = dj_database_url.parse(self.__env.str('DATABASE_URL'))
        self.DEBUG = self.__env.bool('DEBUG', default=True)
        self.SECRET_KEY = self.__env.str('SECRET_KEY', default='django-insecure-jizyjlj_lvn@%m+g43c(s2$7*%4h0kqslhw85zcs#^jgsqjp36')
        self.ALLOWED_HOSTS = self.__env.list('ALLOWED_HOSTS', default=['*'])
        