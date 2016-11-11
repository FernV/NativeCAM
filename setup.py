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

import sys
import os

try :
    from lxml import etree
except :
    print('python-lxml required, command is in README.md')
    exit(1)

lcode = os.getenv('LANGUAGE', 'en')[0:2]
# print lcode

if "c" in sys.argv[1:] :
    cls = True
else :
    cls = False

print 'wait, processing...'

find = os.popen("find /usr -name 'hal_pythonplugin.py'").read()
if find > '' :
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
                else :
                    print('"from ncam import NCam" already exists in %s\n' % s)

        head, fn = os.path.split(s)

        fn = os.path.join(head, 'ncam.py')
        if os.path.islink(fn) :
            if cls :
                os.remove(fn)
                print 'removed link to ncam.py from ', head, '\n'
            else :
                print 'link to ncam.py already exists in ', head, '\n'
        elif not cls :
            os.symlink(os.path.join(os.getcwd(), 'ncam.py'), fn)
            print 'created link to ncam.py in ', head, '\n'

        sd = os.path.join(head, 'path2ncam')
        if os.path.isfile(sd) :
            os.remove(sd)
            print 'removed path2ncam file'
        if not cls :
            open(sd, "w").write(os.getcwd())
            print 'created path2ncam file'

else :
    print 'Directory of "hal_pythonplugin.py" not found - EXITING'
    exit(2)


edited = False
find = os.popen("find /usr -name 'hal_python.xml'").read()
if find > '' :
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
                        edited = True
                        print('glade-widget-class named NCam removed from %s\n' % s)
                        break
            else :
                classfounded = False
                for n in dest.findall('glade-widget-class'):
                    if n.get('name') == 'NCam':
                        classfounded = True
                        print('glade-widget-class named NCam already exists in %s\n' % s)
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
                    edited = True
                    print('glade-widget-class named NCam added to %s\n' % s)


            dest = root.find('glade-widget-group')
            if cls :
                for n in dest.findall('glade-widget-class-ref') :
                    if n.get('name') == 'NCam':
                        dest.remove(n)
                        edited = True
                        print('glade-widget-class-ref name NCam removed from %s\n' % s)
                        break
            else :
                classfounded = False
                for n in dest.findall('glade-widget-class-ref'):
                    if n.get('name') == 'NCam':
                        classfounded = True
                        print('glade-widget-class-ref named NCam already exists in %s' % s)
                        break
                if not classfounded :
                    dest.insert(0, etree.fromstring('<glade-widget-class-ref name="NCam"/>'))
                    edited = True
                    print('glade-widget-class-ref named NCam added to %s\n' % s)

            if edited :
                xml.write(s, pretty_print = True)
                print s, 'saved'

else :
    print 'File "hal_python.xml" not found - EXITING'
    exit(3)

if cls :
    # remove link to translation file
    pass
else :
    # add link to translation files
    pass

exit(0)
