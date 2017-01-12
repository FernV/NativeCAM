'''
Created on 2016-11-28

@author: Fernand Veilleux
'''

import gtk
import sys
import pygtk
pygtk.require('2.0')

from lxml import etree
# import gobject
import ConfigParser
import re, os
# import getopt
# import shutil
# import hashlib
# import subprocess
# import webbrowser
import io
# from cStringIO import StringIO
# import gettext
# import time
# import locale

CFG_DIR = 'cfg'
CATALOGS_DIR = 'catalogs'

# try :
#    t = gettext.translation('ncam', '/usr/share/locale')
#    _ = t.ugettext
# except :
#    gettext.install('ncam', None, unicode = True)

class Parameter() :
    def __init__(self, ini = None, ini_id = None, xml = None) :
        self.attr = {}
        self.from_ini(ini, ini_id)

    def __repr__(self) :
        return etree.tostring(self.to_xml(), pretty_print = True)

    def from_ini(self, ini, ini_id) :
        self.attr = {}
        ini = dict(ini)
        for i in ini :
            self.attr[i] = ini[i]

    def get_name(self) :
        return self.attr["name"] if "name" in self.attr else ""

    def get_attr(self, name) :
        return self.attr[name] if name in self.attr else None

class Feature():
    def __init__(self, src = None, xml = None) :
        self.attr = {}
        self.param = []
        if src is not None :
            self.from_src(src)
        elif xml is not None :
            self.from_xml(xml)

    def __repr__(self) :
        return etree.tostring(self.to_xml(), pretty_print = True)

#    def get_attr(self, attr) :
#        return self.attr[attr] if attr in self.attr else None

    def get_name(self):
        return self.attr["name"] if "name" in self.attr else ""

    def from_src(self, src) :
        src_config = ConfigParser.ConfigParser()
        f = open(src).read()

        # add "." in the begining of multiline parameters to save indents
        f = re.sub(r"(?m)^(\ |\t)", r"\1.", f)
        src_config.readfp(io.BytesIO(f))
        # remove "." in the begining of multiline parameters to save indents
        conf = {}
        for section in src_config.sections() :
            conf[section] = {}
            for item in src_config.options(section) :
                s = src_config.get(section, item, raw = True)
                s = re.sub(r"(?m)^\.", "", " " + s)[1:]
                conf[section][item] = s
        self.attr = conf["SUBROUTINE"]

        self.attr["src"] = src
        self.attr["name"] = self.get_name()

        # get order
        if "order" not in self.attr :
            self.attr["order"] = []
        else :
            self.attr["order"] = self.attr["order"].upper().split()
        self.attr["order"] = [s if s[:6] == "PARAM_" else "PARAM_" + s \
                              for s in self.attr["order"]]

        # get params
        self.param = []
        parameters = self.attr["order"] + [p for p in conf if \
                    (p[:6] == "PARAM_" and p not in self.attr["order"])]
        for s in parameters :
            if s in conf :
                p = Parameter(ini = conf[s], ini_id = s.lower())
                p.attr['name'] = p.get_name()
                p.attr['tool_tip'] = (p.get_attr('tool_tip') \
                            if "tool_tip" in p.attr else p.get_attr('name'))
                opt = p.attr["options"] if "options" in self.attr else None
                self.param.append(p)


def mess_dlg(mess, title = "NativeCAM Translation"):
    dlg = gtk.MessageDialog(parent = None,
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        type = gtk.MESSAGE_WARNING,
        buttons = gtk.BUTTONS_OK, message_format = '%s' % mess)
    dlg.set_title(title)
    dlg.set_keep_above(True)
    dlg.run()
    dlg.destroy()


def get_translations() :

    def get_menu_strings(path, trslatbl):
        for ptr in range(len(path)) :
            p = path[ptr]
            if p.tag.lower() == "group":
                name = p.get("name") if "name" in p.keys() else None
                if (name is not None) :
                    trslatbl.append("_(%s)" % repr(name))

                tooltip = p.get('tool_tip') if "tool_tip" in p.keys() else None
                if (tooltip is not None) and (tooltip != '') :
                    trslatbl.append("_(%s)" % repr(tooltip))

                get_menu_strings(p, trslatbl)

            elif p.tag.lower() == "sub":
                name = p.get("name") if "name" in p.keys() else None
                if (name is not None) :
                    trslatbl.append("_(%s)" % repr(name))

                tooltip = p.get('tool_tip') if "tool_tip" in p.keys() else None
                if (tooltip is not None) and (tooltip != '') :
                    trslatbl.append("_(%s)" % repr(tooltip))

    def get_strings():
        # py and glade files
        os.popen("xgettext ./ncam.py ./*.glade -o ./locale/_a.po")
        os.popen("sed --in-place ./locale/_a.po -e s/charset=CHARSET/charset=UTF-8/")

        # catalogs
        find = os.popen("find ./%s -name 'menu.xml'" % CATALOGS_DIR).read()
        for s in find.split() :
            translatable = []
            d, splitname = os.path.split(s)
            d, catalog = os.path.split(d)

            destname = './locale/' + splitname
            xml = etree.parse(s).getroot()
            get_menu_strings(xml, translatable)

            translatable = "\n".join(translatable)
            open(destname, "w").write(translatable)

            os.popen("xgettext --language=Python --from-code=UTF-8 %s -o %s" % (destname, destname))
            os.popen("sed --in-place %s -e s/charset=CHARSET/charset=UTF-8/" % destname)
            os.popen("sed --in-place %s -e 's/locale/%s/g'" % (destname, catalog))
            os.popen("msgcat %s ./locale/_a.po -o ./locale/_a.po" % destname)
            os.popen("rm %s" % destname)

        # cfg files
        find = os.popen("find ./%s -name '*.cfg'" % CFG_DIR).read()
        for s in find.split() :
            translatable = []
            d, splitname = os.path.split(s)
            d, catalog = os.path.split(d)
            destname = './locale/' + splitname

            f = Feature(src = s)
            for i in ["name", "help"] :
                if i in f.attr :
                    translatable.append("_(%s)" % repr(f.attr[i]))

            for p in f.param :
                for i in ["name", "help", "tool_tip", "options"] :
                    if i in p.attr :
                        translatable.append("_(%s)" % repr(p.attr[i]))

            translatable = "\n".join(translatable)
            open(destname, "w").write(translatable)

            os.popen("xgettext --language=Python --from-code=UTF-8 %s -o %s" % (destname, destname))
            os.popen("sed --in-place %s -e s/charset=CHARSET/charset=UTF-8/" % destname)
            os.popen("sed --in-place %s -e 's/locale/%s/g'" % (destname, catalog))
            os.popen("msgcat %s ./locale/_a.po -o ./locale/_a.po" % destname)
            os.popen("rm %s" % destname)

        if os.path.exists("./locale/ncam.po") :
            os.popen("msgcat ./locale/_a.po ./locale/ncam.po -o ./locale/ncam.po")
            os.remove("./locale/_a.po")
        else :
            os.rename("./locale/_a.po", "./locale/ncam.po")

    try :
        get_strings()
        mess_dlg('Done !\nFile : ./locale/ncam.po')
    except Exception, detail :
        mess_dlg('Error while getting data for translation :\n\n%(detail)s' % \
                   {'detail':detail})

if __name__ == "__main__":
    get_translations()
