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

import sys
from datetime import datetime

log = open("log.txt", "a", 0)
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
        self.terminal.write(message)        
        mylines = message.replace('\n', '')
        mylines = mylines.replace('\r', '')
        mylines = mylines.strip()
        mylines = mylines.encode("UTF-8", errors='replace')
        if mylines!="": 
            self.log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + self.typ + " " + mylines + "\n")
    
    
def logInit():        
    sys.stdout = Logger(log, "OUT")
    sys.stderr = Logger(log, "ERR")
    
def logRenew():
    global log
    sys.stdout = stdout_old 
    sys.stderr = stderr_old 
    log.close()
    log = open("log.txt", "w", 0)
    logInit()
    
def logPause():
    sys.stdout = stdout_old 
    sys.stderr = stderr_old 

def logResume():    
    logInit()
       
def logStop():
    global log
    log.close()
    