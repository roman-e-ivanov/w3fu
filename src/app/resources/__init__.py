from app.resources.index import Index
from app.resources.auth import Login, Register
from app.resources.home import Home
from app.resources.geo import PlaceSuggest


resources = [Index, Home,
             Login, Register,
             PlaceSuggest]
