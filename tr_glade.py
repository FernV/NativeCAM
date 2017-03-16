#!/usr/bin/env python
# coding: utf-8
'''
Created on 2017-03-13

@author: Fernand Veilleux <fernveilleux@gmail.com>

This translates glade files as string
for testing language files before installation.

Export these values :
NATIVECAM_LOCALE=path_to_ncam_locale
LANGUAGE=2_characters_language_code

then run NativeCAM standalone in same terminal
'''

import gtk
import sys, os
import re
import pygtk
pygtk.require('2.0')

def translate(fstring):
    # translate the file
    txt2 = fstring.split('\n')
    fstring = ''
    for line in txt2 :
        inx = line.find('translatable="yes">')
        if inx > -1 :
            inx2 = line.find('</')
            txt = line[inx + 19:inx2]
            line = re.sub(r'%s' % txt, '%s' % _(txt), line)
        fstring += line + '\n'
    return fstring
