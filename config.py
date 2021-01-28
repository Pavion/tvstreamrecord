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

    @author: pavion
"""
from __future__ import print_function
from __future__ import unicode_literals

configuration = [
[
'cfg_xmltvinitpath',
'Initial path for an XMLTV-Import',
#'http://xmltv.spaetfruehstuecken.org/xmltv/datalist.xml.gz'
#'http://www.xmltvepg.nl/rytecxmltvskyde.gz'
'http://xmltv.xmltv.se/datalist.xml.gz'
],

[
'cfg_purgedelta',
'Purge database records older than [days]',
30
],

[
'cfg_delta_before_epg',
'Lenghten an EPG-record (delta before), [minutes]',
3
],

[
'cfg_delta_after_epg',
'Lenghten an EPG-record (delta after), [minutes]',
3
],

[
'cfg_recordpath',
'Path for your recordings',
'/volume1/common/'
],

[
'cfg_dbpath',
'full path to settings.db (read-only)',
'settings.db'
],

[
'cfg_server_bind_address',
'Server bind address (restart needed)',
'0.0.0.0'
],

[
'cfg_server_port',
'Server port (restart needed)',
8030
],

[
'cfg_file_extension',
"File extension for the recorded stream (default='.ts')",
'.ts'
],

[
'cfg_switch_concurrent',
"Enable concurrent records",
'1'
],

[
'cfg_ffmpeg_path',
'Full path to ffmpeg for other streams support',
'ffmpeg'
],

[
'cfg_switch_legacy',
"Use legacy recording method for http streams",
'0'
],

[
'cfg_ffmpeg_params',
"Additional output arguments for ffmpeg (default: '-acodec copy -vcodec copy')",
'-loglevel fatal -map 0 -c copy'
],

[
'cfg_ffmpeg_alternate_url',
"Alternative URL for a second device",
''
],

[
'cfg_grab_time',
"Time to perform daily EPG grab on all marked channels (hh:mm format, 24h based, default '0' for manual only)",
'0'
],

[
'cfg_grab_zoom',
"Zoom level for EPG view. Positive values for horizontal, negative for vertical view (default '1' for old style)",
'1'
],

[
'cfg_switch_epg_overlay',
"Toggle EPG overlay for recordings",
'1'
],

[
'cfg_switch_xmltv_auto',
"Automatic XMLTV-Import (default off)",
'0'
],

[
'cfg_switch_epglist_mode',
"EPG list mode",
'0'
],

[
'cfg_theme',
"UI theme",
'smoothness/jquery-ui.min.css'
],

[
'cfg_language',
"UI language",
'english'
],

[
'cfg_locale',
"UI locale",
'default'
],

[
'cfg_epg_max_events',
"Max events to be sent",
'5000'
],

[
'cfg_record_mask',
"Record name mask",
'%date% - %title%'
],

[
'cfg_xmltvtimeshift',
'Time shift for XMLTV data (in hours)',
'0'
],

[
'cfg_xmltv_mc2xml',
'mc2xml command line',
''
],

[
'cfg_epg_autorecord',
'Keywords for autorecord (comma separated)',
''
],

[
'cfg_retry_count',
'Retry count for failed records',
99
],

[
'cfg_switch_postprocess',
"Enables postprocessing",
'0'
],

[
'cfg_postprocess',
"Postprocessing",
'synoindex -a %file%'
],

[
'cfg_switch_proxy',
"Enables proxy",
'0'
],

[
'cfg_proxy',
"Proxy URL",
'http://127.0.0.1:8080'
],

[
'cfg_ip_filter',
"IP Filter",
'10.,127.,192.,localhost'
],

[
'cfg_failsafe_delta',
'Do not restart ffmpeg if that much seconds remains',
10
]

]

from sql import sqlRun
from datetime import datetime

for config in configuration:
    globals()[config[0]] = config[2]

def getUser():
    rows = sqlRun("SELECT value FROM config WHERE param='credentials'")
    if rows:
        return rows[0][0]
    else:
        return setUser("")

def setUser(userhash):
    sqlRun("UPDATE config SET value = ? WHERE param='credentials'", (userhash, ))
    return userhash

def banIP(ip):
    rows = sqlRun("SELECT trycount FROM blacklist WHERE ip=?", (ip, ))
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    if rows:
        sqlRun("UPDATE blacklist SET trycount=?, lasttry=? WHERE ip=?", (rows[0][0]+1, now, ip))
        if rows[0][0]+1==3:
            print ("IP %s has been blacklisted for for three unsuccessful login attempts" % ip)

    else:
        sqlRun("INSERT INTO blacklist VALUES (?, ?, ?)", (ip, 1, now) )

def clearIP(ip):
    sqlRun("DELETE FROM blacklist WHERE ip=?", (ip, ))

def checkIP(ip):
    sqlRun("DELETE FROM blacklist WHERE julianday('now', 'localtime')-julianday(lasttry)>=2;")
    rows = sqlRun("SELECT trycount FROM blacklist WHERE ip=?", (ip, ))
    if rows:
        if rows[0][0]>=3:
            return False
    return True

def getDict():
    ret = []
    for r in globals():
        if r[0:4] =='cfg_':
            ret.append(r)
    return ret

def loadConfig():
    sqlRun("INSERT OR IGNORE INTO config VALUES (?, ?, ?)",configuration,1)
    rows = sqlRun("SELECT param, value FROM config WHERE param<>'cfg_version'")
    setConfig(rows)
    return

def setConfig(attrlist = []):
    for attr in attrlist:
        if attr[0] in globals():
            if attr[0]=="cfg_recordpath":
                if attr[1][-1]!="/" and attr[1][-1]!="\\":
                    if "\\" in attr[1]:
                        attr=(attr[0], attr[1]+"\\")
                    else:
                        attr=(attr[0], attr[1]+"/")
            globals()[attr[0]] = attr[1]
    saveConfig()


def saveConfig():
    sql = ''
    for var in getDict():
        sql += "UPDATE config SET value='%s' WHERE param='%s';" % (globals()[var], var)
    sqlRun(sql, -1, 1)

# Port changes should also be written in the Synology Webman configuration
def writeWebman(port):
    try:
        webman = list()
        lfile = open("webman/config", "rb")
        for lline in lfile:
            webman.append(lline)
        lfile.close()
        lfile = open("webman/config", "wb")
        for lline in webman:
            pos = lline.find(b'"port":')
            if pos>0:
                lfile.write( lline[:pos+8] + b'"' + str(port).encode() + b'"\n')
            else:
                lfile.write(lline)
        lfile.close()
    except:
        pass
    try:
        webman = list()
        lfile = open("/var/packages/tvstreamrecord/INFO", "rt")
        for lline in lfile:
            webman.append(lline)
        lfile.close()
        lfile = open("/var/packages/tvstreamrecord/INFO", "wt")
        for lline in webman:
            if lline[:9] == "adminport":
                lline = "adminport=%s\n" % (port)
            lfile.write(lline)
        lfile.close()        
    except:
        pass
    print ("Port changes saved, new port: %s, please restart the software" % str(port))
    return

