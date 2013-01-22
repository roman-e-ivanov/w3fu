from w3fu.storage import Database

from app import config

from app.storage.auth import Users, User
from app.storage.geo import Places, Place
from app.storage.providers import Providers, Provider
from app.storage.services import Services, Service
from app.storage.workers import Workers, Worker


database = Database(uri=config.db_uri, dbname=config.db_name)

users_c = Users(database, 'users', User)
providers_c = Providers(database, 'providers', Provider)
services_c = Services(database, 'services', Service)
workers_c = Workers(database, 'workers', Worker)
places_c = Places(database, 'places', Place)
