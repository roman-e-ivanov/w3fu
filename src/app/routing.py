from w3fu.args import StrArg, IdArg
from w3fu.routing import Router, Route


router = Router(
                 test=Route('/test'),
                 index=Route('/'),
                 home=Route('/home'),
                 register = Route('/register'),
                 login = Route('/login'),
                 shortcut_login = Route('/login/{shortcut}', shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}')),
                 providers_public = Route('/providers'),
                 provider_public = Route('/providers/{id_}', id_=IdArg('id_')),
                 providers_admin = Route('/home/providers'),
                 provider_admin = Route('/home/providers/{id_}', id_=IdArg('id_')),
                 providers_list_admin = Route('/home/providers/list'),
                 )