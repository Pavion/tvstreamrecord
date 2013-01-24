from bottle import route, run, template, post, request
from bottle import static_file, redirect
import sqlite3
from datetime import datetime, timedelta, time
import urllib2
import threading 
#import json

records = []    

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
    
    
@route('/list')
def list_s():
    return template('list', rows=sqlRun('SELECT channels.rowid, cname, cpath, cenabled FROM channels'))

@post('/list')
def list_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-1":
        sqlRun("DELETE FROM channels WHERE channels.rowid=%s" % (myid))
    else: 
        sqlRun("UPDATE channels SET cenabled=%s WHERE channels.rowid=%s" % (what, myid))            
    setRecords()
    return

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

#@route('/upload')
#def upload():
#    return template('upload')

@post('/upload')
def upload_p():
    upfile = request.files.upfile
    header = upfile.file.read(7)
    if header.startswith("#EXTM3U"):
        how = getBool(request.forms.get("switch00"))
        upfilecontent = upfile.file.read()        
        conn = sqlite3.connect('settings.db')
        conn.text_factory = str
        c = conn.cursor()
        if how==0:
            c.execute('DELETE FROM channels')
        lines = upfilecontent.splitlines()
        i = 0
        name = ""
        #id = 0
        for line in lines:
            i = i + 1
            if i>1:
                if i % 2 == 0: 
                    name = line.split(",",1)[1]
                if i % 2 == 1: 
                    c.execute("INSERT INTO channels VALUES (?, ?, '1')", (name, line))
                    #id = id + 1
                    name = ""
        conn.commit()
        conn.close() 
            
        redirect("/list") 

@route('/records')
def records_s():    
    return template('records', rows1=sqlRun("SELECT records.rowid, recname, cname, strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rvon), strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rbis), renabled, 100*(strftime('%s','now', 'localtime')-strftime('%s',rvon)) / (strftime('%s',rbis)-strftime('%s',rvon)) FROM channels, records where channels.rowid=records.cid AND datetime(rbis)>=datetime('now', 'localtime') ORDER BY rvon"), rows2=sqlRun('SELECT rowid, cname FROM channels where cenabled=1'))

@route('/epg')
def epg_s():    
    widthq = 0.9
    ret = list()
    rtemp = list()
    w = 0.0
    for i in range(24):
        t = time(i)
        x = i * 100.0 / 24.0 * widthq
        w =  1.0 / 24.0 * widthq * 100.0 
        rtemp.append([1, x, w, t.strftime("%H:%M"), ""])
    ret.append(rtemp)    
    
    today =  datetime.strptime("2013-02-02 00:00:00","%Y-%m-%d %H:%M:%S")
    todaysql = datetime.strftime(today, "%Y-%m-%d %H:%M:%S")
        
    rows=sqlRun("SELECT guide.g_id FROM guide, guide_chan WHERE guide.g_id=guide_chan.g_id AND (date(g_start)=date('%s') OR date(g_stop)=date('%s')) GROUP BY guide.g_id" % (todaysql, todaysql))
    y=1
    for row in rows:
        rtemp = list()
        y+=1 
        c_rows=sqlRun("SELECT g_title, g_start, g_stop, g_desc FROM guide WHERE (date(g_start)=date('%s') OR date(g_stop)=date('%s')) AND g_id='%s' ORDER BY g_start" % (todaysql, todaysql, row[0]))
        for event in c_rows:
            d_von = datetime.strptime(event[1],"%Y-%m-%d %H:%M:%S")
            d_bis = datetime.strptime(event[2],"%Y-%m-%d %H:%M:%S")
            if d_von.date() < today.date():
                d_von = today
            if d_bis.date() > today.date():
                d_bis=datetime.combine(d_bis.date(),time.min)
            x = d_von - datetime.combine(d_von.date(),time.min)
            w = d_bis - d_von
            #print x.total_seconds(),w.total_seconds()     
            rtemp.append ([y, x.total_seconds()/86400.0*100.0*widthq, w.total_seconds()/86400.0*100.0*widthq, event[0], event[1]+" till "+event[2]+" "+event[3]])
        ret.append(rtemp)
    return template('epg', rowss=ret)            
            
            
        
        #print row[0]#,row[1]#,row[2],row[3],row[4]
    #return template('epg', rows1=sqlRun("SELECT g_name, g_title, g_start, g_stop, g_desc FROM guide, guide_chan WHERE guide.g_id=guide_chan.g_id"))


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

    print "%s - %s - %s - %s - %s - %s" % (recname, sender, von, bis, am, aktiv)
    #return
#    if hasattr(datetime, 'strptime'):
    strptime = datetime.strptime
#    else:
#        strptime = lambda date_string, format: datetime(*(time.strptime(date_string, format)[0:6]))
    d_von = strptime(am + " " + von, "%d.%m.%Y %H:%M")
    d_bis = strptime(am + " " + bis, "%d.%m.%Y %H:%M")
    delta = timedelta(days=1)
    if d_bis < d_von:
        d_bis = d_bis + delta         
    
    sqlRun("INSERT INTO records VALUES (?, ?, ?, ?, ?)", (recname, sender, d_von, d_bis, aktiv))
    
    setRecords()
    
    #redirect("/recordings")
    return 
    
def sqlRun(sql, t=-1):    
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    conn.text_factory = str
    if t != -1:
        rows = c.execute(sql, t)
    else:
        rows = c.execute(sql)
    fa=rows.fetchall();
    conn.commit()
    conn.close()
    return fa
    
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
        
    def __init__(self, row):
        threading.Thread.__init__(self)
        #print "init id: %d" % row[0]
        self.id = row[0]
        self.von = datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S")
        self.bis = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")        
        print self.von
        print self.bis
        print row[4]
        print row[2]
        self.fname = row[4]+row[2]
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
        fn = datetime.now().strftime("%Y%m%d%H%M%S")
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
    return

    rows=sqlRun("SELECT records.rowid, cpath, rvon, rbis, cname FROM channels, records where channels.rowid=records.cid AND datetime(rbis)>=datetime('now', 'localtime') AND renabled = 1 ORDER BY datetime(rvon)")
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

#sqlRun('DROP TABLE records')    
sqlRun('CREATE TABLE IF NOT EXISTS channels (cname TEXT, cpath TEXT, cenabled INTEGER)')  
sqlRun('CREATE TABLE IF NOT EXISTS records (recname TEXT, cid INTEGER, rvon TEXT, rbis TEXT, renabled INTEGER)')    

setRecords()
    
run(host='127.0.0.1', port=8030)

for t in records:
    t.stop()