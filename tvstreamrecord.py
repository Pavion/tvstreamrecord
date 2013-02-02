# coding=UTF-8
from bottle import route, run, template, post, request
from bottle import static_file, redirect
from datetime import datetime, timedelta, time, date
import config
from sql import sqlRun, sqlCreateAll, purgeDB
import xmltv
import json
import urllib2
import threading 

records = []    
localdatetime = "%d.%m.%Y %H:%M:%S"
localtime = "%H:%M"
localdate = "%d.%m.%Y"
dayshown = datetime.combine(date.today(), time.min) 

@route('/js/<filename>')
def server_static1(filename):
    return static_file(filename, root='./js')
@route('/css/smoothness/<filename>')
def server_static2(filename):
    return static_file(filename, root='./css/smoothness')
@route('/css/images/<filename>')
def server_static6(filename):
    return static_file(filename, root='./css/images')
@route('/css/<filename>')
def server_static3(filename):
    return static_file(filename, root='./css')
@route('/css/smoothness/images/<filename>')
def server_static4(filename):
    return static_file(filename, root='./css/smoothness/images')
@route('/images/<filename>')
def server_static5(filename):
    return static_file(filename, root='./images')

#------------------------------- Channel List -------------------------------

@route('/channellist')
def chanlist():
    l = []
    rows=sqlRun('SELECT channels.rowid, cname, cpath, cenabled FROM channels')    
    for row in rows:
        l.append([row[0], row[1], row[2], row[3]])
    return json.dumps({"aaData": l } )

@route('/list')
def list_s():
    return template('list')
    
@post('/list')
def list_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    print what, myid
    if what=="-1":
        sqlRun("DELETE FROM channels WHERE channels.rowid=%s" % (myid))
    else: 
        sqlRun("UPDATE channels SET cenabled=%s WHERE channels.rowid=%s" % (what, myid))            
    setRecords()
    return

#------------------------------- Configuration -------------------------------
    
@post('/config')
def config_p():    
    attrl = []
    dicts = config.getDict()
    for d in dicts:
        print d
        print request.forms.get(d)        
        print "******************"
        val = request.forms.get(d)
        attrl.append([d, val])
    config.setConfig(attrl)
    redirect("/config") 

@route('/config')
def config_s():    
    return template('config', rows=sqlRun('SELECT * FROM config'))

@post('/create_channel')
def createchannel():
    cname = request.forms.cname
    cpath = request.forms.cpath
    aktiv = getBool(request.forms.aktiv)
    sqlRun("INSERT INTO channels VALUES (?, ?, ?)", (cname, cpath, aktiv))
    return
    
@route('/')
def main():
    return template('header', rows = None)

@post('/getepg')
def getepg():
    thread = epgthread() 
    thread.start()
    return 

class epgthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        xmltv.getProgList()



@post('/upload')
def upload_p():
    print "upload started"
    retl = []
    upfile = request.files.upfile
    header = upfile.file.read(7)
    if header.startswith("#EXTM3U"):
        how = getBool(request.forms.get("switch00"))
        upfilecontent = upfile.file.read()        
        if how==0:
            sqlRun('DELETE FROM channels')
        lines = upfilecontent.splitlines()
        i = 0
        name = ""
        for line in lines:
            print line
            i = i + 1
            if i>1:
                if i % 2 == 0: 
                    name = line.split(",",1)[1]
                if i % 2 == 1:
                    retl.append([name, line]) 
                    name = ""
        sqlRun("INSERT OR IGNORE INTO channels VALUES (?, ?, '1')", retl, 1)             
            
    redirect("/list") 

#------------------------------- EPG -------------------------------
    
@post('/epg')
def epg_p():    
    day = request.forms.datepicker3
    global dayshown
    dayshown = datetime.strptime(day,localdate)
    redirect("/epg") 

@route('/epg')
def epg_s():    
    widthq = 0.8
    ret = list()
    rtemp = list()
    w = 0.0
    for i in range(24):
        t = time(i)
        x = i * 100.0 / 24.0 * widthq
        w =  1.0 / 24.0 * widthq * 100.0 
        rtemp.append([-1, x, w, t.strftime("%H:%M"), "", "", -1, ""])
    ret.append(rtemp)    
    
    global dayshown    
    todaysql = datetime.strftime(dayshown, "%Y-%m-%d %H:%M:%S")
    d_von = dayshown    
    rows=sqlRun("SELECT guide.g_id, channels.rowid, channels.cname FROM guide, guide_chan, channels WHERE channels.cenabled=1 AND channels.cname=guide_chan.g_name AND guide.g_id=guide_chan.g_id AND (date(g_start)=date('%s') OR date(g_stop)=date('%s')) GROUP BY guide.g_id" % (todaysql, todaysql))
    for row in rows:
        cid=row[1]
        rtemp = list()
        #y+=1 
        c_rows=sqlRun("SELECT g_title, g_start, g_stop, g_desc, guide.rowid FROM guide WHERE (date(g_start)=date('%s') OR date(g_stop)=date('%s')) AND g_id='%s' ORDER BY g_start" % (todaysql, todaysql, row[0]))
        for event in c_rows:
            d_von = datetime.strptime(event[1],"%Y-%m-%d %H:%M:%S")
            d_bis = datetime.strptime(event[2],"%Y-%m-%d %H:%M:%S")
            fulltext = "<b>"+event[0]+": "+datetime.strftime(d_von, localtime) + " - " + datetime.strftime(d_bis, localtime) + "</b><BR><BR>"+event[3]
            title = fulltext
            if len(title)>300:
                title = title[:297]+"..."
                try:
                    title.decode("UTF-8")
                except:
                    title = title[:296]+"..."
                    pass
            if d_von.date() < dayshown.date():
                d_von = dayshown
            if d_bis.date() > dayshown.date():
                d_bis=datetime.combine(d_bis.date(),time.min)
            x = d_von - datetime.combine(d_von.date(),time.min)
            w = d_bis - d_von
            rtemp.append ([cid, x.total_seconds()/86400.0*100.0*widthq, w.total_seconds()/86400.0*100.0*widthq, event[0], title, fulltext, event[4], row[2]])
            #print row[2]
        ret.append(rtemp)
    return template('epg', curr=datetime.strftime(d_von, localdate), rowss=ret)            

@post('/createepg')
def createepg():
    sqlRun("INSERT INTO records SELECT guide.g_title, channels.rowid, datetime(guide.g_start, '-%s minutes'), datetime(guide.g_stop, '+%s minutes'), 1 FROM guide, guide_chan, channels WHERE guide.g_id = guide_chan.g_id AND channels.cname = guide_chan.g_name AND guide.rowid=%s" % (config.cfg_delta_for_epg, config.cfg_delta_for_epg, request.forms.ret))

    setRecords()
        
    redirect("/records")
    return 

#------------------------------- Record List -------------------------------


@route('/getrecordlist')
def getrecordlist():
    l = []
    rows=sqlRun("SELECT recname, cname, strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rvon), strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rbis), renabled, 100*(strftime('%s','now', 'localtime')-strftime('%s',rvon)) / (strftime('%s',rbis)-strftime('%s',rvon)), records.rowid FROM channels, records where channels.rowid=records.cid AND datetime(rbis)>=datetime('now', 'localtime') ORDER BY rvon")    
    for row in rows:
        l.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
    return json.dumps({"aaData": l } )
    

@route('/records')
def records_s():    
    return template('records', rows2=sqlRun('SELECT rowid, cname FROM channels where cenabled=1'))


@post('/records')
def records_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-1":
        sqlRun("DELETE FROM records WHERE records.rowid=%s" % (myid))
    else: 
        sqlRun("UPDATE records SET renabled=%s WHERE rowid=%s" % (what, myid))            
    setRecords()
    return
    
@post('/create')
def create_p():
    recname = request.forms.recname
    sender = request.forms.Sender
    von = request.forms.von
    bis = request.forms.bis
    am = request.forms.am
    aktiv = getBool(request.forms.aktiv)    

    d_von = datetime.strptime(am + " " + von, "%d.%m.%Y %H:%M")
    d_bis = datetime.strptime(am + " " + bis, "%d.%m.%Y %H:%M")
    delta = timedelta(days=1)
    if d_bis < d_von:
        d_bis = d_bis + delta         
    
    sqlRun("INSERT INTO records VALUES (?, ?, ?, ?, ?)", (recname, sender, d_von, d_bis, aktiv))
    
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
        
    def __init__(self, row):
        threading.Thread.__init__(self)
        self.id = row[0]
        self.von = datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S")
        self.bis = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")        
        self.name = row[5]        
        self.url = row[1]
    
    def run(self): 
        td = self.von-datetime.now()
        deltas = td.total_seconds()
        self.timer = threading.Timer(deltas, self.doIt)
        self.timer.start()
        print "Timer started for %d seconds" % (deltas)
        
    def doIt(self):
        self.running = 1
        block_sz = 8192
        print "record started"    
        u = urllib2.urlopen(self.url)
        fn = config.cfg_recordpath+datetime.now().strftime("%Y%m%d%H%M%S") + " - "        
        fn = fn + "".join([x if x.isalnum() else "_" for x in self.name])
        print fn
        f = open(fn+".mkv", 'wb')
        while self.bis > datetime.now() and self.stopflag==0:
            mybuffer = u.read(block_sz)
            if not mybuffer:
                break
            f.write(mybuffer)
        f.close()
        print "record ended"
    
    def stop(self):
        if self.running==0:
            self.timer.cancel()
        self.stopflag = 1
        #print "stopping"        
   
def setRecords():
    #return

    rows=sqlRun("SELECT records.rowid, cpath, rvon, rbis, cname, records.recname FROM channels, records where channels.rowid=records.cid AND datetime(rbis)>=datetime('now', 'localtime') AND renabled = 1 ORDER BY datetime(rvon)")
    for row in rows: 
        chk = False
        for t in records:
            if t.id == row[0]:
                chk = True
                break
        if chk == False:
            print "created new thread"
            thread = record(row) 
            thread.start()
            records.append(thread)
        
    for index, t in enumerate(records[:]):
        chk = False
        for row in rows: 
            if t.id == row[0]:
                chk = True
                break
        if chk == False:
            print "recording stopped"
            t.stop()
            del records[index]


sqlCreateAll()
purgeDB()          
config.loadConfig()
setRecords()
    
run(host=config.cfg_server_bind_address, port=config.cfg_server_port) #, quiet=True

for t in records:
    t.stop()