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

import xml.etree.ElementTree as et
from datetime import datetime, timedelta
import httplib
import urllib2
import zlib
from sql import sqlRun
import config

version = ''

def getProgList(ver=''):
    global version
    version = ver    
    print "tvstreamrecord v.%s / XMLTV import started" % version
    stri = getFile(config.cfg_xmltvinitpath, 1)
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
                        #print source
                        getProg(source)    
                    if dt>dtmax:
                        dtmax = dt

                if not rows:
                    sqlRun("INSERT OR IGNORE INTO guide_chan VALUES (?, ?, ?)", (g_id, name, datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S") ))
                else:
                    sqlRun("UPDATE guide_chan SET g_lasttime=? WHERE g_id=?", (datetime.strftime(dtmax, "%Y-%m-%d %H:%M:%S"), g_id))                       
    print "XMLTV import completed"
       
def getProg(p_id):    
    stri = getFile(p_id)
    sqllist = []
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
            #print dt1, dt2, p_id, title
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
        #print lastmod, etag
        httplib.HTTPConnection.debuglevel = 1                            
        request = urllib2.Request(file_in)
        request.add_header('User-Agent', 'tvstreamrecord/' + version)
        if override==0:
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
        print "XMLTV: reading URL %s" % file_in
    except:
        print "XMLTV: no new data, try again later"
        pass
    return out
    
