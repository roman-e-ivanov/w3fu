from w3fu.storage.collections import Collection, errorsafe, wrapped

from app.storage.documents.auth import User


class Users(Collection):

    _doc_cls = User
    _indexes = [('login', {'unique': True}),
                ('sessions.id', {})]

    @errorsafe
    def push_session(self, id, session):
        self._collection.update({'_id': id},
                                {'$push': {'sessions': session.raw}})

    @errorsafe
    def pull_session(self, id):
        self._collection.update({'sessions.id': id},
                                {'$pull': {'sessions': {'id': id}}})

    @wrapped
    @errorsafe
    def find_login(self, login):
        return self._collection.find_one({'login': login})

    @wrapped
    @errorsafe
    def find_valid_session(self, id, expires):
        return self._collection.find_one({'sessions.id': id,
                                          'sessions.expires': {'$gt': expires}})
