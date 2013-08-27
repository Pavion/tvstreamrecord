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

import urllib2
from datetime import datetime, timedelta#, time, date
import time
import sys

# Debug only
#def cls():
#    from os import system, name
#    system('cls' if name=='nt' else 'clear')
    

def unistr(strin):
    strout = unicode('')
    for s in strin:
        try:
            strout = strout + unicode(s)
        except:
            try:
                strout = strout + s.decode('latin1')
            except:
                pass     
    return strout

# converts string into time, i.e. 0x20 0x15 0x15 = 20:15:00 - what a funny way to encode time!
def str_to_delta(strin):
    try:
        h = int(hex(ord(strin[0])).replace("0x",""))
        n = int(hex(ord(strin[1])).replace("0x",""))
        s = int(hex(ord(strin[2])).replace("0x",""))
        return timedelta(hours=h, minutes = n, seconds = s)
    except:
        #print "Wrong time detected"
        return timedelta(0)

# converts Modified Julian date to local date
def mjd_to_local(strin):
        
    try:
        MJD = ord(strin[0]) * 256 + ord(strin[1])
        Yx = int ( (MJD - 15078.2) / 365.25 ) 
        Mx = int ( (MJD - 14956.1 - int (Yx * 365.25) ) / 30.6001 )
        D = MJD - 14956 - int (Yx * 365.25) - int (Mx * 30.6001)
        K = 0
        if Mx == 14 or Mx == 15:
            K = 1
        Y = Yx + K + 1900
        M = Mx - 1 - K * 12
    
        start = datetime(Y, M, D, 0, 0, 0)                
    
        # UTC / daytime offset
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset = - (time.altzone if is_dst else time.timezone)
        utc_off_delta = timedelta(seconds = utc_offset)
    
        # time offset
        t = str_to_delta(strin[2:5])
        
        start = start + utc_off_delta + t
    except:
        start = datetime(1900,1,1,0,0,0) 
    
    return start 

def read_stream(f_in):
    # Possible package sizes of MPEG-TS (default = 188)
    packagesizes = [188, 204, 208]
    size = -1        
    
    # Sync byte (default = 'G' or 0x47)
    syncbyte = 'G' 
    
    # EPG data
    channel = [0x12]
    
    # Channel list & description
    channelinfo = [0x11]

    # Analysing stream and step size
    block_sz = 1000
    mybuffer = f_in.read(block_sz)
    for i in range(0, 400): 
        if mybuffer[i] == syncbyte: 
            for s in packagesizes:
                if mybuffer[i+s] == syncbyte and mybuffer[i+s*2] == syncbyte and mybuffer[i+s*3] == syncbyte:
                    size = s
                    break
            if size != -1:
                break
    if size == -1:
        print "No sync byte found, probably not a MPEG2 stream. Aborting..."
        return

    # syncronise package size and start byte
    r = range(0,1000+size,size)
    offset = r[len(r)-1]-1000
    f_in.read(offset)
    
    # define blocks 
    blocktoread = 100
    block_sz = size * blocktoread
    blocksread = 0
    maxblocksread = 150*1024*1024
    # or
    maxtimespend = timedelta(seconds=60)
    starttime = datetime.now() 
    
    # Continuity counter    
    ccount = [-1, -1]
    ccount_new = [-1, -1]
    
    # Payload storing an controlling 
    payload = ["",""]
    myfirstpayload = ["", ""]
    ch = 0
    maxlist = [list(),list()]
    analyse = [False, False]
    
    # read loop
    while True:
        mybuffer = f_in.read(block_sz)
        blocksread = blocksread + block_sz  
        if not mybuffer or blocksread>maxblocksread or datetime.now() -starttime>maxtimespend:
            print "Read finished at %s/%s MB" % (blocksread/1024/1024, maxblocksread/1024/1024)            
            for ch in range(0,2):
                plist = getList(payloadSort(payload[ch], False), ch)
                if len(plist)>len(maxlist[ch]):
                    maxlist[ch] = plist
            break
        for i in range(0, len(mybuffer), size):
            pid1 = ord(mybuffer[i+1])
            pid2 = ord(mybuffer[i+2])
            pid3 = ord(mybuffer[i+3])            
            if not (pid1 & 16 or pid1 & 8 or pid1 & 4 or pid1 & 2 or pid1 & 1) and (pid2 in channel  or pid2 in channelinfo):
                
                if pid2 in channel: 
                    ch = 0
                elif pid2 in channelinfo: 
                    ch = 1
            
                # Continuity control
                ccount_new[ch] = pid3 - (pid3 >> 4 << 4)
                if ccount[ch]!=-1 and not (ccount_new[ch] == ccount[ch] + 1 or (ccount_new[ch] == 0 and ccount[ch] == 15)):
                    print "out of sync at ID %s" % ch
                    # Out of sync! 
                    payload[ch] = payloadSort(payload[ch], False)
                    analyse[ch] = True                                     
                ccount[ch] = ccount_new[ch]
                # Continuity control ends
                
                tmp = mybuffer[i+4: i+size]
                # Save first payload to avoid duplicity
                if myfirstpayload[ch] == "": 
                    myfirstpayload[ch] = tmp
                elif tmp == myfirstpayload[ch]:    
                    # Payload match encountered
                    print "Payload %s match encountered" % ch
                    payload[ch] = payloadSort(payload[ch], True)
                    analyse[ch] = True
                 
                # Data analyse and matching
                if analyse[ch]:     
                    plist = getList(payload[ch], ch)
                    if len(plist)>len(maxlist[ch]):
                        maxlist[ch] = plist
                    myfirstpayload[ch] = tmp
                    payload[ch] = ""                                        
                    analyse[ch] = False
    
                payload[ch] = payload[ch] + tmp
            
    return maxlist

# shift or cut the payloads to get the package beginning 
def payloadSort(payload, match):
    pos = payload.find(chr(255)+chr(255)+chr(255)+chr(255))
    if match:
        payload = payload[pos:] + payload[:pos]
    else:
        payload = payload[pos:] 
    return payload

    
def getList(payload, ch):
    chl = list()
    if ch == 1:
        chl = getChannelList(payload)
    else:
        chl = getGuides(payload)
    return chl
    
################################################################################
# Beginning with the analyse of the binary data
# Payload 0 = Guide information
    
def getGuides(pl):                     
    guides = list()

    try:    
        # Sorting the tables, taking 5* and 6* tables only.
        guidetext = ""
        pos0 = -1
        pos1 = -1       
        for i in range(0, len(pl)-4):
            if ord(pl[i]) == 0xFF and ord(pl[i+1]) == 0xFF and ord(pl[i+2]) == 0x00:
                pos1 = i + 2
                if pos0 != -1:
                    guidetext = guidetext + "////" + ( pl[pos0+1:pos1] )
                    pos0 = -1 
                if ord(pl[i+3]) >> 4 == 5  or ord(pl[i+3]) >> 4 == 6:
                    pos0 = i+2
                    
        # Separating the tables into a list 
        guidelist = guidetext.split("////")
        
        for guide in guidelist:
            if len(guide)>14:
                pos = 0
                slen = (  ord(guide[pos+1])  - (ord(guide[pos+1]) >> 4 << 4 ) )*256 + ord(guide[pos+2])
                # Channel ID 
                sid = ord(guide[pos+3])*256 + ord(guide[pos+4])                        
                pos = pos + 14
                while pos < slen-10:                
                    #try:
                    #eid = ord(guide[pos])*256 + ord(guide[pos+1]) # Event ID 
                    start = mjd_to_local(guide[pos+2:pos+7])
                    duration = str_to_delta(guide[pos+7:pos+10]) 
    
                    
                    dlen = (  ord(guide[pos+10])  - (ord(guide[pos+10]) >> 4 << 4 ) )*256 + ord(guide[pos+11])
                    if dlen>0:
                        pos2 = pos + 17
                        # Steuerbyte for several descriptions (?)
                        stb = guide[pos2+1]
                        if stb==chr(05): # several descriptions / lines available
                            desc = ""
                            desccnt = 0
                            while pos2<pos+12+dlen-1: 
                                if guide[pos2]==chr(0x4E):    
                                    pos2 = pos2 + 7
                                elif guide[pos2]==chr(0x50) or guide[pos2]==chr(0x54) :    
                                    break;
                                dlen2 = ord(guide[pos2])
                                if dlen2<=0:
                                    break
                                    
                                if desccnt == 1 or desccnt == 2:
                                    desc = desc + "\n" + guide[pos2+2:pos2+1+dlen2] 
                                else:
                                    desc = desc + guide[pos2+2:pos2+1+dlen2] 
                                
                                desccnt = desccnt + 1
                                pos2 = pos2+dlen2+1
                        else: # only one description available
                            dlen2 = ord(guide[pos2])
                            desc = guide[pos2+1:pos2+1+dlen2]
                            
                        guides.append([sid, start, duration, unistr(desc)])                        
                        
                    pos = pos + dlen + 12                    
        
    except:
        pass
    return guides

################################################################################
# Payload 1 - Channel info
# 0x42 and 0x46 tables are to be taken

def getChannelList(pl):
    channellist = list()
    try:    
        splittables = pl.replace(chr(0xFF)+chr(0x00)+chr(0x46),chr(0xFF)+chr(0x00)+chr(0x42)).split(chr(0xFF)+chr(0x00)+chr(0x42))
        for table in splittables:
            pos =  table.find(chr(255)+chr(255)+chr(255)+chr(255))
            if pos!=-1:
                table = table[:pos]
            # avoid duplicate headers
            header = table[0:10]
            pos = table.find(header, 10)
            if pos!=-1:
                table = table[pos:]
    
            pos = 10
            
            dlen = 0                
            while pos < len(table)-4:
                cid = ord(table[pos])*256 + ord(table[pos+1])
                dlen = (  (ord(table[pos+3]) >> 4 << 4 )- ord(table[pos+3])  )*256 + ord(table[pos+4])
                if dlen < 0: 
                    break
                #print pos, len(table)-4
                
                i = pos+6
    
                if table[i-1]=='V' or table[i-1]=='H':
                    i = i + 2
                clen = ord(table[i])
                provider = table[i+1: i+clen+1].replace(chr(0x86), "").replace(chr(0x87), "").replace(chr(0x05), "")
                i = i + clen + 1
                clen = ord(table[i]) 
                          
                channame = table[i+1: i+clen+1]            
                channame = channame.replace(chr(0x86), "").replace(chr(0x87), "").replace(chr(0x05), "")
                                
                if channame!=".":
                    channellist.append([cid, provider, channame])
                    
                pos = pos + 5 + dlen
    except:
        pass
    
    return channellist
   
def savePayloads(payloads):
    for i in range(0, 2):
        f = open("out-%s.hex" % i, "wb")
        f.write(payloads[i])                    
        f.close()

def loadPayloads():
    payloads = ["",""]
    for i in range(0, 2):
        f = open("out-%s.hex" % i, "rb")
        payloads[i] = f.read()                    
        f.close()
    return payloads    

from operator import itemgetter
def getFullList(f):
    fulllist = list()
    
    lists = read_stream(f)
    guides = lists[0]
    channellist = lists[1]

    #print "guides %s" % (len(guides))
    for g in guides:
        print g[0], g[1], g[2], g[3]
        

    #print "channellist %s" % ()
#    for g in channellist:
#        print g[0], g[1], g[2]

    for l in guides:
        for c in channellist:
            if l[0] == c[0]:
                fulllist.append([c[2], l[1], l[2], l[3]])
                break
    fulllist = sorted(fulllist, key=itemgetter(0,1,2))
    
#    for i in range(0, len(fulllist)-1):
#        if fulllist[i][0]==fulllist[i+1][0]:
#            if fulllist[i][1] + fulllist[i][2] != fulllist[i+1][0]:
#                print "aha!"
                
#    for x in fulllist            
#    fl2 = list()

    print "EPG grab finished with %s channels, %s guide infos, joined amount: %s" % (len(channellist), len(guides), len(fulllist))
    
    return fulllist
  
def main(argv=None):
#    cls()
    inp = None
    if argv is None:
        argv = sys.argv    
    if len(argv)>1:
        try:            
            if argv[1].find("://")!=-1: # URL
                print "EPG grabbing started on %s" % argv[0]
                inp = urllib2.urlopen(argv[1]) 
            else:
                inp = open(argv[1], "rb")
        except:
            print "Supplied file/stream could not be found, aborting..."
            return
    else:  # default
        #inp = open("test.mpg", "rb")
        #inp = urllib2.urlopen("http://192.168.0.20/stream/tunerequest00040000C0FFFFFF00B82C70000100FF0085001B010102FF")
        inp = urllib2.urlopen("http://192.168.0.20/stream/tunerequest00040000C0FFFFFF00B9F960044100FF00012F08010101FF") # RTL
        
    fulllist = getFullList(inp)

#    for l in fulllist:
#        print "%s\t%s\t%s\t%s" % ('{0: <18}'.format(l[0]), l[1], l[2], l[3].split("\n")[0][0:20] )
    #    print l[0], l[1], l[2], l[3]

    inp.close()
    return fulllist

if __name__ == "__main__":
    sys.exit(main())
