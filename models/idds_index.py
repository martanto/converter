from orator import Model
from database import database as db

Model.set_connection_resolver(db)

class IddsIndex(Model):
    __table__ = 'idds_indexes'
    pass
