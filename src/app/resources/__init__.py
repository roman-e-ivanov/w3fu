from app.routing import router

from app.resources.test import Test
from app.resources.index import Index
from app.resources.home import Home
from app.resources.auth import ShortcutLogin, Login, Register
from app.resources.providers import ProviderPublic, ProvidersPublic, \
    ProvidersListAdmin, ProviderAdmin, ProvidersAdmin
from app.resources.services import \
    ServicesListAdmin, ServicesAdmin, ServiceAdmin, \
    ServiceGroupsAdmin, ServiceGroupAdmin
from app.resources.workers import \
    WorkersListAdmin, WorkersAdmin, WorkerAdmin


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
router['services_admin'].target = ServicesAdmin()
router['service_admin'].target = ServiceAdmin()
router['services_list_admin'].target = ServicesListAdmin()
router['service_groups_admin'].target = ServiceGroupsAdmin()
router['service_group_admin'].target = ServiceGroupAdmin()
router['workers_admin'].target = WorkersAdmin()
router['worker_admin'].target = WorkerAdmin()
router['workers_list_admin'].target = WorkersListAdmin()
