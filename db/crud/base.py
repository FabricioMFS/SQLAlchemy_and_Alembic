import pprint
from datetime import datetime
from typing import TypeVar, List

from sqlalchemy.sql.expression import column
from sqlalchemy.orm import Session, selectinload, session
from sqlalchemy import select, delete, update

from db.models.models import Base
from db.session import DbConnect


def show_error(error):
    pprint.pprint(error)
    return {'status': False}

def res_success(obj=None):
    return {'status': True, 'content': obj}


ModelType = TypeVar("ModelType", bound=Base)

class CrudBase(DbConnect):
    soft_delete = False
    db = DbConnect

    async def create(self, obj: ModelType = None, value: dict = None):

        if value:
            obj = self.model(**value)

        try:
            async with next(self.db.get_db()) as conn:
                conn.add(obj)
                await conn.commit()

                return res_success(obj)
        except Exception as error:
            return show_error(error)

    async def create_multiple(self, objs: List[ModelType] = None, values: List[dict] = None):
        if values:
            objs = [self.model(**value) for value in values]

        try:
            async with next(self.db.get_db()) as conn:
                conn.add_all(objs)
                await conn.commit()

                return res_success(objs)
        except Exception as error:
            return show_error(error)

    async def search_by_id(self, id: int, query_params: dict = {}):

        params = []
        
        if self.soft_delete:
            params.append(self.model.deleted_at == None)
        
        for key, value in query_params.items():
            if isinstance(query_params.get(key), List):
                params.append(column(key).in_(value))
            else:
                params.append(column(key) == value)


        query = select(self.model).where(self.model.id == id, *params)

        try:
            async with next(self.db.get_db()) as conn:
                obj = await conn.execute(query)
                return res_success(obj.scalars().all())
        except Exception as error:
            return show_error(error)

    async def search_by_ids(self, ids: list, query_params:dict = {}):

        params = []
        
        if self.soft_delete:
            params.append(self.model.deleted_at == None)
        
        for key, value in query_params.items():
            if isinstance(query_params.get(key), List):
                params.append(column(key).in_(value))
            else:
                params.append(column(key) == value)


        query = select(self.model).where(self.model.id.in_(ids), *params)

        try:
            async with next(self.db.get_db()) as conn:
                obj = await conn.execute(query)
                return res_success(obj.scalars().all())
        except Exception as error:
            return show_error(error)

    async def show_all(self, query_params:dict = {}):
        params = []

        if self.soft_delete:
            params.append(self.model.deleted_at == None)
        
        for key, value in query_params.items():
            if isinstance(query_params.get(key), List):
                params.append(column(key).in_(value))
            else:
                params.append(column(key) == value)


        query = select(self.model).where(*params)

        try:
            async with next(self.db.get_db()) as conn:
                obj = await conn.execute(query)

                return res_success(obj.scalars().all())
        except Exception as error:
            return show_error(error)

    async def modify(self, id, values: dict):

        query = update(self.model).where(self.model.id == id).values(values)

        try:
            async with next(self.db.get_db()) as conn:
                await conn.execute(query)
                await conn.commit()

                return res_success()
        except Exception as error:
            return show_error(error)

    async def modify_multiple(self, ids: list, values: dict):

        query = update(self.model).where(self.model.id.in_(ids)).values(values)

        try:
            async with next(self.db.get_db()) as conn:
                await conn.execute(query)
                await conn.commit()

                return res_success()
        except Exception as error:
            return show_error(error)


    async def destroy(self, id):
        if self.soft_delete:
            values = dict()
            values['deleted_at'] = datetime.now()
            values['updated_at'] = datetime.now()

            query = update(self.model).where(self.model.id == id).values(values)
        else:
            query = delete(self.model).where(self.model.id == id)

        try:
            async with next(self.db.get_db()) as conn:
                await conn.execute(query)
                await conn.commit()

                return res_success()
        except Exception as error:
            return show_error(error)

    async def destroy_multiple(self, ids: list):

        if self.soft_delete:
            values = dict()
            values['deleted_at'] = datetime.now()
            values['updated_at'] = datetime.now()
            query = update(self.model).where(self.model.id.in_(ids)).values(values)
        else:
            query = delete(self.model).where(self.model.id.in_(ids))

        try:
            async with next(self.db.get_db()) as conn:
                await conn.execute(query)
                await conn.commit()

                return True
        except Exception as error:
            return show_error(error)
