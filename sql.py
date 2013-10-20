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

import sqlite3

def sqlRun(sql, t=-1, many=0):    
    fa = []
    try:
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        conn.text_factory = str
        if t != -1:
            if many == 1:
                rows = c.executemany(sql, t)
            else:                
                rows = c.execute(sql, t)
        else:
            if many == 1:
                rows = c.executescript(sql)
            else:
                rows = c.execute(sql)
        fa=rows.fetchall();
        conn.commit()
        conn.close()
    except:            
        print "exception: %s" % sql
        pass
    return fa

def sqlDropAll():
    sql  = 'DROP TABLE IF EXISTS channels;'
    sql += 'DROP TABLE IF EXISTS records;'
    sql += 'DROP TABLE IF EXISTS guide_chan;'
    sql += 'DROP TABLE IF EXISTS guide;'
    sql += 'DROP TABLE IF EXISTS caching;'
    sql += 'DROP TABLE IF EXISTS config;'
    sqlRun(sql, -1, 1)
    return    
    
def sqlCreateAll(version):
    sql = ""
    rows = sqlRun("select * from config")
    if not rows:
        sql += 'CREATE TABLE IF NOT EXISTS channels (cname TEXT collate nocase UNIQUE, cpath TEXT, cenabled INTEGER, cext TEXT, cid INTEGER, epgscan INTEGER);'
        sql += 'CREATE TABLE IF NOT EXISTS records (recname TEXT, cid INTEGER, rvon TEXT, rbis TEXT, renabled INTEGER, rmask INTEGER);'    
        sql += 'CREATE TABLE IF NOT EXISTS caching (crTime TEXT, url TEXT, Last_Modified TEXT, ETag TEXT);'
        sql += 'CREATE TABLE IF NOT EXISTS guide_chan (g_id TEXT UNIQUE, g_name TEXT collate nocase UNIQUE, g_lasttime TEXT);'
        sql += 'CREATE TABLE IF NOT EXISTS guide (g_id TEXT, g_title TEXT, g_start TEXT, g_stop TEXT, g_desc TEXT, PRIMARY KEY (g_id, g_start, g_stop));'
        sql += 'CREATE TABLE IF NOT EXISTS config (param TEXT UNIQUE, desc TEXT, value TEXT);'
        sql += "INSERT OR REPLACE INTO config VALUES ('cfg_version', 'Program version', '%s');" % version           
    else: 
        rows = sqlRun("select value from config where param='cfg_version'")
        if not rows: # Version < 0.4.4
            sql += 'ALTER TABLE records ADD COLUMN rmask INTEGER DEFAULT 0;'
            sql += "INSERT INTO config VALUES ('cfg_version', 'Program version', '%s');" % version           
        else: # Versioning
            oldver = rows[0][0]
            if oldver<>version:
                if oldver < '0.4.4a':
                    sql += "ALTER TABLE channels ADD COLUMN cext TEXT DEFAULT '';" 
                if oldver < '0.5.0':
                    sql += "ALTER TABLE channels ADD COLUMN cid INTEGER;" 
                    sql += "UPDATE channels SET cid=rowid;"
                if oldver < '0.5.1':
                    sql += "ALTER TABLE channels ADD COLUMN epgscan INTEGER DEFAULT 0;" 
                if oldver < '0.5.2':
                    sql += 'CREATE TABLE IF NOT EXISTS guide_chan_neu (g_id TEXT UNIQUE, g_name TEXT collate nocase UNIQUE, g_lasttime TEXT);'
                    sql += 'INSERT OR IGNORE INTO guide_chan_neu SELECT * FROM guide_chan;'
                    sql += 'DROP TABLE guide_chan;'
                    sql += 'ALTER TABLE guide_chan_neu RENAME TO guide_chan;'
                if oldver > version:
                    print "Critical error: Version mismatch!!!"     
               
                sql += "INSERT OR REPLACE INTO config VALUES ('cfg_version', 'Program version', '%s');" % version           
                print "New version %s was implemented" % version    
           
    
    sqlRun(sql, -1, 1)
    return
    
def purgeDB():
    import config
    #sql  = "DELETE FROM records WHERE julianday('now', 'localtime')-julianday(rbis)>%d;" % config.cfg_purgedelta
    sql  = "DELETE FROM caching WHERE julianday('now', 'localtime')-julianday(crTime)>%d;" % config.cfg_purgedelta
    sql += "DELETE FROM guide_chan WHERE julianday('now', 'localtime')-julianday(g_lasttime)>%d;" % config.cfg_purgedelta
    sql += "DELETE FROM guide WHERE julianday('now', 'localtime')-julianday(g_start)>%d;" % config.cfg_purgedelta
    sqlRun(sql, -1, 1)
    return
