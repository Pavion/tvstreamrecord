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
        pass
    return fa
