from db.crud.base import CrudBase, Session, show_error, select, delete
from db.models.models import *
from db.session import db

class CRUD(CrudBase):
    def __init__(self, db, model, soft_delete = False):
        self.model = model
        self.soft_delete = soft_delete
        self.db = db


#model_name = CRUD(ModelName)
