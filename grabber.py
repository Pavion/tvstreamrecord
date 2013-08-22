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
from datetime import datetime, timedelta, time, date
import time

# converts string into time, i.e. 0x20 0x15 0x15 = 20:15:00 - what a funny way to encode time!
def str_to_delta(str):
    h = int(hex(ord(str[0])).replace("0x",""))
    n = int(hex(ord(str[1])).replace("0x",""))
    s = int(hex(ord(str[2])).replace("0x",""))
    return timedelta(hours=h, minutes = n, seconds = s)

# converts Modified Julian date to local date
def mjd_to_local(str):
                
    MJD = ord(str[0]) * 256 + ord(str[1])
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
    t = str_to_delta(str[2:5]) 
    
    return start + utc_off_delta + t

def read_stream(f_in):
    packagesizes = [188, 204, 208]
    size = -1
    syncbyte = 'G'
    channel = [0x12]
    channelinfo = [0x11]

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
    
    # define number of blocks to be read
    blocktoread = 100
    block_sz = size * blocktoread
    
    # Continuity counter
    
    ccount = [-1, -1]
    ccount_new = [-1, -1]
    payload = ["",""]
    myfirstpayload = ["", ""]
    blocksread = 0
    maxblocksread = 20*1024*1024
    ch = 0
    maxpayload = ["",""]
    
    
    # read until the end or payload match
    match = [False, False]
    
    while False in match:
        mybuffer = f_in.read(block_sz)
        blocksread = blocksread + block_sz  
        if not mybuffer:
            print "Buffer end encountered, data may be incomplete."
            break
        elif blocksread>maxblocksread: 
            print "Timeout at %sMB, data may be incomplete. Largest available payload will be used. " % maxblocksread/1024/1024
            if len(payload[ch])<len(maxpayload[ch]):
                        payload[ch] = maxpayload[ch] 
            break
        for i in range(0, len(mybuffer), size):
            pid1 = ord(mybuffer[i+1])
            pid2 = ord(mybuffer[i+2])
            pid3 = ord(mybuffer[i+3])            
            if not (pid1 & 16 or pid1 & 8 or pid1 & 4 or pid1 & 2 or pid1 & 1) and ((pid2 in channel and not match[0]) or (pid2 in channelinfo and not match[1])):
                
                if pid2 in channel: 
                    ch = 0
                elif pid2 in channelinfo: 
                    ch = 1
            
                # Continuity control
                ccount_new[ch] = pid3 - (pid3 >> 4 << 4)
                if ccount[ch]!=-1 and not (ccount_new[ch] == ccount[ch] + 1 or (ccount_new[ch] == 0 and ccount[ch] == 15)):
#                    print hex(pid2), "Out of sync at ID %s (%s/%s)" % (ch, ccount[ch],ccount_new[ch])
                    # Out of sync! 
                    if len(payload[ch])>len(maxpayload[ch]):
                        maxpayload[ch] = payload[ch]
                    myfirstpayload[ch] = ""
                    payload[ch] = ""                                        
                
                ccount[ch] = ccount_new[ch]
                # Continuity control ends
                
                tmp = mybuffer[i+4: i+size]
                # Save first payload to avoid duplicity
                if myfirstpayload[ch] == "": 
                    myfirstpayload[ch] = tmp
                elif tmp == myfirstpayload[ch]:    
                    print "Payload %s match encountered" % ch
                    match[ch] = True                    
    
                payload[ch] = payload[ch] + tmp

    # shift or cut the payloads to get the package beginning 
    for i in range(0,2):
        pos = payload[i].find(chr(255)+chr(255)+chr(255)+chr(255))
        if match[i]:
            payload[i] = payload[i][pos:] + payload[i][:pos]
        else:
            payload[i] = payload[i][pos:] 
            
    return payload    

    
################################################################################
# Beginning with the analyse of the binary data
# Payload 0 = Guide information
    
def getGuides(pl):                     
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
    guides = list()
#    print len(guidelist)
    
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
                        
 #                   print sid, start, duration, desc
                    guides.append([sid, start, duration, desc])
                pos = pos + dlen + 12                    
    
    return guides

################################################################################
# Payload 1 - Channel info
# 0x42 and 0x46 tables are to be taken

def getChannelList(pl):
    channellist = list()
        
    splittables = pl.replace(chr(0xFF)+chr(0x00)+chr(0x46),chr(0xFF)+chr(0x00)+chr(0x42)).split(chr(0xFF)+chr(0x00)+chr(0x42))
    for table in splittables:
        pos =  table.find(chr(255)+chr(255)+chr(255)+chr(255))
        if pos!=-1:
            table = table[:pos]
        pos = 10
        
        dlen = 0                
        while pos < len(table)-4:
            #print pos, len(table)-4
            cid = ord(table[pos])*256 + ord(table[pos+1])
            dlen = (  (ord(table[pos+3]) >> 4 << 4 )- ord(table[pos+3])  )*256 + ord(table[pos+4])
            if dlen < 0: 
                break
            
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
    
    return channellist
    

          
    
                        
#    f = open("out0.hex", "wb")
#    f.write(payload[0])                    
#    f.close()

#    f = open("out1.hex", "wb")
#    f.write(payload[1])                    
#    f.close()

#    f = open("out0-1.hex", "wb")
#    f.write(guidetext)                    
#    f.close()

   
#
   
#f = open("o:/20130819195200 - Boerse.mpg", "rb")
#f = open("o:/20130821195200 - Boerse.mpg", "rb")
#break
#print localtime()


def getFullList(f):
    fulllist = list()
    
    payloads = read_stream(f)
    
    guides = getGuides(payloads[0])    

    #print guides
#    for g in guides:
#        print g[0], g[1], g[2], g[3]
#    return None
    
    channellist = getChannelList(payloads[1])

    for l in guides:
        for c in channellist:
            if l[0] == c[0]:
                fulllist.append([c[2], l[1], l[2], l[3]])
                break
    
    return fulllist

# using URL
#f = urllib2.urlopen("http://192.168.0.20/stream/tunerequest00040000C0FFFFFF00AF5E8803FB00FF0001283D020301FF")
# using file
f = open("../test.mpg", "rb")

fullist = getFullList(f)

for l in fullist:
    print l[0], l[1], l[2], l[3]

f.close()