# coding=UTF-8
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: Pavion
"""
from __future__ import print_function
from __future__ import unicode_literals

import sys
import codecs
from datetime import datetime

log = None
stdout_old = sys.stdout
stderr_old = sys.stderr

class Logger(object):
    msg = ''
    def __init__(self, logfile, typ):
        self.typ = typ
        self.log = logfile
        if typ == "OUT":
            self.terminal = sys.stdout
        else:
            self.terminal = sys.stderr

    def write(self, message):
        try:
            self.terminal.write(message)
        except:
            pass
        mylines = message.replace('\n', '')
        mylines = mylines.replace('\r', '')
        mylines = mylines.strip()
        if mylines!=u"":
            ms = '{:03d}'.format( int(datetime.now().microsecond / 1000) )                
            self.log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "." + ms + " " + mylines + "\n")

    def flush(self):
        pass


def logInit(filemode):
    global log
    log = codecs.open("log.txt", encoding='utf-8', mode=filemode, buffering=0)
    sys.stdout = Logger(log, "OUT")
    sys.stderr = Logger(log, "ERR")

def logRenew():
    logStop()
    logInit('w')

#def logPause():

#def logResume():
#    logInit()

def logStop():
    global log, stdout_old, stderr_old
    sys.stdout = stdout_old
    sys.stderr = stderr_old
    log.close()
