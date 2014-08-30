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


from datetime import datetime, timedelta
try:
    import httplib
    import urllib2 as urllib32
except:
    import http.client as httplib
    import urllib.request as urllib32
import zlib
try:
    from sql import sqlRun
    import config
except:
    def sqlRun(v1="", v2="", v3=""):
        return None

def getAttr(stri, attr):
    ret = ""
    p1 = stri.find(attr) + len(attr) + 2
    p2 = stri.find('"', p1)
    if p1 >= len(attr) + 2 and p2>p1:
        ret = stri[p1:p2]
    return ret

def getFirst(stri, attr):
    ret = ""
    p1 = stri.find('<'+attr) 
    if p1 != -1:
        p1 = p1 + len(attr) + 1
        p2 = stri.find('>', p1) + 1 
        p3 = stri.find('</'+attr, p2) 
        ret = stri[p2:p3].strip()
    return ret

def getList(stri, attr):
#    treelist = list()
    p1 = stri.find('<'+attr) 
    while p1!=-1:
        p1 = p1 + len(attr) + 1 
        p2 = stri.find('>', p1) + 1     
        p3 = stri.find('</'+attr, p2) 
        att = stri[p1:p2-1].strip()
        txt = stri[p2:p3].strip()
        yield((att, txt))
        p1 = stri.find('<'+attr, p3)   

def getProgList(ver=''):
    print ("tvstreamrecord v.%s / XMLTV import started" % ver)
    stri = getFile(config.cfg_xmltvinitpath, 1, ver)
    
    channellist = []        
    typ = getAttr(stri[:200], "generator-info-name")
    
    for attr,innertxt in getList(stri, "channel"):
        g_id = getAttr(attr, "id")
        name = getFirst(innertxt, 'display-name')
        if typ == "nonametv":
            url = getFirst(innertxt, 'base-url')
        elif typ[:4] == "TVxb":
            pass
        else: 
            print ("Unknown XMLTV generator '%s', please contact me if it fails" % typ)
            url = getFirst(innertxt, 'base-url')
                
        rows=sqlRun("SELECT cname from channels WHERE cname = '%s' and cenabled=1 GROUP BY cname" % name)
        if rows:
            timerows=sqlRun("SELECT g_lasttime FROM guide_chan WHERE g_id='%s'" % (g_id))
            dtmax = datetime.now()
            if typ[:4] == "TVxb":   # same file
                channellist.append(g_id)
            else:               # separate files
                lastdate = datetime.now()-timedelta(days=30)
                if timerows:
                    lastdate = datetime.strptime(timerows[0][0], "%Y-%m-%d %H:%M:%S")
                dtmax = datetime.min
                
                for t_attr, dttext in getList(innertxt, "datafor"):
                    dtepg  = datetime.strptime(dttext, "%Y-%m-%d")
                    dt = datetime.strptime(getAttr(t_attr, "lastmodified")[0:14],"%Y%m%d%H%M%S")
                    if dt>lastdate and dtepg>=datetime.now()-timedelta(days=1):
                        source = url+g_id+"_"+dttext+".xml.gz"
                        getProg(getFile(source,0,ver))
                    if dt>dtmax:
                        dtmax = dt
            if not timerows:
                sqlRun("INSERT OR IGNORE INTO guide_chan VALUES (?, ?, ?)", (g_id, name, datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S") ))
            else:
                sqlRun("UPDATE guide_chan SET g_lasttime=? WHERE g_id=?", (datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S"), g_id))                       

    if typ[:4] == "TVxb" and len(channellist)>0:   # same file
        getProg(stri, channellist)
      
    del (stri)        
    print ("XMLTV import completed")
    return
  

def getProg(strp, channellist=[]):    
    sqllist = []
    
    for attr,innertxt in getList(strp, 'programme'):    
        dt1 = datetime.strptime(getAttr(attr, "start")[0:14],"%Y%m%d%H%M%S")        
        dt2 = datetime.strptime(getAttr(attr, "stop")[0:14],"%Y%m%d%H%M%S")        
        p_id = getAttr(attr, "channel")
        if len(channellist)==0 or p_id in channellist:
            desc = ""
            title = getFirst(innertxt, 'title')
            sub_title = getFirst(innertxt, 'sub-title')
            if not "http://" in sub_title: # fix for corrupted XML data
                if title != "": title = title + " - "
                title = title + sub_title
            eplist = getFirst(innertxt, 'episode-num')
            for epatt, epin in getList(eplist, 'system'):
                if getAttr(epatt, 'system') == 'onscreen':
                    desc = epin + ". "
                    break
            tmpdesc = getFirst(innertxt, 'desc')
            desc = desc + tmpdesc 
            sqllist.append([p_id, title, datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S"), datetime.strftime(dt2, "%Y-%m-%d %H:%M:%S"), desc])
    sqlRun("INSERT OR IGNORE INTO guide VALUES (?, ?, ?, ?, ?)", sqllist, 1)

    return    
        
def getTestFile():
    with open('e.xml', 'r') as content_file:
        stri = content_file.read()
    try:
        stri = stri.decode("UTF-8")
    except:
        pass
    return stri

def getFile(file_in, override=0, ver=""):
    rows=sqlRun("SELECT * FROM caching WHERE url='%s'" % file_in)    
    lastmod = ""
    etag = "" 
    out = ""
    if rows:
        lastmod = rows[0][2]
        etag = rows[0][3]
    try:
        httplib.HTTPConnection.debuglevel = 0                            
        request = urllib32.Request(file_in)
        request.add_header('User-Agent', 'tvstreamrecord/' + ver)
        if override==0:
            request.add_header('If-Modified-Since', lastmod)
            request.add_header('If-None-Match', etag)                
        opener = urllib32.build_opener()
        hresponse = opener.open(request)
        feeddata = hresponse.read()
        hr = hresponse.info()        
        lastmod = hr.get('Last-Modified')
        etag = hr.get('ETag')
        if rows and lastmod and etag:
            sqlRun("UPDATE caching SET crTime=datetime('now', 'localtime'), Last_Modified=?, ETag=? WHERE url='%s'" % file_in, (lastmod, etag))
        elif lastmod and etag:
            sqlRun("INSERT INTO caching VALUES (datetime('now', 'localtime'), ?, ?, ?)", (file_in, lastmod, etag))        
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
        out = d.decompress(feeddata)
        print ("XMLTV: reading URL %s with %s bytes" % (file_in, len(out)))
        if not b"</tv>" in out[-1000:]:
            print ("Possibly corrupted XML file, attempting to repair...")
            pos = out.rfind(b"</programme>") 
            if pos != -1:
                out = out[:pos+12]  + b"</tv>"
            else: 
                pos = out.rfind(b"</channel>")
                if pos != -1:
                    out = out[:pos+10]  + b"</tv>" 
    except Exception as ex:
        #print (ex)
        print ("XMLTV: no new data, try again later (%s)" % file_in)
        pass

    try:
        out = out.decode("UTF-8")
    except:
        pass
    
    return out

def main(argv=None):
    getProgList('debug')
    return
    
if __name__ == "__main__":
    exit(main())