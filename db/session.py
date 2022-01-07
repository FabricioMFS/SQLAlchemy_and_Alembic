from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

URL_DB_ASYNC = "postgresql+asyncpg://postgres:secret@localhost/estudos_SQL"
DB_POOL_SIZE = 5

class DbConnect:
    def __init__(self, URL_ASYNC=None, URL_SYNC=None):
        self.URL_ASYNC = URL_ASYNC
        self.URL_SYNC = URL_SYNC

        if self.URL_ASYNC:
            self.engine = create_async_engine(self.URL_ASYNC, pool_size=DB_POOL_SIZE)
            self.session_local = sessionmaker(bind=self.engine,
                                              autoflush=False,
                                              autocommit=False,
                                              expire_on_commit=False,
                                              class_=AsyncSession
                                              )

        else:
            self.engine = create_engine(self.URL_SYNC)
            self.session_local = sessionmaker(bind=self.engine,
                                              autoflush=False,
                                              autocommit=False,
                                              expire_on_commit=False,
                                              )
    def get_db(self):
        try:
            yield self.session_local()
        finally:
            pass

db = DbConnect(URL_ASYNC=URL_DB_ASYNC)



