from app.routing import router

from app.resources.test import Test
from app.resources.index import Index
from app.resources.home import Home
from app.resources.auth import ShortcutLogin, Login, Register
from app.resources.providers import ProviderPublic, ProvidersPublic, \
    ProvidersListAdmin, ProviderAdmin, ProvidersAdmin


router['test'].target = Test()
router['home'].target = Home()
router['index'].target = Index()
router['register'].target = Register()
router['login'].target = Login()
router['shortcut_login'].target = ShortcutLogin()
router['providers_public'].target = ProvidersPublic()
router['provider_public'].target = ProviderPublic()
router['providers_admin'].target = ProvidersAdmin()
router['provider_admin'].target = ProviderAdmin()
router['providers_list_admin'].target = ProvidersListAdmin()
