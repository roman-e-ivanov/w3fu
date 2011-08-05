from pymongo.errors import DuplicateKeyError

from w3fu.storage.collections import Collection
from w3fu.storage.documents.auth import User


class Users(Collection):

    _doccls = User

    def _ensure_index(self):
        self._c.ensure_index('login', unique=True)
        self._c.ensure_index('sessions.id')

    def insert(self, doc):
        try:
            self._c.insert(doc, safe=True)
            return True
        except DuplicateKeyError:
            return False

    def _find_login(self, login):
        return self._c.find_one({'login': login}, as_class=self._doccls)

    def _find_valid_session(self, id, expires):
        return self._c.find_one({'sessions.id': id,
                                 'sessions.expires': {'$gt': expires}},
                                as_class=self._doccls)

    def _push_session(self, user, session):
        self._c.update({'_id': user.id}, {'$push': {'sessions': session}})

    def _pull_session(self, id):
        self._c.update({'sessions.id': id}, {'$pull': {'sessions': {'id': id}}})
