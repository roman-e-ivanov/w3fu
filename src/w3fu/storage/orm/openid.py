from openid.association import Association
from openid.store import nonce
from time import time

from w3fu.storage.orm import Mapper


class OpenIdStore(Mapper):

    add_nonce_sql = '''
        insert ignore into nonces values (%{url}s, %{timestamp}s, %{salt}s)
    '''
    set_assoc_sql = '''
        replace into assocs values
        (%{url}s, %{handle}s, %{secret}s, %{issued}s, %{lifetime}s, %{type}s)
    '''
    get_assoc_sql = '''
        select handle, secret, issued, lifetime, type
        from assocs where url = %{url}s and handle = %{handle}s
    '''
    get_assocs_sql = '''
        select handle, secret, issued, lifetime, type
        from assocs where url = %{url}s
    '''
    remove_assoc_sql = '''
        delete from assocs where url = %{url}s and handle = %{handle}s
    '''

    def storeAssociation(self, url, assoc):
        params = {
                  'url': url,
                  'handle': assoc.handle,
                  'secret': assoc.secret,
                  'issued': assoc.issued,
                  'lifetime': assoc.lifetime,
                  'type': assoc.assoc_type
                  }
        self._conn.cursor().query(self.set_assoc_sql, params)

    def getAssociation(self, url, handle=None):
        params = {'url': url}
        if handle is None:
            cursor = self._conn.cursor().query(self.get_assocs_sql, params)
        else:
            params['handle'] = handle
            cursor = self._conn.cursor().query(self.get_assoc_sql, params)
        if not cursor.count:
            return None
        assocs = []
        for row in cursor:
            assoc = Association(row['handle'], row['secret'], row['issued'],
                                row['lifetime'], row['type'])
            if assoc.getExpiresIn() == 0:
                self.removeAssociation(url, assoc.handle)
            else:
                assocs.append((assoc.issued, assoc))
        if assocs:
            assocs.sort()
            return assocs[-1][1]
        else:
            return None

    def removeAssociation(self, url, handle):
        params = {'url': url, 'handle': handle}
        return self._conn.cursor().query(self.remove_assoc_sql, params).count > 0

    def useNonce(self, url, timestamp, salt):
        if abs(timestamp - time()) > nonce.SKEW:
            return False
        params = {'url': url, 'timestamp': timestamp, 'salt': salt}
        return self._conn.cursor().query(self.add_nonce_sql, params).count > 0
