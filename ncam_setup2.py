#!/usr/bin/env python

from lxml import etree
import getopt
import sys

if "c" in sys.argv[1:] :
    cls = True
else :
    cls = False


fname = '/usr/share/pyshared/gladevcp/hal_pythonplugin.py'
f = open(fname).read()
if cls :
    if f.find('from ncam import NCam') >= 0:
        open(fname, "w").write(f.replace('from ncam import NCam', ''))
else :
    if f.find('from ncam import NCam') == -1:
        open(fname, "w").write('from ncam import NCam\n' + f)

fname = '/usr/share/glade3/catalogs/hal_python.xml'
xml = etree.parse(fname)
root = xml.getroot()

dest = root.find('glade-widget-classes')
for n in dest.findall('glade-widget-class'):
    if n.get('name') == 'NCam':
        if cls :
            dest.remove(n)
        break

elem = etree.fromstring('''
<glade-widget-class name="NCam" generic-name="ncam" title="ncam">
    <properties>
        <property id="size" query="False" default="1" visible="False"/>
        <property id="spacing" query="False" default="0" visible="False"/>
        <property id="homogeneous" query="False" default="0" visible="False"/>
    </properties>
</glade-widget-class>\n
''')
if not cls:
    dest.insert(0, elem)

dest = root.find('glade-widget-group')
for n in dest.findall('glade-widget-class-ref'):
    if n.get('name') == 'NCam':
        if cls :
            dest.remove(n)
        break

elem = etree.fromstring('''<glade-widget-class-ref name="NCam"/>
''')
if not cls:
    dest.insert(0, elem)

xml.write(fname, pretty_print = True)
