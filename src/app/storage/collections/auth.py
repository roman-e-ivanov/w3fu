from w3fu.storage.collections import Collection, errorsafe, wrapped

from app.storage.documents.auth import User


class Users(Collection):

    _doc_cls = User
    _indexes = [('email', {'unique': True}),
                ('shortcut', {'unique': True}),
                ('sessions.id', {})]

    @errorsafe
    def push_session(self, user, session):
        self._collection.update({'_id': user.id},
                                {'$push': {'sessions': session.raw}})

    @errorsafe
    def pull_session(self, id):
        self._collection.update({'sessions.id': id},
                                {'$pull': {'sessions': {'id': id}}})

    @errorsafe
    def update_password(self, user):
        self._collection.update({'_id': user.id},
                                {'$set': {'password': user.password},
                                 '$unset': {'shortcut': 1}})

    @wrapped
    @errorsafe
    def find_email(self, email):
        return self._collection.find_one({'email': email})

    @wrapped
    @errorsafe
    def find_shortcut(self, shortcut):
        return self._collection.find_one({'shortcut': shortcut})

    @wrapped
    @errorsafe
    def find_valid_session(self, id, expires):
        return self._collection.find_one({'sessions.id': id,
                                          'sessions.expires': {'$gt': expires}})
