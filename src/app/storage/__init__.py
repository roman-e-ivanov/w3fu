from w3fu.storage import BaseModel, Database

from app import config


database = Database(uri=config.db_uri, dbname=config.db_name)


class Model(BaseModel):

    _database = database
