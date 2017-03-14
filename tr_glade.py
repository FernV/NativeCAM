'''
Created on 2017-03-13

@author: fernand

This translate glade files for treting before installation
export these values :
NATIVECAM_LOCALE=path_to_ncam_locale
LANGUAGE=2_characters_language_code
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
#            ttxt = _(txt)
            line = re.sub(r'%s' % txt, '%s' % _(txt), line)
        fstring += line + '\n'

    return fstring

# if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
#    exit translate('')
