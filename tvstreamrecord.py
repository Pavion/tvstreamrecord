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
from __future__ import division

from bottle import CherryPyServer # , TEMPLATES
from bottle import route, run, template, post, request, response
from bottle import static_file, redirect
from datetime import datetime, timedelta, time, date
from timezone import tDiff
from time import sleep
import subprocess
import config
from sql import sqlRun, sqlCreateAll, purgeDB
import grabber
import xmltv
import json
import sys
import shlex
import re
if sys.version_info[0] == 2:
    # Python 2.x
    import urllib as urllib32
    import urlparse
    tvcookie = b"tvstreamrecord_user"
else:
    # Python 3.x
    import urllib.request as urllib32
    import urllib.parse as urlparse
    tvcookie = "tvstreamrecord_user"
from threading import Thread, Timer
import os
from mylogging import logInit, logRenew, logStop
import hashlib
import codecs

def total(timedelta):
    try:
        return timedelta.total_seconds()
    except:
        return (timedelta.microseconds + (timedelta.seconds + timedelta.days * 24 * 3600) * 10**6) / 10**6

records = []
localdatetime = "%d.%m.%Y %H:%M:%S"
localtime = "%H:%M"
localdate = "%d.%m.%Y"
dayshown = datetime.combine(date.today(), time.min)
shutdown = False
version = '1.3.9'

@route('/live/<filename>')
def server_static9(filename):
    rows = sqlRun("SELECT * FROM channels WHERE cid=?", (filename.split(".")[0], ))
    if rows:
        write_m3u(rows[0][0], rows[0][1])
    else:
        return
    return static_file("/live.m3u", root='', mimetype='video')

def write_m3u(name, path):
    f = codecs.open("live.m3u", "w", "utf-8")
    f.write("#EXTM3U\n")
    f.write("#EXTINF:0,"+name+"\n")
    f.write(path+"\n")
    f.close()

@route('/channels.m3u')
def server_static8():
    return static_file("/channels.m3u", root='')
@route('/settings.db')
def server_static8():
    return static_file("/settings.db", root='', download="settings.db")
# Languages
@route('/lang/<filename>')
def server_static10(filename):
    return static_file(filename, root='./lang')
# Log file
@route('/log.txt')
def server_static7():
    return static_file("/log.txt", root='', download="log.txt")
# JavaScript
@route('/js/<filename>')
def server_static1(filename):
    return static_file(filename, root='./js')
@route('/js/i18n/<filename>')
def server_static11(filename):
    return static_file(filename, root='./js/i18n')
# CSS handling
@route('/css/<curstyle>/<filename>')
def server_static2(curstyle,filename):
    return static_file(filename, root='./css/'+curstyle)
@route('/css/<curstyle>/images/<filename>')
def server_static4(curstyle,filename):
    return static_file(filename, root='./css/'+curstyle+'/images')
@route('/css/<filename>')
def server_static3(filename):
    return static_file(filename, root='./css')
# Common images
@route('/images/<filename>')
def server_static5(filename):
    return static_file(filename, root='./images')

#------------------------------- Login script ------------------------------------

@post('/login')
def postLogin():
    global credentials
    pw = request.forms.pw.encode("utf-8")
    hash = hashlib.sha224(pw).hexdigest()
    if hash == credentials:
        config.clearIP(request.remote_addr)
    else:
        config.banIP(request.remote_addr)
    if not request.forms.store_pw:
        response.set_cookie(name=tvcookie, value=hash)
    else:
        response.set_cookie(name=tvcookie, value=hash, max_age=315360000)

    redirect("/")

@route('/logoff')
def postLogout():
    response.delete_cookie(tvcookie)
    if config.checkIP(request.remote_addr) == True:
        return template('login')

@post('/setpass')
def setPass():
    global credentials
    pass_old = hashlib.sha224(request.forms.pass_old).hexdigest() if request.forms.pass_old else ""
    pass_new_1 = hashlib.sha224(request.forms.pass_new_1).hexdigest() if request.forms.pass_new_1 else ""
    pass_new_2 = hashlib.sha224(request.forms.pass_new_2).hexdigest() if request.forms.pass_new_2 else ""
    if pass_old == credentials and pass_new_1 == pass_new_2:
        response.delete_cookie(tvcookie)
        credentials = config.setUser(pass_new_1)
        ret = 0
    elif pass_old != credentials:
        ret = 1
    else:
        ret = 2
    return json.dumps( {"ret": ret } )

def checkLogin():
    patterns = config.cfg_ip_filter.strip().split(',')
    localhost = False
    for pattern in patterns:
        if request.remote_addr.startswith(pattern) and not len(pattern.strip())==0:
            localhost = True
    global credentials
    if credentials and not localhost:
        if credentials != request.get_cookie(tvcookie):
            if config.checkIP(request.remote_addr) == True:
                return template('login')
            else:
                return "Sorry, your IP %s has been blacklisted for three unsuccessful login attempts" % request.remote_addr
    return ""

#------------------------------- Recurring records -------------------------------
def getWeekdays(mask):
    mask = 127 if mask == 0 else mask
    ret = list()
    for i in range(0, 7):
        ret.append( ( mask & pow(2,i) ) == pow(2,i)  )
    return ret

#------------------------------- Internalization -------------------------

#actlocal = ['mm/dd/yy', ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"], 0]
def checkLang():
    if not config.cfg_language == "english":
        ret_lng = ( fileexists("lang/tvstreamrecord." + config.cfg_language + ".json") and fileexists("lang/dataTables." + config.cfg_language + ".json") )
        if not ret_lng:
            config.cfg_language = "english"
            print ("Language not found, reverting to default language")
    else:
        ret_lng = True
    if not config.cfg_locale == "default":
        ret_loc = ( fileexists("js/i18n/jquery.ui.datepicker-" + config.cfg_locale + ".js") and fileexists("js/i18n/jquery-ui-timepicker-" + config.cfg_locale + ".js" ) )
        if not ret_loc:
            config.cfg_locale = "default"
            print ("Locale not found, reverting to default locale")
    else:
        ret_loc = True
    ret_style = ( fileexists("css/" + config.cfg_theme) )
    if not ret_style:
        config.cfg_theme = "smoothness/jquery-ui-1.10.4.custom.min.css"
        print ("Theme not found, reverting to default theme")
    if not (ret_loc and ret_lng and ret_style):
        config.saveConfig()

def internationalize(templ,noheader=False):
    login = checkLogin()
    if login != "":
        return login
    else:
        #TEMPLATES.clear() # debug only, should be turned off!
        if not noheader:
            header = template('header', style=config.cfg_theme, version=version, language=config.cfg_language, locale=config.cfg_locale, logout=(not credentials=="") )
            footer = template('footer')
            templ = header + templ + footer
        if not config.cfg_language == "english":
            try:
                json_data=open('lang/tvstreamrecord.' + config.cfg_language + '.json', "rb")
                data = json.loads(json_data.read().decode('utf-8'))
                json_data.close()
                for word in data:
                    if data[word]:
                        templ = templ.replace(u"§"+word+u"§", data[word])
            except:
                pass
        templ = templ.replace(u"§","")
        return templ

def fileexists(file):
    try:
        return os.path.isfile(file)
    except Exception as ex:
        return os.path.isfile(file.encode('utf-8').decode(sys.getfilesystemencoding()))

#------------------------------- Main menu -------------------------------

@route('/')
@route('/login')
def root_s():
    agent = request.headers.get('User-Agent')
    if ("Android" in agent and "Mobile" in agent) or "berry" in agent or "Symbian" in agent or "Nokia" in agent or "iPhone" in agent:
        count = sqlRun("select count(cid) from channels where cenabled=1")[0][0]
        if count > 0:
            redirect("/mobile")
        else:
            redirect("/records")
    else:
        redirect("/records")

@route('/about')
def about_s():
    changelog=""
    if fileexists("CHANGELOG"):
        f = codecs.open("CHANGELOG", "r", "utf-8")
        changelog = f.read()
        f.close()
    return internationalize(template('about', changelog=changelog))

#------------------------------- Logging -------------------------------

logInit('a')

print ("Starting tvstreamrecord v.%s with Python %s.%s" % (version, sys.version_info[0], sys.version_info[1]))
print ("Logging output initialized")

@post('/resetlog')
def log_reset():
    logRenew()
    return "null"

@route('/log')
def log_s():
    return internationalize(template('log'))

@route('/logget')
def log_get():
    l = list()
    lfile = codecs.open("log.txt", "r", "utf-8")
    for lline in lfile:
        if len(lline)>24:
            l.append([ lline[0:23], lline[24:] ])
    lfile.close()
    return json.dumps( {"aaData": l } )

#------------------------------- Channel List -------------------------------

@route('/channellist')
def chanlist():
    rows=sqlRun('SELECT channels.cid, cname, cpath, cext, epgscan, cenabled FROM channels')
    return json.dumps({"aaData": rows } )

@route('/list')
def list_s():
    return internationalize(template('list',rows2=sqlRun('SELECT cid, cname FROM channels where cenabled=1 ORDER BY cid')))

@post('/list')
def list_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-1":
        sqlRun("DELETE FROM channels WHERE cid=%s" % (myid))
        sqlRun("DELETE FROM records WHERE cid=%s" % (myid))
    else:
        sqlRun("UPDATE channels SET cenabled=%s WHERE cid=%s" % (what, myid))
        sqlRun("UPDATE records SET renabled=%s WHERE cid=%s" % (what, myid))
    setRecords()
    return "null"

#------------------------------- Channel creation -------------------------------

@post('/clgen')
def clgen_p():
    rows = sqlRun("select cid, cname, cpath from channels where cenabled=1 ORDER BY cid")
    if rows:
        f = codecs.open("channels.m3u", "w", "utf-8")
        f.write("#EXTM3U\n")
        for row in rows:
            f.write("#EXTINF:0,"+row[1]+"\n")
            f.write(row[2]+"\n")
        f.close()
    return "null"

@post('/grab_channel')
def grabchannel():
    myid = request.forms.myid
    sqlRun("UPDATE channels SET epgscan=-epgscan+1 WHERE cid = ?", (myid, ))
    return "null"

@post('/create_channel')
def createchannel():
    prev = request.forms.prev
    cid =  request.forms.ccid
    cname = request.forms.cname
    cpath = request.forms.cpath
    aktiv = getBool(request.forms.aktiv)
    epggrab = getBool(request.forms.epggrab)
    cext = request.forms.cext

    if prev=="":
        prev = -1
    elif prev.isdigit():
        prev = int(prev)
    else:
        print ("Wrong number found for the previous ID. Aborting creation/update.")
        return

    if cid=="":
        cid = 1
    elif cid.isdigit():
        cid = int(cid)
    else:
        print ("Wrong number found for the new ID. Aborting creation/update.")
        return

    if cext!='':
        if cext[0:1]!='.':
            cext = '.' + cext

    exists = False
    if cid == prev:
        exists = True
    else:
        rows3  = sqlRun("select cid from channels where cid=?", (cid, ))
        if rows3:
            exists = True

    if prev!=-1:
        if cid == prev:  # editing/renaming only
            sqlRun("UPDATE channels SET cname=?, cpath=?, cext=?, cenabled=?, epgscan=? WHERE cid=?", (cname, cpath, cext, aktiv, epggrab, cid))
        else: # also moving
            if exists:
                sqlRun("UPDATE channels SET cid = -1 WHERE cid = ?", (prev, ))
                sqlRun("UPDATE records  SET cid = -1 WHERE cid = ?", (prev, ))
                if prev > cid:
                    sqlRun("UPDATE channels SET cid = cid+1 WHERE cid >= %s AND cid < %s" % (cid, prev))
                    sqlRun("UPDATE records  SET cid = cid+1 WHERE cid >= %s AND cid < %s" % (cid, prev))
                else:
                    sqlRun("UPDATE channels SET cid = cid-1 WHERE cid > %s AND cid <= %s" % (prev, cid))
                    sqlRun("UPDATE records  SET cid = cid-1 WHERE cid > %s AND cid <= %s" % (prev, cid))
                sqlRun("UPDATE channels SET cname=?, cid=?, cpath=?, cext=?, cenabled=?, epgscan=? WHERE cid=-1", (cname, cid, cpath, cext, aktiv, epggrab))
                sqlRun("UPDATE records SET cid=? WHERE cid=-1", (cid, ))
            else:
                sqlRun("UPDATE channels SET cname=?, cid=?, cpath=?, cext=?, cenabled=?, epgscan=? WHERE cid=?", (cname, cid, cpath, cext, aktiv, epggrab, prev))
                sqlRun("UPDATE records SET cid=? WHERE cid=?", (cid, prev))
    else:
        if exists:
            sqlRun("UPDATE channels SET cid = cid+1 WHERE cid >= ?", (cid, ))
            sqlRun("UPDATE records SET cid = cid+1 WHERE cid >= ?", (cid, ))
        sqlRun("INSERT INTO channels VALUES (?, ?, ?, ?, ?, ?)", (cname, cpath, aktiv, cext, cid, epggrab))
    return "null"

@post('/upload')
def upload_p():
    print ("M3U upload parsing started")
    retl = []
    upfile = request.files.upfile
    if not upfile:
        print ("No file specified, please try again")
    else:
        content = upfile.file.read()
        try:
            content = content.decode("UTF-8")
        except:
            pass
        if "#EXTM3U" in content:
            how = getBool(request.forms.get("switch_list_append"))
            rowid = 1
            if how==0:
                sqlRun('DELETE FROM channels')
                sqlRun('DELETE FROM records')
                setRecords()
            else:
                rows2 = sqlRun("select max(cid) from channels")
                if rows2 and not rows2[0][0] is None:
                    rowid = rows2[0][0]+1

            lines = content.splitlines()
            i = 0
            name = ""
            for line in lines:
                if line != "" and not "#EXTVLCOPT" in line and not "#EXTM3U" in line:
                    i = i + 1
                    if i % 2 == 1:
                        name = line.split(",",1)[1]
                    if i % 2 == 0:
                        retl.append([name, line, rowid])
                        rowid = rowid + 1
                        name = ""
            sqlRun("INSERT OR IGNORE INTO channels VALUES (?, ?, '1', '', ?, 0)", retl, 1)
            print("M3U parsing completed with %d entries" % len(retl))
        else:
            print("Bad M3U format detected (missing #EXTM3U tag)")

    redirect("/list")

#------------------------------- Configuration -------------------------------

@post('/config')
def config_p():
    configdata = json.loads(request.forms.get('configdata'))
    for cfg in configdata:
        if cfg[0]=="cfg_grab_time":
            if cfg[1]!=config.cfg_grab_time:
                config.cfg_grab_time = cfg[1]
                grabthread.run()
    config.setConfig(configdata)
    return "null"

@route('/config')
def config_s():
    themes = list()
    for theme in os.listdir("css"):
        if os.path.isdir("css/"+theme) == True:
            for css in os.listdir("css/"+theme+"/"):
                if css.endswith(".css"):
                    themes.append([theme+'/'+css,theme])
                    break
    languages = list()
    languages.append("english")
    for langfile in os.listdir("lang"):
        if langfile.startswith("tvstreamrecord.") and langfile.endswith(".json"):
            lang = langfile[15:-5]
            if fileexists("lang/dataTables." + lang + ".json"):# and fileexists("js/i18n/jquery.ui.datepicker-" + lang[1] + ".js") and fileexists("js/i18n/jquery-ui-timepicker-" + lang[1] + ".js"):
                languages.append(lang)
    locales = list()
    locales.append("default")
    for locfile in os.listdir("js/i18n"):
        if locfile.startswith("jquery.ui.datepicker-") and locfile.endswith(".js"):
            locale = locfile[21:-3]
            if fileexists("js/i18n/jquery-ui-timepicker-" + locale + ".js"):
                locales.append(locale)
    return internationalize(template('config', themes=themes, languages=languages, locales=locales))

@route('/getconfig')
def getconfig():
    rows=sqlRun("SELECT param, '', value FROM config WHERE param<>'cfg_version' AND not param LIKE 'table_%'")
    return json.dumps({"configdata": rows } )

@post('/gettree')
def gettree():
    deny=['/etc', '/var', '/usr', '/sbin', '/bin', '/recycler']
    r=['<ul class="jqueryFileTree" style="display: none;">']
    try:
        d=urllib32.unquote(request.POST.get('dir','\\'))
        for f in os.listdir(d):
            ff=os.path.join(d,f)
            if os.path.isdir(ff) and not ff.lower() in deny and f[0] != '@':
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
                pass
    except:
        pass
    r.append('</ul>')
    return r

#------------------------------- EPG Grabbing part -------------------------------
class epggrabthread(Thread):
    stopflag = False
    running = False
    epggrabberstate = [0,0]
    timer = None

    def getState(self):
        return [self.running, self.epggrabberstate[0], self.epggrabberstate[1], self.stopflag]

    def isRunning(self):
        return self.running

    def setChannelCount(self):
        self.epggrabberstate[1] = 0
        if config.cfg_switch_grab_auto == "1":
            rows = sqlRun("SELECT count(cname) FROM channels WHERE epgscan = 1 AND cenabled = 1;")
            if rows:
                self.epggrabberstate[1] += rows[0][0]
        if config.cfg_switch_xmltv_auto=="1":
            self.epggrabberstate[1] += 1

    def __init__(self):
        self.setChannelCount()
        Thread.__init__(self)

    def kill(self):
        if not self.timer == None:
            self.timer.cancel()

    def run(self):
        self.kill()
        if not config.cfg_grab_time == '0' and len(config.cfg_grab_time)>=3:
            try:
                mytime = datetime.strptime(config.cfg_grab_time, "%H:%M").time()
                mydatetime = datetime.combine(datetime.now().date(), mytime)
                if mydatetime < datetime.now():
                    mydatetime = mydatetime + timedelta(days=1)
                td = tDiff(mydatetime,datetime.now())
                deltas = total(td)
                self.timer = Timer(deltas, self.doGrab)
                self.timer.start()
                if deltas>0:
                    print ("EPG Thread timer waiting till %s (%d seconds)" % (config.cfg_grab_time, deltas))
            except:
                print ("Something went wrong with EPG thread. Please check your config settings regarding your start time")

    def doGrab(self, override=False):
        self.kill()
        self.running = True
        if config.cfg_switch_grab_auto=="1"  and not self.stopflag: self.grabStream()
        if config.cfg_switch_xmltv_auto=="1" and not self.stopflag: self.grabXML()
        self.epggrabberstate[0]=0
        self.running = False
        if not override:
            sleep(61)
        self.stopflag = False
        self.run()

    def grabXML(self):
        if config.cfg_xmltv_mc2xml.strip() != "":
            try:
                mcargs = config.cfg_xmltv_mc2xml.strip().split()
                print ("mc2xml will be called with: %s" % (mcargs))
                mcproc = subprocess.Popen(mcargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = mcproc.communicate()
                if err:
                    print ("mc2xml ended with an error:\n%s" % (err))
                else:
                    print ("mc2xml ended without errors")
            except Exception as ex:
                print ("Error calling mc2xml: %s" % (ex))
                pass

        try:
            if xmltv.getProgList(version)>0:
                setRecords()
        except Exception as ex:
            print ("XMLTV import could not be completed, please try again later (%s)" % ex)
        self.epggrabberstate[0] += 1

    def grabStream(self):
        rows = sqlRun("SELECT cname, cpath FROM channels WHERE epgscan = 1 AND cenabled = 1;")
        for row in rows:
            if self.stopflag:
                break
            self.epggrabberstate[0] += 1
            fulllist = grabber.startgrab(row)
            sqllist = list()
            sqlchlist = list()
            prevname = ""
            actname = "dummy"
            cid = 0

            for l in fulllist:
                actname = l[0]
                if actname!=prevname:
                    rows2 = sqlRun("SELECT cid FROM channels WHERE cenabled = 1 AND lower(cname)=?", (actname.lower(), ))
                    if rows2:
                        cid = rows2[0][0]
                        sqlchlist.append([cid, actname, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") ] )
                    else:
                        cid = -1
                    prevname=actname

                if cid!=-1:
                    dt1 = l[1]
                    dt2 = l[1] + l[2]
                    pos = l[3].find("\n")
                    if pos!=-1:
                        title = l[3][0:pos]
                        desc = l[3][pos+1:]
                    else:
                        title = l[3]
                        desc = ""

                    sqllist.append([cid, title, datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S"), datetime.strftime(dt2, "%Y-%m-%d %H:%M:%S"), desc])

            if len(sqllist)>0:
                sqlRun("INSERT OR REPLACE INTO guide_chan VALUES (?, ?, ?)", sqlchlist, 1 )
                sqlRun("INSERT OR IGNORE INTO guide VALUES (?, ?, ?, ?, ?)", sqllist, 1)


    def stop(self):
        self.stopflag = True

@route('/getepgstate')
def getepgstate():
    return json.dumps( {"grabState": grabthread.getState() } )

@post('/grabepg')
def grabepg():
    mode = int(request.forms.mode)
    if not grabthread.isRunning():
        if mode == 0:
            doGrab = Thread(target=grabthread.doGrab, args=("True", ))
            doGrab.start()
    elif mode == 1:
        grabthread.stop()
    return "null"

#------------------------------- EPG painting part -------------------------------

@post('/removeepg')
def removeepg():
    sqlRun("DELETE FROM guide")
    sqlRun("DELETE FROM guide_chan")
    sqlRun("DELETE FROM caching")
    print ("All EPG data was deleted")
    return "null"

@post('/epg')
def epg_p():
    day = request.forms.datepicker_epg
    global dayshown
    dayshown = datetime.strptime(day,"%Y-%m-%d")
    return "null"

@post('/setzoom')
def zoom_p():
    zoom = request.forms.zoom
    config.cfg_grab_zoom = zoom
    config.saveConfig()
    return "null"

@route('/epgchart')
def epg_s():
    grabthread.setChannelCount()

    global dayshown

    if dayshown < datetime.combine(date.today(), time.min):
        dayshown = datetime.combine(date.today(), time.min)

    todaysql = datetime.strftime(dayshown, "%Y-%m-%d %H:%M:%S")
    weekbit = pow(2, int(datetime.strftime(dayshown, "%w")))
    # For handling overnight recurrent records from yesterday
    yesterday = dayshown - timedelta(days=1)
    weekbit_y = pow(2, int(datetime.strftime(yesterday, "%w")))
    yestersql = datetime.strftime(yesterday, "%Y-%m-%d %H:%M:%S")

    if dayshown == datetime.combine(date.today(), time.min): # really today
        sthour = datetime.now().time().hour
        daystart = datetime.combine(date.today(), time(sthour,0,0))
        totalwidth = 86400 - total(daystart - dayshown)
    else:
        sthour = 0
        daystart = dayshown
        totalwidth = 86400

    hours = int(totalwidth / 3600)
    d_von = daystart

    widthq = 1
    ret = list()
    rtemp = list()
    w = 0.0
    for i in range(0, hours):
        t = time(i+sthour)
        x = i * 100.0 / hours * widthq
        w =  1.0 / hours * widthq * 100.0
        rtemp.append([-1, x, w, t.strftime("%H:%M"), "", "", "", -1, "", 0])
    ret.append(rtemp)

    rows=sqlRun("SELECT guide.g_id, channels.cid, channels.cname FROM guide, guide_chan, channels WHERE channels.cenabled=1 AND channels.cname=guide_chan.g_name AND guide.g_id=guide_chan.g_id AND (date(g_start)=date(?) OR date(g_stop)=date(?)) GROUP BY channels.cid ORDER BY channels.cid", (todaysql, todaysql))
    if config.cfg_switch_epg_overlay == "1":
        # insert only channels with records but without guide data for using with overlay
        ol_rows = sqlRun("SELECT 'tvstreamrecord.service', channels.cid, channels.cname FROM channels JOIN records ON records.cid=channels.cid WHERE records.renabled=1 AND (date(records.rvon)=date(:1) OR date(records.rbis)=date(:1) OR records.rmask & :2 = :2 OR records.rmask & :3 = :3) AND channels.cenabled=1", (todaysql, weekbit, weekbit_y))
        for ol_row in ol_rows:
            found = False
            for row in rows:
                if row[1] == ol_row[1]:
                    found = True
                    break
            if not found:
                rows.append(ol_row)
    for row in rows:
        cid=row[1]
        rtemp = list()
        c_rows=sqlRun("SELECT g_title, g_start, g_stop, g_desc, guide.rowid, ((records.renabled is not null and records.renabled  = 1) OR (recurr.renabled is not null and recurr.renabled  = 1) OR (recurry.renabled is not null and recurry.renabled  = 1)) FROM guide " +
        "LEFT JOIN records ON records.cid=:1 AND guide.g_start>=records.rvon and guide.g_stop<=records.rbis " +
        "LEFT JOIN (" +
          "SELECT recname,cid, datetime(rvon, '+' || (julianday(date(:2)) - julianday(date(rvon))) || ' day') as rvon, datetime(rbis, '+' || (julianday(date(:2)) - julianday(date(rvon))) || ' day') as rbis, renabled, rmask, uniqueid FROM records WHERE records.rmask & :3 = :3 AND date(records.rvon)<date(:2) AND cid=:1" +
        ") AS recurr ON guide.g_start>=recurr.rvon and guide.g_stop<=recurr.rbis " +
        "LEFT JOIN (" +
          "SELECT recname,cid, datetime(rvon, '+' || (julianday(date(:4)) - julianday(date(rvon))) || ' day') as rvon, datetime(rbis, '+' || (julianday(date(:4)) - julianday(date(rvon))) || ' day') as rbis, renabled, rmask, uniqueid FROM records WHERE records.rmask & :5 = :5 AND date(rbis, '+' || (julianday(date(:4)) - julianday(date(rvon))) || ' day')=date(:2) AND cid=:1" +
        ") AS recurry ON guide.g_start>=recurry.rvon and guide.g_stop<=recurry.rbis " +
        "WHERE (date(g_start)=date(:2) OR date(g_stop)=date(:2)) AND datetime(g_stop, '+60 minutes')>datetime('now', 'localtime') AND g_id=:6 ORDER BY g_start", (cid, todaysql, weekbit, yestersql, weekbit_y, row[0]))
        if config.cfg_switch_epg_overlay == "1":
            # adding today records for overlay
            c_rows += sqlRun("SELECT '', records.rvon, records.rbis, '', -2, 0 FROM records WHERE records.cid=:1 AND (date(records.rvon)=date(:2) OR date(records.rbis)=date(:2)) AND renabled=1 ORDER BY rvon", (cid, todaysql))
            # adding recurrent records not yet scheduled
            c_rows += sqlRun("SELECT '', datetime(rvon, '+' || (julianday(:1) - julianday(date(rvon))) || ' day'), datetime(rbis, '+' || (julianday(:1) - julianday(date(rvon))) || ' day'), '', -2, 0 FROM records WHERE records.cid=:2 AND records.rmask & :3 = :3 AND records.renabled=1 AND date(records.rvon)<date(:1)", (todaysql, cid, weekbit))
            # adding overnight recurrent records
            c_rows += sqlRun("SELECT '', datetime(rvon, '+' || (julianday(:1) - julianday(date(rvon))) || ' day'), datetime(rbis, '+' || (julianday(:1) - julianday(date(rvon))) || ' day'), '', -2, 0 FROM records WHERE records.cid=:2 AND records.rmask & :3 = :3 AND records.renabled=1 AND date(rbis, '+' || (julianday(:1) - julianday(date(rvon))) || ' day')=date(:4)", (yestersql, cid, weekbit_y, todaysql))
        for event in c_rows:

            d_von = datetime.strptime(event[1],"%Y-%m-%d %H:%M:%S")
            d_bis = datetime.strptime(event[2],"%Y-%m-%d %H:%M:%S")

            if d_von < daystart:
                d_von = daystart
            if d_bis.date() > daystart.date():
                d_bis=datetime.combine(d_bis.date(),time.min)
            x = total(d_von - daystart)
            w = total(d_bis - d_von)

            # restoring dates for correct record times
            d_von = datetime.strptime(event[1],"%Y-%m-%d %H:%M:%S")
            d_bis = datetime.strptime(event[2],"%Y-%m-%d %H:%M:%S")

            if x >= 0 and w > 0:
                rtemp.append ([cid, x/totalwidth*100.0*widthq, w/totalwidth*100.0*widthq, event[0], d_von, d_bis, event[3], event[4], row[2], event[5]])
        ret.append(rtemp)
    return internationalize(template('epgchart', curr=datetime.strftime(dayshown, "%Y-%m-%d"), rowss=ret, zoom=config.cfg_grab_zoom, rows2=sqlRun('SELECT cid, cname FROM channels where cenabled=1 ORDER BY cid'), deltab=config.cfg_delta_before_epg, deltaa=config.cfg_delta_after_epg))

@route('/epglist')
@route('/epglist&<keyword>')
def epglist_s(keyword=''):
    return internationalize(template('epglist', keyword_for_epg=keyword, listmode=config.cfg_switch_epglist_mode, rows2=sqlRun('SELECT cid, cname FROM channels where cenabled=1 ORDER BY cid'), deltab=config.cfg_delta_before_epg, deltaa=config.cfg_delta_after_epg))

@route('/epglist_getter')
def epglist_getter():
    sEcho =  request.query.sEcho
    retlist = []
    totalrows = 0
    if sEcho: # Server-side processing
        columns = ['guide_chan.g_name', 'guide.g_title', 'guide.g_desc', 'guide.g_start', 'guide.g_stop']
        sLimit = "LIMIT %s OFFSET %s" % (request.query.iDisplayLength, request.query.iDisplayStart)
        iSortingCols = int(request.query.iSortingCols)
        sOrder = ""
        if iSortingCols:
            sOrder = "ORDER BY"
            col = int(request.query['iSortCol_0'])
            sOrder += " %s " % columns[col]
            sOrder += "ASC" if request.query['sSortDir_0']=="asc" else "DESC"
            if sOrder == "ORDER BY":
                sOrder = ""
        iSearch = request.query.sSearch
        sWhere = ""
        if iSearch and iSearch!="":
            sWhere = "AND (guide_chan.g_name LIKE '%" + iSearch + "%' OR guide.g_title LIKE '%" + iSearch + "%' OR guide.g_desc LIKE '%" + iSearch + "%')"

        query = "SELECT guide_chan.g_name, guide.g_title, guide.g_desc, guide.g_start, guide.g_stop, null, guide.rowid FROM guide INNER JOIN guide_chan ON guide.g_id = guide_chan.g_id INNER JOIN channels ON channels.cname=guide_chan.g_name WHERE datetime(guide.g_stop)>datetime('now', 'localtime') AND channels.cenabled<>0 %s %s %s" % (sWhere, sOrder, sLimit)
        countquery = "SELECT COUNT(guide.g_start) FROM guide INNER JOIN guide_chan ON guide.g_id = guide_chan.g_id INNER JOIN channels ON channels.cname=guide_chan.g_name WHERE datetime(guide.g_stop)>datetime('now', 'localtime') AND channels.cenabled<>0 %s" % (sWhere)
        count = sqlRun(countquery)
        if count:
            totalrows = count[0][0]

        rows=sqlRun(query)
    else: # Client-side processing
        rows=sqlRun("SELECT guide_chan.g_name, guide.g_title, guide.g_desc, guide.g_start, guide.g_stop, null, guide.rowid FROM guide INNER JOIN guide_chan ON guide.g_id = guide_chan.g_id INNER JOIN channels ON channels.cname=guide_chan.g_name WHERE datetime(guide.g_stop)>datetime('now', 'localtime') AND channels.cenabled<>0 ORDER BY g_start LIMIT %s;" % (config.cfg_epg_max_events))

    for row in rows:
        retlist.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    return json.dumps(
                      {"aaData": retlist,
                       "sEcho": sEcho,
                      "iTotalRecords": totalrows,
                       "iTotalDisplayRecords": totalrows
                       } )


# ------------------- Mobile version ----------------

def getLocale():
    if config.cfg_locale == "default":
        return None
    else:
        try:
            f = codecs.open("js/i18n/jquery.ui.datepicker-" + config.cfg_locale + ".js", "r", "utf-8")
            loc = f.read()
            f.close()
            p1 = loc.find("{")
            p1 = loc.find("{", p1+1)
            p2 = loc.find("}", p1+1)
            full = loc[p1+2:p2]
            f = codecs.open("js/i18n/jquery-ui-timepicker-" + config.cfg_locale + ".js", "r", "utf-8")
            loc = f.read()
            f.close()
            p1 = loc.find("{")
            p1 = loc.find("{", p1+1)
            p2 = loc.find("}", p1+1)
            full = full + "," + loc[p1+1:p2]
            #full = full.replace('\t', '').replace(',\n', ',"').replace(': ', '": ').replace('\n', '').replace("\"'",'"').replace("'",'"')
            full = full.replace('\t', '').replace(',\n', ',"').replace(': ', '": ').replace('\n', '').replace("\"'",'"').replace("'",'"')
            return '{"' + full + '}'
        except:
            print ("Error at parsing locales to JSON string")
            return None

@route('/mobile')
def records_s():
    return internationalize(template('mobile',locale=getLocale(), deltab=config.cfg_delta_before_epg, deltaa=config.cfg_delta_after_epg),True)

@route('/getchannelgroups')
def getchannelgroups():
    l = []
    sql = "case WHEN  substr(upper(cname), 1, 1)  >= 'A' AND  substr(upper(cname), 1, 1) <= 'Z' THEN  substr(upper(cname), 1, 1) ELSE '0' END"
    sql = "select " + sql + ", count(cname) from channels where cenabled=1 group by " + sql
    rows=sqlRun(sql)
    for row in rows:
        l.append([row[0], row[1]])
    return json.dumps({"aaData": l} )

@post('/getchannelgroup')
def getchannelgroup():
    l = []
    id = request.forms.get("id")
    sql = "select cid, cname from channels where cenabled=1 "
    if id=='-':
        sql = sql + "LIMIT 10"
    elif id=='0':
        sql = sql + "AND NOT (substr(upper(cname), 1, 1)  >= 'A' AND  substr(upper(cname), 1, 1) <= 'Z')"
    else:
        sql = sql + "AND substr(upper(cname), 1, 1)  = '" + id + "'"
    rows=sqlRun(sql)
    for row in rows:
        l.append([row[0], row[1]])
    return json.dumps({"aaData": l} )

@post('/getepgday')
def getepgday():
    cname = request.forms.get("cname")
    try:
        cname = cname.decode("utf-8")
    except:
        pass
    rdate = request.forms.get("rdate")
    rows=sqlRun("SELECT substr(g_title,1,50), g_start, substr(g_desc, 1, 100), g_stop FROM guide, guide_chan WHERE guide.g_id = guide_chan.g_id AND guide_chan.g_name=? AND (date(g_start)=date(?) OR date(g_stop)=date(?)) AND datetime(guide.g_stop)>datetime('now', 'localtime') ORDER BY g_start", (cname, rdate, rdate))
    if rows:
        return json.dumps({"aaData": rows} )
    else:
        return "null"

#------------------------------- Record List -------------------------------

@route('/getrecordlist')
def getrecordlist():
    l = []
    rows=sqlRun("SELECT recname, cname, rvon, rbis, rmask, renabled, 100*(strftime('%s','now', 'localtime')-strftime('%s',rvon)) / (strftime('%s',rbis)-strftime('%s',rvon)), records.rowid, rvon, rbis, channels.cid FROM channels, records where channels.cid=records.cid ORDER BY rvon")
    for row in rows:
        m3u = "<a href=\"live/" + str(row[10]) + ".m3u\">" + row[1] + "</a>"
        l.append([row[0], m3u, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])
    return json.dumps({"aaData": l} )

@route('/records')
def records_s():
    return internationalize(template('records', rows2=sqlRun('SELECT cid, cname FROM channels where cenabled=1 ORDER BY cid')))

@post('/records')
def records_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-2":
        sqlRun("DELETE FROM records WHERE datetime(rbis)<datetime('now', 'localtime') AND NOT rmask>0")
    if what=="-1":
        sqlRun("DELETE FROM records WHERE records.rowid=?", (myid, ))
    else:
        sqlRun("UPDATE records SET renabled=? WHERE rowid=?", (what, myid))
    setRecords()
    return "null"

#------------------------------- Record creation -------------------------------

@post('/createepg')
def createepg():
    sqlRun("INSERT OR IGNORE INTO records SELECT guide.g_title, channels.cid, datetime(guide.g_start, '-%s minutes'), datetime(guide.g_stop, '+%s minutes'), 1, 0, '' FROM guide, guide_chan, channels WHERE guide.g_id = guide_chan.g_id AND channels.cname = guide_chan.g_name AND guide.rowid=? GROUP BY datetime(guide.g_start, '-%s minutes')" % (config.cfg_delta_before_epg, config.cfg_delta_after_epg, config.cfg_delta_before_epg), (request.forms.ret, ))
    setRecords()
    redirect("/records")
    return "null"

@post('/createtvb')
def create_tvb():

    recname = request.forms.recname
    sender = request.forms.sender
    von = request.forms.von
    bis = request.forms.bis
    am = request.forms.am
    uniqueid = request.forms.uniqueid

    d_von = datetime.strptime(am + " " + von, "%Y-%m-%d %H:%M")
    d_bis = datetime.strptime(am + " " + bis, "%Y-%m-%d %H:%M")
    delta = timedelta(days=1)
    if d_bis < d_von:
        d_bis = d_bis + delta

    print ("POST request received from TV-Browser plugin")
    print ("Name: %s, channel: %s, start: %s, stop: %s" % (recname, sender, d_von, d_bis))
    rows=sqlRun("SELECT cid FROM channels WHERE cname=? AND cenabled=1", (sender, ))
    if rows:
        cid = rows[0][0]
        print ("Channel %s was found with CID %s, creating record" % (sender, cid))
        deltaepgbefore = timedelta(minutes=int(config.cfg_delta_before_epg))
        deltaepgafter = timedelta(minutes=int(config.cfg_delta_after_epg))
        d_von = d_von - deltaepgbefore
        d_bis = d_bis + deltaepgafter
        sqlRun("INSERT OR IGNORE INTO records VALUES (?, ?, ?, ?, 1, 0, ?)", (recname, cid, d_von, d_bis, uniqueid))
        setRecords()
        return "true"
    else:
        print ("Channel %s could not be found, please check your channel names" % (sender))
        return "false"

@route('/gettvb')
def gettvb():
    ret = ""
    rows=sqlRun("SELECT uniqueid FROM records WHERE uniqueid <> '' AND renabled=1")
    for row in rows:
        ret += row[0] + "\n"
    return ret.rstrip()

@post('/deletetvb')
def deletetvb():
    uniqueid = request.forms.uniqueid
    rows = sqlRun("SELECT * FROM records WHERE uniqueid = ?", (uniqueid, ))
    if len(rows) == 0:
        return "false"
    else:
        sqlRun("DELETE FROM records WHERE uniqueid = ?", (uniqueid, ))
        print ("TVB record '%s' has been deleted" % rows[0][0])
        setRecords()
        return "true"

@post('/create')
def create_p():
    prev = request.forms.prev
    recname = request.forms.recname
    sender = request.forms.Sender
    von = request.forms.von
    bis = request.forms.bis
    am = request.forms.am
    aktiv = getBool(request.forms.aktiv)
    recurr = request.forms.recurr

    d_von = datetime.strptime(am + " " + von, "%Y-%m-%d %H:%M")
    d_bis = datetime.strptime(am + " " + bis, "%Y-%m-%d %H:%M")
#    d_von = datetime.strptime(am + " " + von, "%d.%m.%Y %H:%M")
#    d_bis = datetime.strptime(am + " " + bis, "%d.%m.%Y %H:%M")
    delta = timedelta(days=1)
    if d_bis < d_von:
        d_bis = d_bis + delta

    if prev=="":
        sqlRun("INSERT OR IGNORE INTO records VALUES (?, ?, ?, ?, ?, ?, '')", (recname, sender, d_von, d_bis, aktiv, recurr))
    else:
        sqlRun("UPDATE records SET recname=?, cid=?, rvon=?, rbis=?, renabled=?, rmask=? WHERE rowid=?", (recname, sender, d_von, d_bis, aktiv, recurr,  prev))

    setRecords()

    return "null"

def getBool(stri):
    r = 0
    if stri == "on" or stri == "1" or stri == "delete" or stri==1:
        r = 1
    return r


class record(Thread):
    running = 0
    id = -1
    stopflag = 0
    timer = None
    name = ""
    mask = 0
    ext = ""
    process = None
    myrow = None
    retries = 0
    retry_count = 0
    ffmpeg = 0

    def __init__(self, row):
        Thread.__init__(self)
        self.id = row[0]
        self.von = datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S")
        self.bis = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")
        self.name = row[5]
        self.url = row[1].strip()
        self.mask = row[6]
        self.myrow = row
        if config.cfg_retry_count.isdigit():
            self.retry_count = int(config.cfg_retry_count)
        if row[7]=='':
            self.ext = config.cfg_file_extension
        else:
            self.ext = row[7]
        if self.mask > 0:
            w = self.von.isoweekday() if self.von.isoweekday()<7 else 0
            if not (self.von>=datetime.now() and getWeekdays(self.mask)[w]):
                delta = timedelta(days=1)
                while not (self.von>=datetime.now() and getWeekdays(self.mask)[w]):
                    self.von = self.von + delta
                    self.bis = self.bis + delta
                    w = self.von.isoweekday() if self.von.isoweekday()<7 else 0
                print ("Recurrent record '%s' moved to %s" % (self.name, self.von))
                sqlRun("UPDATE records SET rvon='%s', rbis='%s' WHERE rowid=%d" % (datetime.strftime(self.von,"%Y-%m-%d %H:%M:%S"), datetime.strftime(self.bis,"%Y-%m-%d %H:%M:%S"), self.id ) )

    def run(self):
        td = tDiff(self.von,datetime.now())
        deltas = total(td)
        self.timer = Timer(deltas, self.doRecord)
        self.timer.start()
        if deltas>0:
            print ("Record: Thread timer for '%s' started for %d seconds" % (self.name, deltas))

    def doRecord(self):
        self.running = 1

        fftypes = config.cfg_ffmpeg_types
        fftypes = fftypes.lower().split()
        streamtype = self.url.lower().split(':', 1)[0]
        ffargs = config.cfg_ffmpeg_params
        ffargs = ffargs.split()

        dateholder = datetime.now().strftime("%Y%m%d%H%M%S")
        titleholder = "".join([x if x.isalnum() else "_" for x in self.name])
        if sys.version_info[0] < 3 and streamtype in fftypes:
            # workaround for unicode, damn me if I ever get it working with 2.x
            titleholder = "".join([x if ord(x) < 128 else "_" for x in titleholder])
        idholder = "%04d" % (self.myrow[8], )

        fulltitle = self.name
        # remove/replace illegal chars
        safetitle = re.sub(r"[\?\:\{\}]", "", fulltitle)
        safetitle = re.sub(r"[\"]", "'", safetitle)
        safetitle = re.sub(r"[\&]", " ", safetitle)
        safetitle = re.sub(r"[\~\#\%\*\\\<\>\/\+\|]", "_", safetitle.rstrip())

        fn = config.cfg_record_mask
        # Placeholders
        fn = fn.replace("%date%", dateholder).replace("%title%", titleholder)
        fn = fn.replace("%month%", datetime.now().strftime("%m")).replace("%year%", datetime.now().strftime("%Y")).replace("%day%", datetime.now().strftime("%d"))
        fn = fn.replace("%hour%", datetime.now().strftime("%H")).replace("%minute%", datetime.now().strftime("%M")).replace("%second%", datetime.now().strftime("%S"))
        fn = fn.replace("%year2%", datetime.now().strftime("%y"))
        fn = fn.replace("%channelid%", idholder).replace("%channel%", self.myrow[9])
        if "%fulltitle%" in fn and sys.version_info[0] == 2 and os.name == "nt":
            print ("Usage of %fulltitle% is not possible on Python 2.7 and Windows. Please consider upgrading your Python.")
            fn = fn.replace("%fulltitle%", titleholder)
        else:
            fn = fn.replace("%fulltitle%", safetitle)
        # Placeholders end
        for i in range(0, len(ffargs)):
            ffargs[i] = ffargs[i].replace("%date%", dateholder).replace("%title%", titleholder)
            ffargs[i] = ffargs[i].replace("%month%", datetime.now().strftime("%m")).replace("%year%", datetime.now().strftime("%Y")).replace("%day%", datetime.now().strftime("%d"))
            ffargs[i] = ffargs[i].replace("%hour%", datetime.now().strftime("%H")).replace("%minute%", datetime.now().strftime("%M")).replace("%second%", datetime.now().strftime("%S"))
            ffargs[i] = ffargs[i].replace("%year2%", datetime.now().strftime("%y"))
            ffargs[i] = ffargs[i].replace("%channelid%", idholder).replace("%channel%", self.myrow[9])
            ffargs[i] = ffargs[i].replace("%fulltitle%", fulltitle)

        if "/" in fn or "\\" in fn:
            try:
                path = fn.replace('\\', "/")
                pos = path.rfind("/")
                path = path[:pos]
                path = config.cfg_recordpath + path
                os.makedirs (path)
            except Exception as ex:
                pass

        fn = config.cfg_recordpath + fn
        # Check, if destination file already exists
        fn_check = fn + self.ext
        num = 1
        while fileexists(fn_check) and num<127:
            fn_check = fn + ("_%s" % num) + self.ext
            num += 1
        fn = fn_check
        # End check
        if streamtype in fftypes:
            delta = total(tDiff(self.bis, datetime.now()))
            deltasec = '%d' % delta

            try:
                if config.cfg_ffmpeg_alternate_url != "":
                    for t in records:
                        if t.isRunning() == 1 and t.isFfmpeg() == 1:
                            parser = urlparse.urlsplit(self.url)
                            self.url = urlparse.urlunsplit([parser.scheme, config.cfg_ffmpeg_alternate_url, parser.path, parser.query, parser.fragment])
                            print ("FFMPEG record already in progress, substituting URL...")
                            self.ffmpeg = 2
                            break
            except:
                pass

            if self.ffmpeg == 0:
                self.ffmpeg = 1

            attr = [config.cfg_ffmpeg_path,"-i", self.url, '-y', '-t', deltasec] + ffargs + [fn]
            print ("FFMPEG (%s) record '%s' called with:" % (streamtype, self.name))
            print (attr)
            try:
                if config.cfg_switch_proxy == "1" and config.cfg_proxy != "":
                    os.environ["http_proxy"] = config.cfg_proxy
                else:
                    os.environ["http_proxy"] = ""
                self.process = subprocess.Popen(attr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cleaner = Timer(delta+30, self.cleanProcess) # if ffmpeg won't exit, try to terminate its process in 30 seconds
                cleaner.start()
                out, err = self.process.communicate()
                #self.process.wait() # oops... not needed? harmless!
                cleaner.cancel()
                if err:
                    print ("FFMPEG record '%s' ended with an error:\n%s" % (self.name, err))
                else:
                    print ("FFMPEG record '%s' ended" % self.name)
            except Exception as ex:
                print ("FFMPEG could not be started. Error: %s" % (ex))
        else:
            block_sz = 8192
            print ("Record: '%s' started" % (self.name))
            try:
                u = urllib32.urlopen(self.url)
                try:
                    f = open(fn, 'wb')
                except:
                    f = open(fn.encode('utf-8').decode(sys.getfilesystemencoding()), 'wb')
            #except urllib32.URLError:
            #    print ("Stream could not be parsed (URL=%s), aborting..." % (self.url))
            except ValueError as ex:
                print ("Unknown URL type (%s), record could not be started. Please check your channel settings" % (self.url))
            except Exception as ex:
                print ("Output file %s could not be created. Please check your settings. Description: %s" % (fn, ex))
            else:
                internalRetryCount = 0
                maxRetryCount = 100
                mybuffer = None
                while self.bis > datetime.now() and self.stopflag==0:
                    try:
                        mybuffer = u.read(block_sz)
                        doInternalRetry = False
                    except:
                        doInternalRetry = True
                    if (not mybuffer or doInternalRetry) and internalRetryCount < maxRetryCount: # connection lost?
                        internalRetryCount += 1
                        try:
                            u = urllib32.urlopen(self.url)
                            mybuffer = u.read(block_sz)
                            f.write(mybuffer)
                        except:
                            pass
                    elif internalRetryCount >= maxRetryCount:
                        print ("Record: '%s': too many internal retries, aborting..." % (self.name))
                        break
                    else:
                        f.write(mybuffer)

                f.close()
                if internalRetryCount > 0:
                    print ("Record: '%s' ended with %s internal retries, please check your connection stability" % (self.name, internalRetryCount))
                else:
                    print ("Record: '%s' ended" % (self.name))

        if config.cfg_switch_postprocess == "1" and config.cfg_postprocess != "":
            if fileexists(fn):
                attr = []
                attr = shlex.split(config.cfg_postprocess)
                for i in range(0, len(attr)):
                    attr[i] = attr[i].replace("%file%", fn)
                print ("Postprocessing will be called with following parameters:")
                print (attr)
                try:
                    postprocess = subprocess.Popen(attr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = postprocess.communicate()
                except:
                    print ("Exception calling postprocessing, please check your command line")

        # 2015-01-21 Fail & recurrency check
        if datetime.now() < self.bis - timedelta(seconds=int(config.cfg_failsafe_delta)) and self.stopflag==0:
            delta = total(tDiff(self.bis, datetime.now()))
            if self.retry_count == 0:
                print ("Something went wrong with '%s'. No retries configured, aborting..." % (self.name))
                sleep(delta)
            elif self.retries == self.retry_count:
                print ("Something went wrong with '%s'. Last retry reached, aborting..." % (self.name))
                sleep(delta)
            elif self.retries < self.retry_count:
                self.retries += 1
                print ("Something went wrong with '%s', retry %s/%s in 10 seconds" % (self.name, self.retries, self.retry_count))
                sleep(10)
                self.run()
                return

        self.clean()
        rectimer = Timer(10, setRecords)
        rectimer.start()

    def stop(self):
        if self.running==0:
            self.timer.cancel()
        self.stopflag = 1
        if not self.process==None:
            if self.process.poll()==None:
                self.process.terminate()
        self.clean()
        print ("Record: Stopflag for '%s' received" % (self.name))

    def clean(self):
        self.running = 0
        if self in records: records.remove(self)

    def cleanProcess(self):
        try:
            if not self.process==None:
                self.process.terminate()
            sleep(3)
            if not self.process==None:
                self.process.kill()
                print ("FFMPEG Record '%s' had to be killed. R.I.P." % self.name)
            else:
                print ("FFMPEG Record '%s' had to be terminated." % self.name)
        except:
            print ("FFMPEG Record '%s' termination error, process might be running" % self.name)
        if not self.process==None:
            print ("FFMPEG Record '%s': termination may have failed" % self.name)
        self.running = 0

    def isFfmpeg(self):
        return self.ffmpeg

    def isRunning(self):
        return self.running

def setRecords():
    if shutdown:
        return
    rows=sqlRun("SELECT records.rowid, cpath, rvon, rbis, cname, records.recname, records.rmask, channels.cext, channels.cid, channels.cname FROM channels, records where channels.cid=records.cid AND (datetime(rbis)>=datetime('now', 'localtime') OR rmask>0) AND renabled = 1 ORDER BY datetime(rvon)")
    for row in rows:
        chk = False
        for t in records:
            if t.id == row[0]:
                if t.myrow[1]!=row[1] or t.myrow[2]!=row[2] or t.myrow[3]!=row[3] or t.myrow[4]!=row[4] or t.myrow[5]!=row[5]  or t.myrow[6]!=row[6]  or t.myrow[7]!=row[7]:
                    t.stop()
                    chk = False
                else:
                    chk = True
                break
        if chk == False:
            thread = record(row)
            if config.cfg_switch_concurrent == "0":
                for t in records:
                    t.stop()
                sleep(1)
            thread.start()
            records.append(thread)

    for i in range(len(records)-1,-1,-1):
        t = records[i]
        chk = False
        for row in rows:
            if t.id == row[0]:
                chk = True
                break
        if chk == False:
            t.stop()

print ("Initializing database... ")
sqlCreateAll(version)
purgeDB()
print ("Initializing config...")
config.loadConfig()
credentials = config.getUser()
print ("Checking internationalization...")
checkLang()
print ("Initializing records...")
setRecords()
print ("Initializing EPG import thread...")
grabthread = epggrabthread()
grabthread.run()

print ("Starting server on: %s:%s" % (config.cfg_server_bind_address, config.cfg_server_port))
try:
    run(host=config.cfg_server_bind_address, port=config.cfg_server_port, server=CherryPyServer, quiet=True)
except Exception as ex:
    print ("Server exception. Default network settings will be used this time. Please log in using port 8030 and check your network settings.")
    print ("Starting server on: 0.0.0.0:8030")
    run(host="0.0.0.0", port=8030, server=CherryPyServer, quiet=True)

# Server is shutting down, all threads should be eliminated
shutdown = True
print ("Server aborted. Stopping all records before exiting...")
while len(records)>0:
    records[0].stop()

print ("Stopping EPG grab thread...")
grabthread.kill()

print ("tvstreamrecord v.%s: bye-bye" % version)
logStop()
