class AttributesMeta(type):

    def __init__(cls, name, bases, attrs):
        for name, attr in attrs.iteritems():
            cls.attribute(name, attr)
        super(AttributesMeta, cls).__init__(name, bases, attrs)
