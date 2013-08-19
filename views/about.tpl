%include header 

<div id="about">
<p><b>Tvstreamrecord v.{{ver}}</p></b>

<p><b>Quick guide</b></p>

<ol>
<li><p><b>Introduction</b></p>
<p>This software was designed to record http streams (TV and such). My goal was to be able to record streams from Elgato EyeTV Netstream with my NAS server so it's the primary objective of this software. Please note, that this software can't be used to record any videos from USB-based devices. A simply stream would be http://streamadress/stream000000 and will be recorded or grabbed as is. </p>
<p>As reported, streams from Dreambox (800 HD) can also be used. Its stream URL should be like: <i>http://192.168.0.10:8001/1:0:1:6DCA:44D:1:C00000:0:0:0:</i></p>
<p>Please note, that the recording of some streams may be forbidden by the law of your country or your local content provider. Author takes no responsibility for any records taken.</p>
</li>
<li><p><b>Installation on Synology DS systems</b></p>
<p>Installation in Synology DS systems via community hub <a href="http://www.cphub.net">http://www.cphub.net</a>. Please insert it as package source in your DS Package Center and you will see my software under "other sources"</p>
<p>Please make sure that you have <a href="http://www.python.org/">Python 2.x</a> installed on your DS (not compatible with Python 3.x). Note that if you install Python for the first time, you may need to restart your DS.</p>
<p>Make sure that my software has been started by DS.</p>
</li>
<li><p><b>Installation on other systems</b></p>
<p>You can download a .zip file from my <a href="http://code.google.com/p/tvstreamrecord/">project page</a>. Simply install <a href="http://www.python.org/">Python 2.x</a> for your system and you'll be able to start my software with the following command:<br />
<i>python tvstreamrecord.py</i><br />
You shouldn't need any special permissions.</p></li>
<li><p><b>Running for the first time</b></p>
<p>To access the software you should open your favorite browser and navigate to your target IP with the port 8030, e.g. <a href="http://localhost:8030">http://localhost:8030.</a> Now you should see the web based page of my software. First you should proceed to the config page and review following settings:</p>
<li><p><b>Settings</b></p>
<p><i>Initial path for an XMLTV-Import</i> can be used to import EGP (electronic program guide) from free XMLTV-compatible pages. The default value is the only one tested at this time.<br />
<i>Purge database records</i> will be used to automatically delete old EPG and records information and shouldn't normally be changed<br />
<i>Lenghten an EPG record</i> will be used to prolong the record and avoid any small time shifts in TV charts. Please note, that your system time will be used for recording and should be exact.<br />
<i>Path for your recordings</i> is a vital setting and should be set. On Synology DS you can use any shared folder, which can be accessed with the root user (e.g. /volume1/common/). On Windows systems you can use any path (e.g. d:\records\). Be sure to close your path string with an path char (/ or \), as the path string will be added to the filename. Otherwise you can use this to add prefixes to your recordings. As example, providing the path <i>/volume1/films/rec</i> will result in files with names: rec20130101000000<br />
<i>Server bind address</i> is exactly what it says. Default 0.0.0.0 will make your server available from any local address. Any other choices (i.e. 127.0.0.1) may be used to limit the access. This setting should not normally be changed. Changing it requires restart.<br />
<i>Server port</i> is the port the server runs on. You can change it, if you need it. Changing it requires restart.<br />
<i>File extension for the recorded stream</i> will be added to the filename. Mostly it would be MPEG transport stream (.ts). Changing this parameter doesn't change anything beside filename.<br />
<i>Full path to ffmpeg</i> is needed for experimental <i>ffmpeg</i> support. <i>ffmpeg</i> is not included within this software. On Synology DS is <i>ffmpeg</i> preinstalled and the default value should not be changed.<br />
<i>Stream types</i> would be forwarded to ffmpeg. If your stream can be recorded with, you can add its prefix here.<br />
<i>Additional output arguments for ffmpeg</i> can be used to change your output. Please check next part for details.</p></li>
<li><p><b>FFMPEG support</b></p>
<p>This software can forward your streams to external software <a href='http://www.ffmpeg.org/'>ffmpeg</a> thus providing support for non-HTTP streams. If you can record your stream with ffmpeg, you can also do it through my software. On Synology systems ffmpeg is preinstalled, for other systems please check <a href='http://www.ffmpeg.org/'>ffmpeg</a> page. Here is a small tutorial for checking and adding your stream support:<br />
<ul>
<li>Make sure, that you have ffmpeg installed by running ffmpeg from the console. You should see no error but ffmpeg output. You may need to download and install ffmpeg for your operating system first and provide full path to this installation (e.g. c:\ffmpeg\ffmpeg.exe)</li>	
<li>Check your stream foo://10.0.0.1:1000 with following command:<br />
<i>ffmpeg -i foo://10.0.0.1:1000 -t 30 -acodec copy -vcodec copy out.mpg</i><br />
If it works, you should be able to locate the generated file out.mpg in current folder. Else you should check for any errors in console output. Make sure that you've provided an correct extension for your stream (.ts, .mpg, .avi, .mk4, .mkv and such): ffmpeg uses this to determine output file type. Look into ffmpeg documentation and experiment with your stream till you get your file. I ask you to understand that I'm unable to test any possible stream myself or to provide any technical support for ffmpeg.</li>   
<li>If you've got your file and can play it with your favorite media player, you can now add your stream type at the 'Config' page (e.g. rtmp rtm foo).</li>	
<li>Check your ffmpeg path at config page.</li>	
<li>If you want to provide additional output arguments for ffmpeg, you can also do it in config. First arguments are always <i>-i inputstreamname -t recordduration</i> and last argument <i>outputstreamname.extension</i> (you will see all arguments used in my log file after each ffmpeg recording).</li>	
<li>You can now create a channel with some name, your stream address and your file extension.</li>
<li>Congratulation, you can now start using this software.</li>
</ul>          	
</p>	
<li><p><b>Channels manipulation</b></p>
<p>As for now you have two ways to add channels. You can normally add a channel by providing its ID, name, URL and file extension or you can import an .m3u playlist. 
With Elgato EyeTV Netstream you can export your channel list from the device page and import the file in my software. You can also use other .m3u with following syntax:</p>
<p><i>
<ul>
<li>#EXTM3U</li>
<li>#EXTINF:0,channel name 1</li>
<li>http://192.168.0.10/stream/tunerequest000000000000000000000000000000000000000000000000</li>
<li>#EXTINF:0,channel name 2</li>
<li>http://192.168.0.10/stream/tunerequest000000000000000000000000000000000000000000000001</li>
</ul>
</i></p>
<p><b>Please note, that adding a new playlist without appending will erase all the old channels and records as well, due to the possibility of ID conflict!</b></p>
<p>For using XMLTV the channel names should be the same as those from your XMLTV provider (e.g. 'channel name 1' and not epg.channel1.com). <br />
You can add an file extension while creating new channels. This file extension will be simply added at the end of the file name. If you're using ffmpeg, file extension may be crucial for determining your output type. While importing from .m3u you can't specify any file extension. In case of empty extension the default one from configuration will be used automatically. </p>
<p>Once added, you can edit and move your channels. To do this, please click on the gear symbol at the right of the table row. You're now able to edit the channel informations as well as to assign a new ID. Using an existing ID will insert the current record before this ID and renumerate the others. <br />
You can also delete you channel from here. Please note, that deleting a channel will also delete all associated records. </p>
<li><p><b>EPG import</b></p>
<p>If you have a free XMLTV provider from your region, you should add his address in config. Now you should be able to import EPG by pressing the corresponding button one time. Please just one time. As for now there is no direct feedback for this feature and full synchronisation takes some time, please check the log file for the progress or error status. The only provider tested is <a href="http://xmltv.spaetfruehstuecken.org/xmltv/">Egon zappt</a>. As I'm following <a href="http://www.oztivo.net/twiki/bin/view/TVGuide/StaticXMLGuideAPI">OzTiVo rules</a> to grab EPG data, you can receive new data only, which would normally be refreshed one time a day.</p>
</li>
<li><p><b>Records</b></p>
<p>Here you can create a new record with channel and time provided. You can also pause and delete your recordings. You can also create recurrent records by providing weekdays. This would still be one record only, which can be paused/resumed/deleted. Unlike 'normal' records, which are done after completion, the next runtime will be automatically calculated and set there.</p>
</li>
<li><p><b>Feedback</b></p>
<p>As I'm not able to test my software on every plattform of the world, I beg you for your feedback regarding any issues with my software. Thank you!</p>
</li>
<li><p><b>Thanks</b></p>
<p><ul>
<li>Flouwy for his support and inspiration</li>
<li>Sideshowbob for his ffmpeg support idea and testing</li>
<li>plusulli for his Dreambox feedback</li>
<li>Honu, zamp411 and other supporters for their feedbacktrust</li>
</ul>
</p>
</li>
<ol />
</div>

%include footer         