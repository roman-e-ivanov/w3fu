from w3fu.storage.collections import Collection, errorsafe, wrapped

from app.storage.documents.firms import Firm


class Firms(Collection):

    _doc_cls = Firm
