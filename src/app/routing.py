from w3fu.args import StrArg, IdArg
from w3fu.routing import Router, Route


router = Router(
                test=Route('/test'),
                index=Route('/'),
                home=Route('/home'),
                register=Route('/register'),
                login=Route('/login'),
                shortcut_login=Route('/login/{shortcut}', shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}')),
                providers_public=Route('/providers'),
                provider_public=Route('/providers/{provider_id}', provider_id=IdArg('provider_id')),
                providers_list_admin=Route('/home/providers/list'),
                providers_admin=Route('/home/providers'),
                provider_admin=Route('/home/providers/{provider_id}', provider_id=IdArg('provider_id')),
                services_list_admin=Route('/home/providers/{provider_id}/services/list', provider_id=IdArg('provider_id')),
                services_admin=Route('/home/providers/{provider_id}/services', provider_id=IdArg('provider_id')),
                service_admin=Route('/home/services/{service_id}', service_id=IdArg('service_id')),
                )
