#!/usr/bin/env python

# This script will erase modifications made to run Features embedded

from lxml import etree
import getopt
import sys
import string

fname = '/usr/share/pyshared/gladevcp/hal_pythonplugin.py'
f = open(fname).read()
if f.find('from features import Features') >= 0 :
    open(fname, "w").write(f.replace('from features import Features', ''))

fname = '/usr/share/glade3/catalogs/hal_python.xml'
xml = etree.parse(fname)
root = xml.getroot()

dest = root.find('glade-widget-classes')
for n in dest.findall('glade-widget-class'):
    if n.get('name') == 'Features':
        dest.remove(n)
        break

dest = root.find('glade-widget-group')
for n in dest.findall('glade-widget-class-ref'):
    if n.get('name') == 'Features':
        dest.remove(n)
        break

xml.write(fname, pretty_print = True)
