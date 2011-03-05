from w3fu.storage.mapping import Mapper
from w3fu.data.domain.auth import User, Session


class Users(Mapper):

    table = 'users'
    rowcls = User

    find_by_login_sql = 'select * from {self} where login = %(p0)s'


class Sessions(Mapper):

    table = 'sessions'
    rowcls = Session

    find_sql = '''
        select * from {self} where {pk} = %(p0)s and utc_timestamp() < expires
    '''
