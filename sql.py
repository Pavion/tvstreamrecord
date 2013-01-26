import sqlite3

def sqlRun(sql, t=-1):    
    fa = []
    try:
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
    except:
            
        print "exception: %s" % sql
        pass
    return fa

def purgeDB():
    purgedelta = 30 # config
    sqlRun("DELETE FROM caching WHERE julianday('now', 'localtime')-julianday(crTime)>%d" % purgedelta)
    sqlRun("DELETE FROM guide_chan WHERE julianday('now', 'localtime')-julianday(g_lasttime)>%d" % purgedelta)
    sqlRun("DELETE FROM guide WHERE julianday('now', 'localtime')-julianday(g_start)>%d" % purgedelta)
    return
