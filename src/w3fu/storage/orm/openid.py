from w3fu.storage.orm import Mapper


class OpenIDStore(Mapper):

    add_nonce_sql = 'insert into nonces values (%%s, %%s, %%s)'
    get_assoc_sql = '''
        select handle, secret, issued, lifetime, assoc_type
        from assocs where server_url = %%s AND handle = %%s
    '''
    get_assocs_sql = '''
        select handle, secret, issued, lifetime, assoc_type
        from assocs where server_url = %%s
    '''
    get_expired_sql = '''
        select server_url from assocs where issued + lifetime < %%s
    '''
    remove_assoc_sql = '''
        delete from assocs where server_url = %%s and handle = %%s
    '''
    set_assoc_sql = '''
        replace into assocs values (%%s, %%s, %%s, %%s, %%s, %%s)
    '''

    def storeAssociation(self, server_url, association):
        pass

    def getAssociation(self, server_url, handle=None):
        pass

    def removeAssociation(self, server_url, handle):
        pass

    def useNonce(self, server_url, timestamp, salt):
        pass
