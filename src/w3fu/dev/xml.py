# -*- coding: utf-8 -*-

from lxml import etree
from timeit import timeit


def toxml(data, name):
    e = etree.Element(name)
    for k, v in data.iteritems():
        xmlworker(v, k, e)
    return e

def xmlworker(data, name, root):
    if isinstance(data, basestring):
        etree.SubElement(root, name).text = data
        return
    try:
        i = data.iteritems()
        e = etree.SubElement(root, name)
        for k, v in i:
            xmlworker(v, k, e)
        return
    except AttributeError:
        pass
    try:
        for v in data:
            xmlworker(v, name, root)
        return
    except TypeError:
        pass
    etree.SubElement(root, name).text = str(data)


def toxml2(data, name):
    e = etree.Element(name)
    for k, v in data.iteritems():
        xmlworker2(v, k, e)
    return e

def xmlworker2(data, name, root, extend=True):
    if isinstance(data, basestring):
        if extend:
            etree.SubElement(root, name).text = data
        else:
            root.set(name, data)
        return
    try:
        i = data.iteritems()
        e = etree.SubElement(root, name)
        for k, v in i:
            xmlworker2(v, k, e, False)
        return
    except AttributeError:
        pass
    try:
        for v in data:
            xmlworker2(v, name, root)
        return
    except TypeError:
        pass
    if extend:
        etree.SubElement(root, name).text = str(data)
    else:
        root.set(name, str(data))


z = {
     'a': 'x',
     'b': ['y', 'z'],
     'c': { 'd': '1', 'e': [{'z': '7'}, ['4', '5']], 'f': '8', 'g': '9', 'h': '10', 'i': '11', 'j': '12' }
     }

z2 = {
      'x': 6,
      'list': {
               'user': [
                         {
                          'login': 'vasya', 'password': '12345678',
                          'login2': 'vasya', 'password2': '12345678',
                          'login3': 'vasya', 'password3': '12345678',
                          'login4': 'vasya', 'password4': '12345678',
                          'login5': 'vasya', 'password5': '12345678',
                          'login6': 'vasya', 'password6': '12345678',
                          'login7': 'vasya', 'password7': '12345678'
                          },
                         ]
               }
      }

e1 = toxml(z2, 'root')
e2 = toxml2(z2, 'root')

print etree.tostring(e1, pretty_print=True, encoding='utf8')
print etree.tostring(e2, pretty_print=True, encoding='utf8')

t1 = timeit(lambda: toxml(z2, 'root'), number=10000)
t2 = timeit(lambda: toxml2(z2, 'root'), number=10000)

t = t1 + t2

p1 = 100 * t1 / t
p2 = 100 * t2 / t

print p1
print p2
