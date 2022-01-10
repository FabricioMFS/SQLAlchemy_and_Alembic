import pytest
import alembic
import asyncio
from alembic.config import Config
from os import environ
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from ..core.configs import settings

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope='session')
def create_db():
    # obtém url do banco pela variável de ambiente e constrói uma url de teste sync
    index = settings.URL_DB_ASYNC.find(':') 
    URL_DB_SYNC_TEST = f'postgresql{settings.URL_DB_ASYNC[index:]}_test'

    # cria instância de teste do banco de dados
    engine = create_engine(URL_DB_SYNC_TEST)
    if not database_exists(engine.url):
        create_database(engine.url)

    yield

    # destrói instância de teste do banco de dados
    if database_exists(engine.url):
        drop_database(engine.url)


@pytest.mark.asyncio
@pytest.fixture(scope='function')
def apply_migrations(create_db):
    # substitui as variáveis de ambiente prod para test
    settings.reload()

    URL_DB =settings.URL_DB_ASYNC
    URL_DB_TEST = URL_DB + '_test'

    environ['URL_DB_ASYNC'] = URL_DB_TEST

    # seleciona o arquivo de configuração do alembic
    config = Config("alembic.ini")
    # roda a migração
    alembic.command.upgrade(config, "head")
    yield    
    # desfaz a migração
    alembic.command.downgrade(config, "base")    
    environ['URL_DB_ASYNC'] = URL_DB
  
