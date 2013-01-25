# coding=UTF-8
import xml.etree.ElementTree as et
import csv
from datetime import datetime, timedelta
#import sqlite3
import httplib
import urllib2
import zlib
from sql import sqlRun

purgedelta = 30
initpath = 'http://xmltv.spaetfruehstuecken.org/xmltv/datalist.xml.gz'
    
#def sqlRun(sql, t=-1):    
#    try:
#        conn = sqlite3.connect('settings.db')
#        c = conn.cursor()
#        conn.text_factory = str
#        if t != -1:
#            rows = c.execute(sql, t)
#        else:
#            rows = c.execute(sql)
#        fa=rows.fetchall();
#        conn.commit()
#        conn.close()
#    except:
#        fa = -1
#        pass
#    return fa
    
#sqlRun('DROP TABLE IF EXISTS guide_chan')
#sqlRun('DROP TABLE IF EXISTS guide')
#sqlRun('DROP TABLE IF EXISTS caching')
sqlRun('CREATE TABLE IF NOT EXISTS caching (crTime TEXT, url TEXT, Last_Modified TEXT, ETag TEXT)')
sqlRun('CREATE TABLE IF NOT EXISTS guide_chan (g_id TEXT, g_name TEXT collate nocase, g_lasttime TEXT)')  
sqlRun('CREATE TABLE IF NOT EXISTS guide (g_id TEXT, g_title TEXT, g_start TEXT UNIQUE, g_stop TEXT, g_desc TEXT)')    

def getProgList():
    stri = getFile(initpath)
    if stri:    
        tree = et.fromstring(stri)
        for dict_el in tree.iterfind('channel'):
            id = dict_el.attrib.get("id")
            name = dict_el.find('display-name').text
            url = dict_el.find('base-url').text 
            
            rows=sqlRun("SELECT cname from channels WHERE cname = '%s' GROUP BY cname")
            if rows:

                rows=sqlRun("SELECT g_lasttime FROM guide_chan WHERE g_id='%s'" % (id))
                lastdate = datetime.now()-timedelta(days=1)
                if rows:
                    lastdate = datetime.strptime(rows[0][0], "%Y-%m-%d %H:%M:%S")
                #source = "" 
                dtmax = datetime.min
                for tim in dict_el.iter("datafor"):
                    dttext = tim.text
                    dt = datetime.strptime(tim.attrib.get("lastmodified")[0:14],"%Y%m%d%H%M%S")
                    if dt>lastdate:   
                        source = url+id+"_"+dttext+".xml.gz"
                        print source
                        #getProg(source)    
                    if dt>dtmax:
                        dtmax = dt

                if not rows:
                    sqlRun("INSERT INTO guide_chan VALUES (?, ?, ?)", (id, name, datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S") ))
                else:
                    sqlRun("UPDATE guide_chan SET g_lasttime=? WHERE g_id=?", (datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S"), id))
           
            
       
def getProg(p_id):    
    stri = getFile(p_id)
    #tree = et.parse(p_id)
    tree = et.fromstring(stri)
    for dict_el in tree.iterfind('programme'):
        dt1 = datetime.strptime(dict_el.attrib.get("start")[0:14],"%Y%m%d%H%M%S")        
        dt2 = datetime.strptime(dict_el.attrib.get("stop")[0:14],"%Y%m%d%H%M%S")        
        p_id = dict_el.attrib.get("channel")
        title = ""
        desc = ""
        if dict_el.find('title') is not None:
            title = dict_el.find('title').text
        if dict_el.find('desc') is not None:
            desc = dict_el.find('desc').text
        sqlRun("INSERT INTO guide VALUES (?, ?, ?, ?, ?)", (p_id, title, datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S"), datetime.strftime(dt2, "%Y-%m-%d %H:%M:%S"), desc))
        
def getFile(file_in):
    rows=sqlRun("SELECT * FROM caching WHERE url='%s'" % file_in)    
    lastmod = ""
    etag = "" 
    out = ""
    if rows:
        lastmod = rows[0][2]
        etag = rows[0][3]
    try:
        print lastmod, etag
        httplib.HTTPConnection.debuglevel = 1                            
        request = urllib2.Request(file_in)
        request.add_header('User-Agent', 'tvstreamrecord/0.3 (alpha/test)')
        request.add_header('If-Modified-Since', lastmod)
        request.add_header('If-None-Match', etag)    
        opener = urllib2.build_opener()
        response = opener.open(request)
        feeddata = response.read()        
        if rows:
            sqlRun("UPDATE caching SET crTime=datetime('now', 'localtime'), Last_Modified=?, ETag=? WHERE url=%s" % file_in, (response.info().getheader('Last-Modified'), response.info().getheader('ETag')))
        else:
            sqlRun("INSERT INTO caching VALUES (datetime('now', 'localtime'), ?, ?, ?)", (file_in, response.info().getheader('Last-Modified'), response.info().getheader('ETag')))        
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
        out = d.decompress(feeddata)
        print "nope"
    except:
        print "passed"
        pass
    return out
    
def purgeDB():
    sqlRun("DELETE FROM caching WHERE julianday('now', 'localtime')-julianday(crTime)>%d" % purgedelta)
    sqlRun("DELETE FROM guide_chan WHERE julianday('now', 'localtime')-julianday(g_lasttime)>%d" % purgedelta)
    sqlRun("DELETE FROM guide WHERE julianday('now', 'localtime')-julianday(g_start)>%d" % purgedelta)
    return

#getProgList()

#rows=sqlRun("SELECT g_name, g_title, g_start, g_stop, g_desc FROM guide, guide_chan WHERE guide.g_id=guide_chan.g_id")
#rows=sqlRun("SELECT * FROM guide_chan")
#for row in rows:
#    print row[0],row[1],row[2]#,row[3],row[4]
#print "aah"

#getFile('http://xmltv.spaetfruehstuecken.org/xmltv/hd.daserste.de_2013-01-23.xml.gz')

#file = open("datalist.xml", "r")
#tt = file.read()
#file.close()
#getProgList(tt)
