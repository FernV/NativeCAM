#!/usr/bin/env python

'''
Will create links and modify files to embed NativeCAM in LinuxCNC
should work with any linux distro

usage :
    sudo python setup.py [c]

    w/ argument c will restore files and delete links
    w/o argument will create links and modify files

DO NOT USE IN ANY WAYS AFTER NATIVECAM IS INTEGRATED WITH LINUXCNC DISTRIBUTION

Created on 2016-10-08

@author: Fernand Veilleux
'''

from lxml import etree
import sys
import os


if "c" in sys.argv[1:] :
    cls = True
else :
    cls = False

find = os.popen("find /usr -name 'hal_pythonplugin.py'").read()
found = find > ''

if found :
    for s in find.split() :
        s = s.rstrip('\n')
        if not os.path.islink(s) :
            f = open(s).read()
            if cls :
                if f.find('from ncam import NCam') >= 0:
                    open(s, "w").write(f.replace('from ncam import NCam', ''))
                    print('"from ncam import NCam" removed from %s\n' % s)
            else :
                if f.find('from ncam import NCam') == -1:
                    open(s, "w").write('from ncam import NCam\n' + f)
                    print('"from ncam import NCam" added to %s\n' % s)

        head, fn = os.path.split(s)
        fn = os.path.join(head, 'ncam.py')
        if os.path.isfile(fn) :
            if cls :
                os.remove(fn)
                print 'removed link from ', head
        elif not cls :
            os.symlink(os.path.join(os.getcwd(), 'ncam.py'), fn)
            print 'created link in ', head


if not found :
    print 'Directory of "hal_pythonplugin.py" not found - EXITING'
    print 'Contact Fern for help'
    exit(1)


find = os.popen("find /usr -name 'hal_python.xml'").read()
found = find > ''

if found :
    for s in find.split() :
        s = s.rstrip('\n')
        if not os.path.islink(s) :
            xml = etree.parse(s)
            root = xml.getroot()
            dest = root.find('glade-widget-classes')
            if cls :
                for n in dest.findall('glade-widget-class'):
                    if n.get('name') == 'NCam':
                        dest.remove(n)
                        print('glade-widget-class named NCam removed from %s' % s)
                        break
            else :
                classfounded = False
                for n in dest.findall('glade-widget-class'):
                    if n.get('name') == 'NCam':
                        classfounded = True
                        print('glade-widget-class named NCam removed from %s' % s)
                        break
                if not classfounded :
                    elem = etree.fromstring('''
<glade-widget-class name="NCam" generic-name="ncam" title="ncam">
            <properties>
                <property id="size" query="False" default="1" visible="False"/>
                <property id="spacing" query="False" default="0" visible="False"/>
                <property id="homogeneous" query="False" default="0" visible="False"/>
            </properties>
        </glade-widget-class> \n

''')
                    dest.insert(0, elem)
                    print('glade-widget-class named NCam added to %s' % s)


            dest = root.find('glade-widget-group')
            if cls :
                for n in dest.findall('glade-widget-class-ref') :
                    if n.get('name') == 'NCam':
                        dest.remove(n)
                        print('glade-widget-class-ref name NCam removed from %s' % s)
                        break
            else :
                classfounded = False
                for n in dest.findall('glade-widget-class-ref'):
                    if n.get('name') == 'NCam':
                        classfounded = True
                        break
                if not classfounded :
                    dest.insert(0, etree.fromstring('<glade-widget-class-ref name="NCam"/>'))
                    print('glade-widget-class-ref named NCam added to %s' % s)

            xml.write(s, pretty_print = True)

if not found :
    print 'File "hal_python.xml" not found - EXITING'
    print 'Contact Fern for help'
    exit(1)

exit(0)