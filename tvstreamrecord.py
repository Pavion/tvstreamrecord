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

from bottle import CherryPyServer
from bottle import route, run, template, post, request
from bottle import static_file, redirect
from datetime import datetime, timedelta, time, date
from time import sleep
import subprocess
import config
from sql import sqlRun, sqlCreateAll, purgeDB
import grabber
import xmltv
import json
import urllib2
import threading 
import os
import sys
from mylogging import logInit, logRenew, logStop

records = []    
localdatetime = "%d.%m.%Y %H:%M:%S"
localtime = "%H:%M"
localdate = "%d.%m.%Y"
dayshown = datetime.combine(date.today(), time.min)
version = '0.6.0' 

@route('/live/<filename>')
def server_static9(filename):
    rows = sqlRun("SELECT * FROM channels WHERE cid=%s" % filename.split(".")[0])
    if rows:
        f = open("live.m3u", "w")
        f.write("#EXTM3U\n")
        f.write("#EXTINF:0,"+rows[0][0]+"\n")
        f.write(rows[0][1]+"\n")
        f.close()
        return static_file("/live.m3u", root='', mimetype='video')
    else:
        redirect("/epg")
@route('/channels.m3u')
def server_static8():
    return static_file("/channels.m3u", root='')
@route('/log.txt')
def server_static7():
    return static_file("/log.txt", root='', download="log.txt")
@route('/js/<filename>')
def server_static1(filename):
    return static_file(filename, root='./js')

#curstyle = "Aristo";


@route('/css/<curstyle>/<filename>')
def server_static2(curstyle,filename):
    return static_file(filename, root='./css/'+curstyle)
@route('/css/<curstyle>/images/<filename>')
def server_static4(curstyle,filename):
    return static_file(filename, root='./css/'+curstyle+'/images')

@route('/css/<filename>')
def server_static3(filename):
    return static_file(filename, root='./css')
@route('/images/<filename>')
def server_static5(filename):
    return static_file(filename, root='./images')

#------------------------------- Recurring records -------------------------------
weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
def getWeekdays(i):
    if i==0: i=127
    l = []
    s = bin(i)[2:]
    while len(s)<7: s = '0'+s
    s = s[::-1]    
    for c in s: l.append(c=='1')
    return l

#--------------------------------- Common --------------------------------

#@post('/savetable')
#def savetable():
#    myid = request.forms.get("myid")
#    mylen = request.forms.get("mylen")
#    sqlRun("INSERT OR REPLACE INTO config VALUES (?, '', ?)",['table_'+myid,mylen])
#    return
#
#def getListLength(myid):
#    mylen = 10
#    row = sqlRun("SELECT value FROM config WHERE param='table_%s'" % myid)
#    if row:
#        mylen = row[0][0]
#    return mylen

#------------------------------- Main menu -------------------------------

@route('/')
@route('/about')
def about_s():    
    return template('about', curstyle=config.cfg_theme, version=version)

#------------------------------- Logging -------------------------------
        

logInit()    

print "Starting tvstreamrecord v.%s" % version
print "Logging output initialized"

@post('/resetlog')
def log_reset():
    logRenew()
    return

@route('/log')
def log_s():
    return template('log', curstyle=config.cfg_theme, version=version)

@route('/logget')
def log_get():
    l = list()
    lfile = open("log.txt", "r")
    for lline in lfile:
        if len(lline)>24:
            l.append([ lline[0:19], lline[20:23], lline[24:] ])
    lfile.close()    
    return json.dumps( {"aaData": l } )

#------------------------------- Channel List -------------------------------

@route('/channellist')
def chanlist():
    l = []
    rows=sqlRun('SELECT channels.cid, cname, cpath, cext, epgscan, cenabled FROM channels')    
    for row in rows:
        m3u = "<a href=\"live/" + str(row[0]) + ".m3u\">" + row[1] + "</a>"
        l.append([row[0], m3u, row[2], row[3], row[4], row[5]])
    return json.dumps({"aaData": l } )

@route('/list')
def list_s():
    return template('list',rows2=sqlRun('SELECT cid, cname FROM channels where cenabled=1 ORDER BY cid'),curstyle=config.cfg_theme, version=version)
    
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
    return

#------------------------------- Channel creation -------------------------------

@post('/clgen')
def clgen_p():
    rows = sqlRun("select cid, cname, cpath from channels where cenabled=1 ORDER BY cid")
    if rows:
        f = open("channels.m3u", "w")
        f.write("#EXTM3U\n")
        for row in rows:
            f.write("#EXTINF:0,"+row[1]+"\n")
            f.write(row[2]+"\n")
        f.close()
    return

@post('/grab_channel')
def grabchannel():
    myid = request.forms.myid
    sqlRun("UPDATE channels SET epgscan=-epgscan+1 WHERE cid = %s" % myid)                
    return
    
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
        print "Wrong number found for the previous ID. Aborting creation/update."
        return

    if cid=="":
        cid = 1
    elif cid.isdigit():
        cid = int(cid)
    else:
        print "Wrong number found for the new ID. Aborting creation/update."
        return
        
    if cext!='': 
        if cext[0:1]<>'.': cext = '.' + cext
    
    exists = False
    if cid == prev:
        exists = True
    else:
        rows3  = sqlRun("select cid from channels where cid=%s" % cid)
        if rows3: 
            exists = True
    
    if prev!=-1:
        if cid == prev:  # editing/renaming only 
            sqlRun("UPDATE channels SET cname='%s', cpath='%s', cext='%s', cenabled=%s, epgscan=%s WHERE cid=%s" % (cname, cpath, cext, aktiv, epggrab, cid))
        else: # also moving
            if exists:
                sqlRun("UPDATE channels SET cid = -1 WHERE cid = %s" % (prev))
                sqlRun("UPDATE records  SET cid = -1 WHERE cid = %s" % (prev))            
                if prev > cid:          
                    sqlRun("UPDATE channels SET cid = cid+1 WHERE cid >= %s AND cid < %s" % (cid, prev))                
                    sqlRun("UPDATE records  SET cid = cid+1 WHERE cid >= %s AND cid < %s" % (cid, prev))            
                else:            
                    sqlRun("UPDATE channels SET cid = cid-1 WHERE cid > %s AND cid <= %s" % (prev, cid))
                    sqlRun("UPDATE records  SET cid = cid-1 WHERE cid > %s AND cid <= %s" % (prev, cid))
                sqlRun("UPDATE channels SET cname='%s', cid=%s, cpath='%s', cext='%s', cenabled=%s, epgscan=%s WHERE cid=-1" % (cname, cid, cpath, cext, aktiv, epggrab))
                sqlRun("UPDATE records SET cid=%s WHERE cid=-1" % cid)
            else:
                sqlRun("UPDATE channels SET cname='%s', cid=%s, cpath='%s', cext='%s', cenabled=%s, epgscan=%s WHERE cid=%s" % (cname, cid, cpath, cext, aktiv, epggrab, prev))                
                sqlRun("UPDATE records SET cid=%s WHERE cid=%s" % (cid, prev))            
    else:
        if exists:
            sqlRun("UPDATE channels SET cid = cid+1 WHERE cid >= %s" % cid)            
            sqlRun("UPDATE records SET cid = cid+1 WHERE cid >= %s" % cid)            
        sqlRun("INSERT INTO channels VALUES (?, ?, ?, ?, ?, ?)", (cname, cpath, aktiv, cext, cid, epggrab))
    return
    
@post('/upload')
def upload_p():
    print "M3U upload parsing started"
    retl = []
    upfile = request.files.upfile
    if not upfile:
        print "No file specified, please try again"
    else:    
        header = upfile.file.read(7)
        if header.startswith("#EXTM3U"):
            how = getBool(request.forms.get("switch03"))
            upfilecontent = upfile.file.read()        
            rowid = 1
            if how==0:
                sqlRun('DELETE FROM channels')
                sqlRun('DELETE FROM records')
                setRecords()
            else:
                rows2 = sqlRun("select max(cid) from channels")
                if rows2 and not rows2[0][0] is None:
                    rowid = rows2[0][0]+1
                
            lines = upfilecontent.splitlines()
            i = 0
            name = ""
            for line in lines:
                if not line[0:10] == "#EXTVLCOPT" and line!="":
                    i = i + 1
                    if i % 2 == 1: 
                        name = line.split(",",1)[1]
                    if i % 2 == 0:
                        retl.append([name, line, rowid])
                        rowid = rowid + 1 
                        name = ""
            sqlRun("INSERT OR IGNORE INTO channels VALUES (?, ?, '1', '', ?, 0)", retl, 1)             
            
    redirect("/list") 

#------------------------------- Configuration -------------------------------
    
@post('/config')
def config_p():    
    configdata = json.loads(request.forms.get('configdata'))
    config.setConfig(configdata)    
    grabthread.run()
    return

@route('/config')
def config_s():    
    themes = list()
    for theme in os.listdir("css"):
        if os.path.isdir("css/"+theme) == True:            
            for css in os.listdir("css/"+theme+"/"):
                if css.endswith(".css"):
                    themes.append([theme+'/'+css,theme])
                    break
    return template('config', curstyle=config.cfg_theme, version=version, themes=themes)

@route('/getconfig')
def getconfig():
    rows=sqlRun("SELECT param, '', value FROM config WHERE param<>'cfg_version' AND not param LIKE 'table_%'")
    return json.dumps({"configdata": rows } )    
    
#------------------------------- EPG Grabbing part -------------------------------

class epggrabthread(threading.Thread):
    stopflag = False
    running = False 
    epggrabberstate = [0,0]
    timer = None
    
    def getState(self):
        return [self.running, self.epggrabberstate[0], self.epggrabberstate[1]]
    
    def isRunning(self):
        return self.running
    
    def setChannelCount(self):
        self.epggrabberstate[1] = 0
        rows = sqlRun("SELECT count(cname) FROM channels WHERE epgscan = 1 AND cenabled = 1;")
        if rows:
            self.epggrabberstate[1] = rows[0][0]
        if config.cfg_switch_xmltv_auto=="1": self.epggrabberstate[1] += 1     
    
    def __init__(self):
        self.setChannelCount()
        threading.Thread.__init__(self)
    
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
                td = mydatetime-datetime.now()
                deltas = td.total_seconds()
                self.timer = threading.Timer(deltas, self.doIt)
                self.timer.start()
                if deltas>0:
                    print "EPG Thread timer waiting till %s (%d seconds)" % (config.cfg_grab_time, deltas)                        
            except:
                print "Something went wrong with EPG thread. Please check your config settings regarding your start time"
    
    def doIt(self):
        self.kill()
        self.running = True        
        if config.cfg_switch_grab_auto=="1" and not self.stopflag:  self.grabStream()
        if config.cfg_switch_xmltv_auto=="1" and not self.stopflag: self.grabXML()
        self.epggrabberstate[0]=0
        self.running = False
        sleep(61)        
        self.stopflag = False
        self.run()
        
    def grabXML(self):
        try:
            xmltv.getProgList(version)
        except:
            print "XMLTV import could not be completed, please try again later (%s)" % sys.exc_info()[0]
        self.epggrabberstate[0] += 1    
 
    def grabStream(self):
        rows = sqlRun("SELECT cname, cpath FROM channels WHERE epgscan = 1 AND cenabled = 1;")
        self.epggrabberstate[1] = len(rows)        
        for row in rows:
            if self.stopflag: 
                break
            self.epggrabberstate[0] = self.epggrabberstate[0] + 1
            fulllist = grabber.startgrab(row)
            sqllist = list()
            sqlchlist = list()
            prevname = ""
            actname = "dummy"
            cid = 0

            for l in fulllist:
                actname = l[0]
                if actname!=prevname:
                    rows2 = sqlRun("SELECT cid FROM channels WHERE cenabled = 1 AND cname='%s' OR lower(cname)='%s'" % (actname, actname.lower()) )
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
        
@post('/grabepg')
def grabepgstart():
    mode = int(request.forms.mode)
    if not grabthread.isRunning():
        if mode == 0:
            grabthread.grabStream()
        elif mode == 1:
            grabthread.stop()
        elif mode == 2:
            grabthread.grabXML()
    return 

#------------------------------- EPG painting part -------------------------------
        
@post('/removeepg')
def removeepg():    
    sqlRun("DELETE FROM guide")
    sqlRun("DELETE FROM guide_chan")
    print "All EPG data was deleted"
    return 

@post('/epg')
def epg_p():    
    day = request.forms.datepicker3
    global dayshown
    dayshown = datetime.strptime(day,localdate)
    redirect("/epg") 

@route('/epg')
def epg_s():    
    grabthread.setChannelCount()

    global dayshown
    
    if dayshown < datetime.combine(date.today(), time.min):
        dayshown = datetime.combine(date.today(), time.min)    
            
    todaysql = datetime.strftime(dayshown, "%Y-%m-%d %H:%M:%S")

    if dayshown == datetime.combine(date.today(), time.min): # really today
        sthour = datetime.now().time().hour
        daystart = datetime.combine(date.today(), time(sthour,0,0))
        totalwidth = 86400 - (daystart - dayshown).total_seconds()
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
        rtemp.append([-1, x, w, t.strftime("%H:%M"), "", "", -1, "", 0])
    ret.append(rtemp)    
    
    rows=sqlRun("SELECT guide.g_id, channels.cid, channels.cname FROM guide, guide_chan, channels WHERE channels.cenabled=1 AND channels.cname=guide_chan.g_name AND guide.g_id=guide_chan.g_id AND (date(g_start)=date('%s') OR date(g_stop)=date('%s')) GROUP BY channels.cid ORDER BY channels.cid" % (todaysql, todaysql))
    for row in rows:
        cid=row[1]
        rtemp = list()
        c_rows=sqlRun("SELECT g_title, g_start, g_stop, g_desc, guide.rowid, (records.renabled is not null and records.renabled  = 1) FROM guide LEFT JOIN records ON records.cid=%s AND datetime(guide.g_start, '-%s minutes')=records.rvon and datetime(guide.g_stop, '+%s minutes')=records.rbis WHERE (date(g_start)=date('%s') OR date(g_stop)=date('%s')) AND datetime(g_stop, '+60 minutes')>datetime('now', 'localtime') AND g_id='%s' ORDER BY g_start" % (cid, config.cfg_delta_for_epg, config.cfg_delta_for_epg, todaysql, todaysql, row[0]))
        #c_rows=sqlRun("SELECT g_title, g_start, g_stop, g_desc, guide.rowid FROM guide WHERE (date(g_start)=date('%s') OR date(g_stop)=date('%s')) AND g_id='%s' ORDER BY g_start" % (todaysql, todaysql, row[0]))
        for event in c_rows:
            
            d_von = datetime.strptime(event[1],"%Y-%m-%d %H:%M:%S")
            d_bis = datetime.strptime(event[2],"%Y-%m-%d %H:%M:%S")
            fulltext = "<b>"+event[0]+": "+datetime.strftime(d_von, localtime) + " - " + datetime.strftime(d_bis, localtime) + "</b><BR><BR>"+event[3]
#            fulltext = fulltext.replace(chr(138), "").replace(chr(0xE4),"").replace(chr(0xF6),"").replace(chr(0xFC),"")
            title = fulltext
            if len(title)>300:
                title = title[:297]+"..."
                try:
                    title.decode("UTF-8")
                except:
                    title = title[:296]+"..."
                    title = ""
                    fulltext = ""
                    pass


            #print d_von, d_bis
            if d_von < daystart:
                d_von = daystart
            if d_bis.date() > daystart.date():
                d_bis=datetime.combine(d_bis.date(),time.min)
            x = d_von - daystart#datetime.combine(d_von.date(),time.min)
            w = d_bis - d_von
            if x.total_seconds()>=0 and w.total_seconds()>0:
                rtemp.append ([cid, x.total_seconds()/totalwidth*100.0*widthq, w.total_seconds()/totalwidth*100.0*widthq, event[0], title, fulltext, event[4], row[2], event[5]])
                #print event[5]
        ret.append(rtemp)
    return template('epg', curr=datetime.strftime(d_von, localdate), rowss=ret, grabstate=grabthread.getState(), zoom=config.cfg_grab_zoom, curstyle=config.cfg_theme, version=version)            

@route('/epglist')
def epglist_s():    
    return template('epglist', grabstate=grabthread.getState(), listmode=config.cfg_switch_epglist_mode, curstyle=config.cfg_theme, version=version)
    
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
            
        query = "SELECT guide_chan.g_name, guide.g_title, guide.g_desc, guide.g_start, guide.g_stop, (records.renabled is not null and records.renabled  = 1), guide.rowid FROM ((guide INNER JOIN guide_chan ON guide.g_id = guide_chan.g_id) INNER JOIN channels ON channels.cname=guide_chan.g_name) LEFT JOIN records ON records.cid=channels.cid AND datetime(guide.g_start, '-%s minutes')=records.rvon and datetime(guide.g_stop, '+%s minutes')=records.rbis WHERE datetime(guide.g_stop)>datetime('now', 'localtime') AND channels.cenabled<>0 %s %s %s" % (config.cfg_delta_for_epg, config.cfg_delta_for_epg, sWhere, sOrder, sLimit)
        countquery = "SELECT COUNT(guide.g_start) FROM ((guide INNER JOIN guide_chan ON guide.g_id = guide_chan.g_id) INNER JOIN channels ON channels.cname=guide_chan.g_name) LEFT JOIN records ON records.cid=channels.cid AND datetime(guide.g_start, '-%s minutes')=records.rvon and datetime(guide.g_stop, '+%s minutes')=records.rbis WHERE datetime(guide.g_stop)>datetime('now', 'localtime') AND channels.cenabled<>0 %s" % (config.cfg_delta_for_epg, config.cfg_delta_for_epg, sWhere)
        count = sqlRun(countquery)
        if count:
            totalrows = count[0][0]
        
        rows=sqlRun(query)
    else: # Client-side processing
        rows=sqlRun("SELECT guide_chan.g_name, guide.g_title, guide.g_desc, guide.g_start, guide.g_stop, (records.renabled is not null and records.renabled  = 1), guide.rowid FROM ((guide INNER JOIN guide_chan ON guide.g_id = guide_chan.g_id) INNER JOIN channels ON channels.cname=guide_chan.g_name) LEFT JOIN records ON records.cid=channels.cid AND datetime(guide.g_start, '-%s minutes')=records.rvon and datetime(guide.g_stop, '+%s minutes')=records.rbis WHERE datetime(guide.g_stop)>datetime('now', 'localtime') AND channels.cenabled<>0 ORDER BY g_start" % (config.cfg_delta_for_epg, config.cfg_delta_for_epg))    

    for row in rows:
        retlist.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], ""])
    return json.dumps(
                      {"aaData": retlist, 
                       "sEcho": sEcho,
                       "iTotalRecords": totalrows,
                       "iTotalDisplayRecords": totalrows 
                       } )

#------------------------------- Record List -------------------------------

@route('/getrecordlist')
def getrecordlist():
    l = []
    rows=sqlRun("SELECT recname, cname, strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rvon), strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rbis), rmask, renabled, 100*(strftime('%s','now', 'localtime')-strftime('%s',rvon)) / (strftime('%s',rbis)-strftime('%s',rvon)), records.rowid, rvon, rbis, channels.cid FROM channels, records where channels.cid=records.cid ORDER BY rvon")     
    for row in rows:
        rec = ""
        if row[4]==0: 
            rec = "no"
        else: 
            wd = getWeekdays(row[4])
            for index, item in enumerate(wd): 
                if item: 
                    rec += weekdays[index]
        m3u = "<a href=\"live/" + str(row[10]) + ".m3u\">" + row[1] + "</a>"
        l.append([row[0], m3u, row[2], row[3], rec, row[5], row[6], row[7], row[8], row[9]])
    return json.dumps({"aaData": l} )

@route('/records')
def records_s():    
    return template('records', rows2=sqlRun('SELECT cid, cname FROM channels where cenabled=1 ORDER BY cid'), curstyle=config.cfg_theme, version=version)

@post('/records')
def records_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-2":
        sqlRun("DELETE FROM records WHERE datetime(rbis)<datetime('now', 'localtime') AND NOT rmask>0")
    if what=="-1":
        sqlRun("DELETE FROM records WHERE records.rowid=%s" % (myid))
    else: 
        sqlRun("UPDATE records SET renabled=%s WHERE rowid=%s" % (what, myid))            
    setRecords()
    return

#------------------------------- Record creation -------------------------------
    
@post('/createepg')
def createepg():
    sqlRun("INSERT INTO records SELECT guide.g_title, channels.cid, datetime(guide.g_start, '-%s minutes'), datetime(guide.g_stop, '+%s minutes'), 1, 0 FROM guide, guide_chan, channels WHERE guide.g_id = guide_chan.g_id AND channels.cname = guide_chan.g_name AND guide.rowid=%s GROUP BY datetime(guide.g_start, '-%s minutes')" % (config.cfg_delta_for_epg, config.cfg_delta_for_epg, request.forms.ret, config.cfg_delta_for_epg))
    setRecords()        
    redirect("/records")
    return 

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

    d_von = datetime.strptime(am + " " + von, "%d.%m.%Y %H:%M")
    d_bis = datetime.strptime(am + " " + bis, "%d.%m.%Y %H:%M")
    delta = timedelta(days=1)
    if d_bis < d_von:
        d_bis = d_bis + delta         

    if prev=="":        
        sqlRun("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)", (recname, sender, d_von, d_bis, aktiv, recurr))
    else:    
        sqlRun("UPDATE records SET recname='%s', cid=%s, rvon='%s', rbis='%s', renabled=%s, rmask=%s WHERE rowid=%s" % (recname, sender, d_von, d_bis, aktiv, recurr,  prev))
    
    setRecords()
    
    return 
   
def getBool(stri):
    r = 0
    if stri == "on" or stri == "1" or stri == "delete" or stri==1:
        r = 1
    return r

    
class record(threading.Thread):
    running = 0
    id = -1
    stopflag = 0 
    timer = None
    name = ""
    mask = 0
    ext = ""
    process = None
    myrow = None
        
    def __init__(self, row):
        threading.Thread.__init__(self)
        self.id = row[0]
        self.von = datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S")
        self.bis = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")        
        self.name = row[5]        
        self.url = row[1].strip()
        self.mask = row[6]
        self.myrow = row
        if row[7]=='':
            self.ext = config.cfg_file_extension
        else:
            self.ext = row[7]
        if self.mask > 0:
            w = self.bis.weekday()
            if not (self.bis>=datetime.now() and getWeekdays(self.mask)[w]):
                delta = timedelta(days=1)
                while not (self.bis>=datetime.now() and getWeekdays(self.mask)[w]):
                    self.von = self.von + delta
                    self.bis = self.bis + delta
                    w = self.bis.weekday()    
                print "Recurrent record '%s' moved to %s" % (self.name, self.von)
                sqlRun("UPDATE records SET rvon='%s', rbis='%s' WHERE rowid=%d" % (datetime.strftime(self.von,"%Y-%m-%d %H:%M:%S"), datetime.strftime(self.bis,"%Y-%m-%d %H:%M:%S"), self.id ) )    
    
    def run(self): 
        td = self.von-datetime.now()
        deltas = td.total_seconds()
        self.timer = threading.Timer(deltas, self.doIt)
        self.timer.start()
        if deltas>0:
            print "Record: Thread timer for '%s' started for %d seconds" % (self.name, deltas)
        
    def doIt(self):
        self.running = 1
        fn = config.cfg_recordpath+datetime.now().strftime("%Y%m%d%H%M%S") + " - "        
        fn = fn + "".join([x if x.isalnum() else "_" for x in self.name])
        fn = fn + self.ext
        fftypes = config.cfg_ffmpeg_types
        fftypes = fftypes.lower().split()
        streamtype = self.url.lower().split(':', 1)[0]
        ffargs = config.cfg_ffmpeg_params
        ffargs = ffargs.split()
        if streamtype in fftypes: 
            delta = self.bis - datetime.now()
            deltasec = '%d' % delta.total_seconds()
            attr = [config.cfg_ffmpeg_path,"-i", self.url, '-y', '-loglevel', 'error', '-t', deltasec] + ffargs + [fn] 
            print "FFMPEG (%s) record '%s' called with:" % (streamtype, self.name)
            print attr
            try:
                self.process = subprocess.Popen(attr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = self.process.communicate()
                self.process.wait()
                #errpos = 0
                if err:
                    print "FFMPEG record '%s' ended with an error:\n%s" % (self.name, err)
                else:
                    print "FFMPEG record '%s' ended" % self.name
#                    errpos = err.lower().rfind("error")
#                    if errpos > 0:
#                        i = err.rfind("\n", 0, errpos)+1
#                print err#[i:]
#            print "FFMPEG record '%s' ended%" % (self.name, (" with an error:%s\n" % err) if err else "")
            except:
                print "FFMPEG could not be started"
        else:        
            block_sz = 8192
            print "Record: '%s' started" % (self.name)
            try:
                u = urllib2.urlopen(self.url)
                f = open(fn, 'wb')
            except urllib2.URLError:
                print "Stream could not be parsed (URL=%s), aborting..." % (self.url)  
                pass
            except:
                print "Output file %s could not be created. Please check your settings." % (fn+".mkv")  
                pass
            else:
                while self.bis > datetime.now() and self.stopflag==0:
                    mybuffer = u.read(block_sz)
                    if not mybuffer:
                        break
                    f.write(mybuffer)
                f.close()
                print "Record: '%s' ended" % (self.name)
                if self in records: records.remove(self) 
        if self.mask > 0:
            rectimer = threading.Timer(5, setRecords)
            rectimer.start()
    
    def stop(self):
        if self.running==0:
            self.timer.cancel()
        self.stopflag = 1
        if not self.process==None:
            if self.process.poll()==None:            
                self.process.terminate()
        if self in records: records.remove(self)
        print "Record: Stopflag for '%s' received" % (self.name)
   
def setRecords():
    rows=sqlRun("SELECT records.rowid, cpath, rvon, rbis, cname, records.recname, records.rmask, channels.cext FROM channels, records where channels.cid=records.cid AND (datetime(rbis)>=datetime('now', 'localtime') OR rmask>0) AND renabled = 1 ORDER BY datetime(rvon)")
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
           
print "Initializing database..."
sqlCreateAll(version)
purgeDB()          
print "Initializing config..."
config.loadConfig()
print "Initializing records..."
setRecords()
print "Initializing EPG import thread..."
grabthread = epggrabthread()
grabthread.run()
    
print "Starting server on: %s:%s" % (config.cfg_server_bind_address, config.cfg_server_port)
run(host=config.cfg_server_bind_address, port=config.cfg_server_port, server=CherryPyServer, quiet=True)


print "Server aborted. Stopping all records before exiting..."
for t in records:
    t.stop()

print "Stopping EPG grab thread..."    
grabthread.kill()
    
print "tvstreamrecord v.%s: bye-bye" % version
logStop()