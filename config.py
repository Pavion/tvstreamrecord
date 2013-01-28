configuration = [
[
'cfg_xmltvinitpath',
'Initial path for an XMLTV-Import',
'http://xmltv.spaetfruehstuecken.org/xmltv/datalist.xml.gz'
],

[
'cfg_purgedelta',
'Purge database records older than [days]',
30
],

[
'cfg_delta_for_epg',
'Lenghten an EPG-record (delta before and after), [minutes]',
3
],

[
'cfg_recordpath',
'path for recording',
'/volume1/common/'
],

[
'cfg_server_bind_address',
'Server bind address',
'0.0.0.0'
],   

[
'cfg_server_port',
'Server port',
8030
]

]

for config in configuration:
    globals()[config[0]] = config[2]
    
def getDict():
    ret = []
    for r in globals():
        if r[0:4] =='cfg_':
            ret.append(r)
    return ret

def loadConfig():
    from sql import sqlRun
    sqlRun("INSERT OR IGNORE INTO config VALUES (?, ?, ?)",configuration,1)
    rows = sqlRun("SELECT param, value FROM config")
    setConfig(rows)
    return
        
def setConfig(attrlist = []):
    for attr in attrlist:
        if attr[0] in globals():
            globals()[attr[0]] = attr[1]                
    #if attrlist:
    saveConfig()
            
            
def saveConfig():
    from sql import sqlRun
    #ret = []
    sql = ''   
    for var in getDict():
        sql += "UPDATE config SET value='%s' WHERE param='%s';" % (globals()[var], var) 
        #ret.append([var, globals()[var]])
        #print [var, globals()[var]]
    # may as well use 'INSERT OR REPLACE INTO', this one is easier while working
    #sqlRun('DELETE FROM config')
    #sqlRun('INSERT INTO config VALUES (?, ?)', ret, 1)
    sqlRun(sql, -1, 1)
    return    
        
#print getDict()
#globals().append('hahaha')
#globals()['cfg_hahaha'] = 12
#print getDict()

