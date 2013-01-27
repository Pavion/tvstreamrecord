import sqlite3
import config

def sqlRun(sql, t=-1, many=0):    
    fa = []
    try:
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        conn.text_factory = str
        if t != -1:
            if many == 1:
                print "na dann mal los"
                rows = c.executemany(sql, t)
            else:                
                rows = c.execute(sql, t)
        else:
            rows = c.execute(sql)
        fa=rows.fetchall();
        conn.commit()
        conn.close()
    except:
            
        print "exception: %s" % sql
        pass
    return fa

def purgeDB():
    sqlRun("DELETE FROM caching WHERE julianday('now', 'localtime')-julianday(crTime)>%d" % config.purgedelta)
    sqlRun("DELETE FROM guide_chan WHERE julianday('now', 'localtime')-julianday(g_lasttime)>%d" % config.purgedelta)
    sqlRun("DELETE FROM guide WHERE julianday('now', 'localtime')-julianday(g_start)>%d" % config.purgedelta)
    return
