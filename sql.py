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

import sqlite3

dbpath = "settings.db"

def setDb(path):
    global dbpath
    dbpath = path

def sqlRun(sql, t=-1, many=0):
    fa = []
    global dbpath
    try:
        conn = sqlite3.connect(dbpath, timeout=20)
        c = conn.cursor()
        c.execute('PRAGMA journal_mode = OFF;')
        conn.text_factory = sqlite3.OptimizedUnicode
        #print (conn.text_factory)
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
        if "INSERT" in sql and many==0:
            fa = rows.lastrowid
        else:
            fa=rows.fetchall()
        conn.commit()
        conn.close()
    except Exception as ex:
        if sql=="select * from config":
            print ("New database created. Thank you for using this package.")
        else:
            print ("SQL Exception '%s' with '%s'" % (ex,sql))
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
        sql += 'CREATE TABLE IF NOT EXISTS records (recname TEXT, cid INTEGER, rvon TEXT, rbis TEXT, renabled INTEGER, rmask INTEGER, uniqueid TEXT, PRIMARY KEY (recname, cid, rvon, rbis, rmask));'
        sql += 'CREATE TABLE IF NOT EXISTS caching (crTime TEXT, url TEXT, Last_Modified TEXT, ETag TEXT);'
        sql += 'CREATE TABLE IF NOT EXISTS guide_chan (g_id TEXT UNIQUE, g_name TEXT collate nocase UNIQUE, g_lasttime TEXT);'
        sql += 'CREATE TABLE IF NOT EXISTS guide (g_id TEXT, g_title TEXT, g_start TEXT, g_stop TEXT, g_desc TEXT, PRIMARY KEY (g_id, g_start, g_stop));'
        sql += 'CREATE TABLE IF NOT EXISTS config (param TEXT UNIQUE, desc TEXT, value TEXT);'
        sql += 'CREATE TABLE IF NOT EXISTS blacklist (ip TEXT UNIQUE, trycount INTEGER, lasttry TEXT);'
        sql += "INSERT OR REPLACE INTO config VALUES ('cfg_version', 'Program version', '%s');" % version
        sql += "INSERT OR REPLACE INTO config VALUES ('credentials', '', '');"
    else:
        rows = sqlRun("select value from config where param='cfg_version';")
        if not rows: # Version < 0.4.4
            sql += 'ALTER TABLE records ADD COLUMN rmask INTEGER DEFAULT 0;'
            sql += "INSERT INTO config VALUES ('cfg_version', 'Program version', '%s');" % version
        else: # Versioning
            oldver = rows[0][0]
            if oldver!=version:
                if oldver < '0.4.4a':
                    sql += "ALTER TABLE channels ADD COLUMN cext TEXT DEFAULT '';"
                if oldver < '0.5.0':
                    sql += "ALTER TABLE channels ADD COLUMN cid INTEGER;"
                    sql += "UPDATE channels SET cid=rowid;"
                if oldver < '0.5.1':
                    sql += "ALTER TABLE channels ADD COLUMN epgscan INTEGER DEFAULT 0;"
                if oldver < '0.5.1f':
                    sql += 'CREATE TABLE IF NOT EXISTS guide_chan_neu (g_id TEXT UNIQUE, g_name TEXT collate nocase UNIQUE, g_lasttime TEXT);'
                    sql += 'INSERT OR IGNORE INTO guide_chan_neu SELECT * FROM guide_chan;'
                    sql += 'DROP TABLE guide_chan;'
                    sql += 'ALTER TABLE guide_chan_neu RENAME TO guide_chan;'
                if oldver < '0.6.1':
                    sql += 'UPDATE records SET rmask = case when (rmask & 64)=64 then ((rmask - 64) << 1) + 1 else rmask << 1 end;'
                if oldver < '0.6.4':
                    sql += 'CREATE TABLE IF NOT EXISTS blacklist (ip TEXT UNIQUE, trycount INTEGER, lasttry TEXT);'
                    sql += "INSERT OR IGNORE INTO config VALUES ('credentials', '', '');"
                    val = sqlRun("SELECT value FROM config WHERE param='cfg_recordpath' AND NOT (substr(value, -1)='/' OR substr(value, -1)='\');")
                    if val:
                        val = val[0][0]
                        for c in range(len(val)-1,0,-1):
                            if val[c]=='/' or val[c]=='\\':
                                sql += "UPDATE config SET value='%s' WHERE param='cfg_recordpath';" % val[0:c+1]
                                sql += "INSERT OR REPLACE INTO config VALUES ('cfg_record_mask', '', '" + val[c+1:] + "%date% - %title%');"
                                break
                if oldver < '1.1.0':
                    sql += "UPDATE config SET value=value || ' rtsp' WHERE param = 'cfg_ffmpeg_types' and not lower(value) LIKE '%rtsp%';"
                if oldver < '1.2.1':
                    sql += "UPDATE config SET value='-loglevel fatal ' || value WHERE param = 'cfg_ffmpeg_params' and not lower(value) LIKE '%loglevel%';"
                if oldver < '1.3.2':
                    sql += "ALTER TABLE records ADD COLUMN uniqueid TEXT;"
                if oldver < '1.3.5':
                    sql += "INSERT OR IGNORE INTO config VALUES ('cfg_delta_before_epg', '', (SELECT value FROM config WHERE param='cfg_delta_for_epg'));"
                    sql += "UPDATE config SET param='cfg_delta_after_epg' WHERE param='cfg_delta_for_epg';"
                if oldver < '1.4.0':
                    sqlRun("DROP TABLE IF EXISTS records_old;", -1, -1)
                    sql += "ALTER TABLE records RENAME TO records_old;"
                    sql += "CREATE TABLE IF NOT EXISTS records (recname TEXT, cid INTEGER, rvon TEXT, rbis TEXT, renabled INTEGER, rmask INTEGER, uniqueid TEXT, PRIMARY KEY (recname, cid, rvon, rbis, rmask));"
                    sql += "INSERT OR IGNORE INTO records SELECT * FROM records_old;"
                    
                if oldver > version:
                    print ("Critical error: Version mismatch!!!")

                sql += "INSERT OR REPLACE INTO config VALUES ('cfg_version', 'Program version', '%s');" % version
                print ("New version %s was implemented" % version)
    if sql:
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
