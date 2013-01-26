# coding=UTF-8
import xml.etree.ElementTree as et
from datetime import datetime, timedelta
import httplib
import urllib2
import zlib
from sql import sqlRun

def getProgList():
    initpath = 'http://xmltv.spaetfruehstuecken.org/xmltv/datalist.xml.gz'
    stri = getFile(initpath)
    if stri:    
        tree = et.fromstring(stri)
        for dict_el in tree.iterfind('channel'):
            g_id = dict_el.attrib.get("id")
            name = dict_el.find('display-name').text
            url = dict_el.find('base-url').text 
            
            rows=sqlRun("SELECT cname from channels WHERE cname = '%s' and cenabled=1 GROUP BY cname" % name)
            if rows:

                rows=sqlRun("SELECT g_lasttime FROM guide_chan WHERE g_id='%s'" % (g_id))
                lastdate = datetime.now()-timedelta(days=10)
                if rows:
                    lastdate = datetime.strptime(rows[0][0], "%Y-%m-%d %H:%M:%S")
                #source = "" 
                dtmax = datetime.min
                for tim in dict_el.iter("datafor"):
                    dttext = tim.text
                    dt = datetime.strptime(tim.attrib.get("lastmodified")[0:14],"%Y%m%d%H%M%S")
                    if dt>lastdate:   
                        source = url+g_id+"_"+dttext+".xml.gz"
                        print source
                        getProg(source)    
                    if dt>dtmax:
                        dtmax = dt

                if not rows:
                    sqlRun("INSERT INTO guide_chan VALUES (?, ?, ?)", (g_id, name, datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S") ))
                else:
                    sqlRun("UPDATE guide_chan SET g_lasttime=? WHERE g_id=?", (datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S"), g_id))
                       
       
def getProg(p_id):    
    stri = getFile(p_id)
    if stri: #tree = et.parse("hd.zdf.de_2013-02-14.xml")
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
            print dt1, dt2, p_id, title
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
            sqlRun("UPDATE caching SET crTime=datetime('now', 'localtime'), Last_Modified=?, ETag=? WHERE url='%s'" % file_in, (response.info().getheader('Last-Modified'), response.info().getheader('ETag')))
        else:
            sqlRun("INSERT INTO caching VALUES (datetime('now', 'localtime'), ?, ?, ?)", (file_in, response.info().getheader('Last-Modified'), response.info().getheader('ETag')))        
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
        out = d.decompress(feeddata)
        print "XML got"
    except:
        print "XML passed"
        pass
    return out
    
