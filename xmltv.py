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

import xml.etree.ElementTree as et
from datetime import datetime, timedelta
try:
    import httplib
    import urllib2 as urllib32
except:
    import http.client as httplib
    import urllib.request as urllib32
import zlib
from sql import sqlRun
import config
from sys import version_info

version = ''

def getProgList(ver=''):
    global version
    version = ver    
    print ("tvstreamrecord v.%s / XMLTV import started" % version)
    stri = getFile(config.cfg_xmltvinitpath, 1)
    channellist = []
    if stri:    
        tree = et.fromstring(stri)
        type = tree.attrib.get("generator-info-name")
        for dict_el in tree.iterfind('channel'):
            g_id = dict_el.attrib.get("id")
            name = dict_el.find('display-name').text
            if type == "nonametv":
                url = dict_el.find('base-url').text
            elif type[:4] == "TVxb":
                pass
            else: 
                print ("Unknown XMLTV generator '%s', please contact me if it fails" % type)
                url = dict_el.find('base-url').text
                        
            rows=sqlRun("SELECT cname from channels WHERE cname = '%s' and cenabled=1 GROUP BY cname" % name)
            if rows:
                timerows=sqlRun("SELECT g_lasttime FROM guide_chan WHERE g_id='%s'" % (g_id))
                dtmax = datetime.now()
                if type[:4] == "TVxb":   # same file
                    channellist.append(g_id)
                else:               # separate files
                    lastdate = datetime.now()-timedelta(days=30)
                    if timerows:
                        lastdate = datetime.strptime(timerows[0][0], "%Y-%m-%d %H:%M:%S")
                    dtmax = datetime.min
                    for tim in dict_el.iter("datafor"):
                        dttext = tim.text
                        dtepg  = datetime.strptime(dttext, "%Y-%m-%d")
                        dt = datetime.strptime(tim.attrib.get("lastmodified")[0:14],"%Y%m%d%H%M%S")
                        if dt>lastdate and dtepg>=datetime.now()-timedelta(days=1):
                            source = url+g_id+"_"+dttext+".xml.gz"
                            stri = getFile(source)
                            getProg(stri)    
                        if dt>dtmax:
                            dtmax = dt

                if not timerows:
                    sqlRun("INSERT OR IGNORE INTO guide_chan VALUES (?, ?, ?)", (g_id, name, datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S") ))
                else:
                    sqlRun("UPDATE guide_chan SET g_lasttime=? WHERE g_id=?", (datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S"), g_id))                       
        if type[:4] == "TVxb" and len(channellist)>0:   # same file
            getProg(stri, channellist)        
    print ("XMLTV import completed")
       
def getProg(stri, channellist=[]):    
    sqllist = []
    #f = open("test.xml", "r")
    #stri = f.read()
    if stri: 
        tree = et.fromstring(stri)
        for dict_el in tree.iterfind('programme'):
            dt1 = datetime.strptime(dict_el.attrib.get("start")[0:14],"%Y%m%d%H%M%S")        
            dt2 = datetime.strptime(dict_el.attrib.get("stop")[0:14],"%Y%m%d%H%M%S")        
            p_id = dict_el.attrib.get("channel")
            if len(channellist)==0 or p_id in channellist:
                title = ""
                desc = ""
                if dict_el.find('title') is not None:
                    title = dict_el.find('title').text
                if dict_el.find('sub-title') is not None:
                    sub_title = dict_el.find('sub-title').text
                    if not "http://" in sub_title: # fix for corrupted XML data
                        if title != "": title = title + " - "
                        title = title + sub_title
                if dict_el.find('episode-num[@system="onscreen"]') is not None:
                    desc = dict_el.find('episode-num[@system="onscreen"]').text + ". "
                if dict_el.find('desc') is not None:
                    desc = desc + dict_el.find('desc').text
                sqllist.append([p_id, title, datetime.strftime(dt1, "%Y-%m-%d %H:%M:%S"), datetime.strftime(dt2, "%Y-%m-%d %H:%M:%S"), desc])
        sqlRun("INSERT OR IGNORE INTO guide VALUES (?, ?, ?, ?, ?)", sqllist, 1)
        
def getFile(file_in, override=0):
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
        request.add_header('User-Agent', 'tvstreamrecord/' + version)
        if override==0:
            request.add_header('If-Modified-Since', lastmod)
            request.add_header('If-None-Match', etag)                
        opener = urllib32.build_opener()
        response = opener.open(request)
        feeddata = response.read()
        try:
            lastmod = response.info().getheader('Last-Modified')
            etag = response.info().getheader('ETag')
        except:
            lastmod = response.getheader('Last-Modified')
            etag = response.getheader('ETag')        
        if rows:
            sqlRun("UPDATE caching SET crTime=datetime('now', 'localtime'), Last_Modified=?, ETag=? WHERE url='%s'" % file_in, (lastmod, etag))
        else:
            sqlRun("INSERT INTO caching VALUES (datetime('now', 'localtime'), ?, ?, ?)", (file_in, lastmod, etag))        
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
        out = d.decompress(feeddata)
        print ("XMLTV: reading URL %s" % file_in)
        
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
        print ("XMLTV: no new data, try again later")
        pass

    if type(out) is bytes and not type(out) is str:
        out = out.decode("UTF-8")

    return out

def main(argv=None):
    getProgList('debug')
    return
    
if __name__ == "__main__":
    exit(main())