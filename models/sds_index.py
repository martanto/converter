from orator import Model
from database import database as db

Model.set_connection_resolver(db)

class SdsIndex(Model):
    pass