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
# import ConfigParser
import re, os
# import getopt
# import shutil
# import hashlib
# import subprocess
# import webbrowser
# import io
# from cStringIO import StringIO
# import gettext
# import time
# import locale

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

    def get_icon(self) :
        return get_pixbuf(self.get_attr("icon"), treeview_icon_size)

    def get_image(self) :
        return get_pixbuf(self.get_attr("image"), add_dlg_icon_size)

    def get_value(self):
        return self.attr["value"] if "value" in self.attr else ""

    def set_value(self, new_val):
        self.attr["value"] = new_val

    def get_type(self):
        return self.attr["type"] if "type" in self.attr else "string"

    def get_tooltip(self):
        return self.attr["tool_tip"] if "tool_tip" in self.attr else \
            self.attr["help"] if "help" in self.attr else None

    def get_attr(self, attr) :
        return self.attr[attr] if attr in self.attr else None

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
                if p.get_type() == 'float' :
                    fmt = '{0:0.%sf}' % p.get_digits()
                    p.set_value(fmt.format(get_float(p.get_value())))
                elif p.get_type() == 'int' :
                    p.set_value(str(get_int(p.get_value())))
                self.param.append(p)

        self.attr["id"] = self.attr["type"] + '_000'

        # get gcode parameters
        for l in ["definitions", "before", "call", "after"] :
            l = l.upper()
            if l in conf and "content" in conf[l] :
                self.attr[l.lower()] = re.sub(r"(?m)\r?\n\r?\.", "\n",
                                              conf[l]["content"])
            else :
                self.attr[l.lower()] = ""

    def from_xml(self, xml) :
        self.attr = {}
        for i in xml.keys() :
            self.attr[i] = xml.get(i)

        self.param = []
        for p in xml :
            self.param.append(Parameter(xml = p))

        if 'short_id' in self.attr :
            del self.attr['short_id']

    def to_xml(self) :
        xml = etree.Element("feature")
        for i in self.attr :
            xml.set(i, unicode(str(self.attr[i])))

        for p in self.param :
            xml.append(p.to_xml())
        return xml

    def get_id(self, xml) :
        num = 1
        if xml is not None :
            # get smallest free name
            l = xml.findall(".//feature[@type='%s']" % self.attr["type"])
            num = max([get_int(i.get("id")[-3: ]) for i in l] + [0]) + 1
        self.attr["id"] = self.attr["type"] + "_%03d" % num

    def get_short_id(self):
        global UNIQUE_ID
        id = self.attr['short_id'] if 'short_id' in self.attr else None
        if id is None :
            id = str(UNIQUE_ID)
            self.attr["short_id"] = id
            UNIQUE_ID += 1
        return id

    def get_definitions(self) :
        global DEFINITIONS
        if self.attr["type"] not in DEFINITIONS :
            s = self.attr["definitions"] if "definitions" in self.attr else ''
            if s != '' :
                s = self.process(s)
                if s != "" :
                    DEFINITIONS.append(self.attr["type"])
                return s
        return ""

    def include(self, srce) :
        src = search_path(2, srce, LIB_DIR)
        if src is not None:
            return open(src).read()
        return ''

    def include_once(self, src) :
        global INCLUDE
        if src not in INCLUDE :
            INCLUDE.append(src)
            return self.include(src)
        return ""

    def process(self, s, line_leader = '') :

        def eval_callback(m) :
            try :
                return str(eval(m.group(2), globals(), {"self":self}))
            except :
                return ''

        def exec_callback(m) :
            s = m.group(2)

            # strip starting spaces
            s = s.replace("\t", " ")
            i = 1e10
            for l in s.split("\n") :
                if l.strip() != "" :
                    i = min(i, len(l) - len(l.lstrip()))
            if i < 1e10 :
                res = ""
                for l in s.split("\n") :
                    res += l[i:] + "\n"
                s = res

            old_stdout = sys.stdout
            redirected_output = StringIO()
            sys.stdout = redirected_output
            exec(s) in {"self":self}
            sys.stdout = old_stdout
            redirected_output.reset()
            out = str(redirected_output.read())
            return out

        def subprocess_callback(m) :
            s = m.group(2)

            # strip starting spaces
            s = s.replace("\t", "  ")
            i = 1e10
            for l in s.split("\n") :
                if l.strip() != "" :
                    i = min(i, len(l) - len(l.lstrip()))
            if i < 1e10 :
                res = ""
                for l in s.split("\n") :
                    res += l[i:] + "\n"
                s = res
            try :
                return subprocess.check_output([s], shell = True,
                                               stderr = subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                msg = _('Error with subprocess: returncode = %(errcode)s\n'
                         'output = %(output)s\n'
                         'e= %(e)s\n') \
                         % {'errcode':e.returncode, 'output':e.output, 'e':e}
                print msg
                mess_dlg(msg)
                return ''

        def import_callback(m) :
            fname = m.group(2)
            fname = search_path(2, fname, XML_DIR)
            if fname is not None :
                return str(open(fname).read())

        s = re.sub(r"#sub_name", "%s" % self.attr['name'], s)
        s = re.sub(r"%NCAM_DIR%", "%s" % NCAM_DIR, s)

        for p in self.param :
            if "call" in p.attr and "value" in p.attr :
                if p.attr['type'] == 'text' :
                    note_lines = p.get_value().split('\n')
                    lines = ''
                    for line in note_lines :
                        lines = lines + '( ' + line + ' )\n'
                    s = re.sub(r"%s([^A-Za-z0-9_]|$)" %
                       (re.escape(p.attr["call"])), r"%s\1" %
                       lines, s)

                else :
                    s = re.sub(r"%s([^A-Za-z0-9_]|$)" %
                       (re.escape(p.attr["call"])), r"%s\1" %
                       p.get_value(), s)

        s = re.sub(r"%NCAM_DIR%", "%s" % NCAM_DIR, s)
        s = re.sub(r"(?i)(<import>(.*?)</import>)", import_callback, s)
        s = re.sub(r"(?i)(<eval>(.*?)</eval>)", eval_callback, s)
        s = re.sub(r"(?ims)(<exec>(.*?)</exec>)", exec_callback, s)
        s = re.sub(r"(?ims)(<subprocess>(.*?)</subprocess>)",
                   subprocess_callback, s)

        f_id = self.get_attr("id")
        s = re.sub(r"#self_id", "%s" % f_id, s)

        if s.find("#ID") > -1 :
            f_id = self.get_short_id()
            s = re.sub(r"#ID", "%s" % f_id, s)

        s = s.lstrip('\n').rstrip('\n\t')
        if s == '' :
            return ''
        if line_leader > '' :
            result_s = '\n'
            for line in s.split('\n') :
                result_s += line_leader + line + '\n'
            return result_s + '\n'
        else :
            return '\n' + s + '\n\n'


def mess_dlg(mess, title = "NativeCAM"):
    dlg = gtk.MessageDialog(parent = None,
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        type = gtk.MESSAGE_WARNING,
        buttons = gtk.BUTTONS_OK, message_format = '%s' % mess)
    dlg.set_title(title)
    dlg.set_keep_above(True)
    dlg.run()
    dlg.destroy()


def get_translations(self, callback = None) :

    def get_menu_strings(path, f_name, trslatbl):
        for ptr in range(len(path)) :
            p = path[ptr]
            if p.tag.lower() == "group":
                name = p.get("name") if "name" in p.keys() else None
                if name is not None :
                    trslatbl.append((f_name, name))

                tooltip = p.get('tool_tip') if "tool_tip" in p.keys() else None
                if (tooltip is not None) and (tooltip != '') :
                    trslatbl.append((f_name, tooltip))

                get_menu_strings(p, f_name, trslatbl)

            elif p.tag.lower() == "sub":
                name = p.get("name") if "name" in p.keys() else None
                if name is not None :
                    trslatbl.append((f_name, name))

                tooltip = p.get('tool_tip') if "tool_tip" in p.keys() else None
                if (tooltip is not None) and (tooltip != '') :
                    trslatbl.append((f_name, tooltip))

    def get_strings():
        os.popen("xgettext --language=Python ./ncam.py -o ./ncam.po")
        os.popen("xgettext --language=Glade ./ncam.glade ./ncam_pref.glade -o ./glade.po")
        os.popen("sed --in-place ./*.po --expression=s/charset=CHARSET/charset=UTF-8/")
        os.popen("msgcat ./ncam.po ./glade.po -o ./locale/ncam.tmp_po")
        os.popen("rm ./ncam.po ./glade.po")

        # catalogs
        find = os.popen("find ./%s -name 'menu.xml'" % CATALOGS_DIR).read()
        for s in find.split() :
            translatable = []
            d, splitname = os.path.split(s)
            fname = s.lstrip('./')
            destname = './locale/' + splitname

            xml = etree.parse(s).getroot()
            get_menu_strings(xml, fname, translatable)

            out = []
            for i in translatable :
                out.append("#: %s" % i[0])
                out.append("_(%s)" % repr(i[1]))

            out = "\n".join(out)
            open(destname, "w").write(out)
            translatable = []
            os.popen("xgettext --language=Python --from-code=UTF-8 %s -o %s" % (destname, destname))
            os.popen("sed --in-place %s --expression=s/charset=CHARSET/charset=UTF-8/" % destname)
            os.popen("msgcat %s ./locale/ncam.tmp_po -o ./locale/ncam.tmp_po" % destname)
            os.popen("rm %s" % destname)

        # cfg files
        find = os.popen("find ./%s -name '*.cfg'" % CFG_DIR).read()
        print find
        for s in find.split() :
            translatable = []
            d, splitname = os.path.split(s)
            fname = s
            destname = './locale/' + splitname
            f = Feature(src = s)
            for i in ["name", "help"] :
                if i in f.attr :
                    translatable.append((fname, f.attr[i]))

            for p in f.param :
                for i in ["name", "help", "tool_tip", "options"] :
                    if i in p.attr :
                        translatable.append((fname, p.attr[i]))

            out = []
            for i in translatable :
                out.append("#: %s" % i[0])
                out.append("_(%s)" % repr(i[1]))

            out = "\n".join(out)
            open(destname, "w").write(out)

        cmd_line = "find ./locale/ -name '*.cfg'"
        find = os.popen(cmd_line).read()
        for s in find.split() :
            os.popen("xgettext --language=Python --from-code=UTF-8 %s -o %s" % (s, s))
            os.popen("sed --in-place %s --expression=s/charset=CHARSET/charset=UTF-8/" % s)
            os.popen("msgcat ./locale/ncam.tmp_po %s -o ./locale/ncam.tmp_po" % s)
            os.popen("rm %s" % s)

        if os.path.exists("./locale/ncam.po") :
            os.popen("msgcat ./locale/ncam.tmp_po ./locale/ncam.po -o ./locale/ncam.po")
            os.remove("./locale/ncam.tmp_po")
        else :
            os.rename("./locale/ncam.tmp_po", "./locale/ncam.po")

    try :
        get_strings()
        mess_dlg('Done !\nFile : ./locale/ncam.po')
    except Exception, detail :
        mess_dlg('Error while getting data for translation :\n\n%(detail)s' % \
                   {'detail':detail})
