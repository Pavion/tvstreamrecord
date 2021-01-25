![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image001.png)
# tvstreamrecord

## Table of contents

- [Introduction](introduction)
- [External links ](external-links-)
- [Installation on Synology NAS](installation-on-synology-nas)
- [Installation in Docker](installation-in-docker)
  - [using Docker on Synology ](using-docker-on-synology-)
- [Configuring this package](configuring-this-package)
  - [General configuration tab](general-configuration-tab)
  - [EPG configuration tab](epg-configuration-tab)
  - [FFMPEG support tab](ffmpeg-support-tab)
  - [Advanced tab](advanced-tab)
- [Using this package](using-this-package)
  - [Channels page](channels-page)
  - [Records page](records-page)
  - [EPG chart page](epg-chart-page)
  - [EPG list page](epg-list-page)
  - [Log page](log-page)
  - [Mobile view](mobile-view)
- [Further information](further-information)
  - [FFMPEG support](ffmpeg-support)
  - [EPG import](epg-import)
  - [License and disclaimer](license-and-disclaimer)
  - [Troubleshooting](troubleshooting)
  - [Modifying the package](modifying-the-package)
- [Contact and support information](contact-and-support-information)

## Introduction

This software is useful for setting recurrent recordings with your favorite streaming device (e.g. Fritz!Box Cable) or provider (e.g. MagentaTV). This software uses ffmpeg as a recording library and supports TV-Browser with corresponding plugin.

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image002.jpg)

## External links 

Following links are provided for companies and projects mentioned in this readme:

- Python: https://www.python.org/
- Synology and DSM6/7: https://www.synology.com/
- Docker: https://www.docker.com/
- ffmpeg: https://ffmpeg.org
- TV-Browser: https://tvbrowser.org/
- mc2xml: http://mc2xml.awardspace.info/

## Installation on Synology NAS 

This package requires Python (preferably Python3), which is preinstalled with DSM7 and can be installed from your Package Center on DSM6 and below. 

For DSM6 please open your Package Center, navigate to the Utilities tab, select any Python version and click Install. Python must not be started and will also create no icon in your Main Menu as it runs on demand only. You've done it, if it looks like this: 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image003.jpg)

In order to install this package please click on Settings button in your Package Center, navigate to the Package Sources tab and click the Add button. Please add our community package hub www.cphub.net as shown below (name may vary): 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image004.jpg)

Click OK to close this window and the one below and click Refresh button in your Package Center. After a short refresh time you should see a Community tab. Click it and scroll down to find the package tvstreamrecord as shown below. Click Install.

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image005.jpg)

You will now be prompted for creating a new share where your settings database and recorded video will be found. Default share `tvstreamrecord` is recommended. If already exists, this share will be reused. No data will be deleted or lost upon installation, deinstallation or upgrade of this package. If you wish to uninstall the package, you will have to delete the new share from Control Panel manually.

Please start the package if it's not running. You should now see a corresponding icon in your Main Menu.  Click it and you are ready to move on and start configuring the package.  Please note, that you can also bookmark any package page to have a quick access to it. 

## Installation in Docker

This tool now moves towards Docker, which will offer images based on master branch. 
Settings:

- Internal port: `8030/TCP`
- Internal mount (changeable): `/volume1/common`

Latest image can be pulled with:

```
docker pull pavion/tvstreamrecord:latest
```

or run with all required arguments: 

```
docker run --daemon -v /videos:/volume1/common --publish 8030:8030 --name tvstreamrecord pavion/tvstreamrecord
```

### using Docker on Synology 

- Install official Docker package from Package Center and open it
- Go to Image and select Add > Image from URL
- Enter `pavion/tvstreamrecord` with no credentials and press Add
- Wait until the installation is completed, select the new image and press Launch
- Change container name and press Advanced Settings
- Volume tab > Add folder > select your target folder then enter `/volume1/common` as mount path
- Port settings tab > change local port from Auto to 8030 (or any other port)
- Press Apply then Next then Apply to create and launch your container
- You should now see a new running container which contains all you should need

## Configuring this package

### General configuration tab

This section covers the general configuration, which is enough to start recording plain streams. Please open the package's web interface and navigate to the Config page. You are now seeing some general options you should consider. Press Submit changes to accept or reload this page to undo all changes.

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image006.jpg)

**Path for your recordings** is a vital setting and should be set. If you're using a Docker or Synology DSM7 you should not change the default share. With other systems you can use any shared folder, which can be accessed with the root user (default: `/volume1/common/`). You can type your desired path in the corresponding box or use the Browse button to select one from the list. 

**File extension for the recorded stream** will be added as a suffix to the filename. It can be vital for [ffmpeg](ffmpeg.org) to detect your stream type. 

**Interface theme** specifies the theme for the web interface to be used. Please select your favorite look and feel from the provided list. 

**Interface language**. As of now, three languages are supported (English, German and Russian).

**Interface locale** adds local date/time support for several countries. Please select your desired locale or the default one. 

**Set remote access password** can be used to provide an access password for from outside your local network. Local connections don't require a password. Warning: entering wrong password three times will block your current IP for at least 48 hours. To disable a password query again just type nothing in the corresponding fields. Please note that you might need to forward the package port (default: TCP/8030) in your router/firewall configuration. See its respective manual for more details.  

### EPG configuration tab

This section hosts all settings regarding an Electronic Program Guide (EPG). If you don't have an EPG content provider and your streams don't transport any EPG information, you can't use this feature and also don't need to setup anything at this page. 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image007.jpg)

**Lengthen an EPG record** will be used to prolong the record and avoid any small time shifts in TV charts. Please note that your system time will be used for recording and should be exact. 

**Enable XMLTV import** for manual import or to be performed once per day at specified time.

**Initial path for an XMLTV-Import** can be used to import EPG (electronic program guide) from free XMLTV-compatible pages. Please read the corresponding section for more information. 

**Time shift for XMLTV data** can be used to shift all imported EPG data by some hours (positive or negative value). That can be useful if importing EPG data from another time zone.

**mc2xml full command line** is for using a third party tool mc2xml). Please consult its page for more information regarding installation and configuration of this tool. If properly configured, corresponding output should be redirected into a local file, which is to be specified under Initial path for an XMLTV-Import. Please read the corresponding section for more information. 

**Time to perform daily EPG/XMLTV grab** can be used to automatically refresh your EPG guide using your streams and/or your XMLTV provider. Please read the corresponding sections for more details.

**Keywords for creating automatic records**. If these keywords are found during EPG data import, corresponding records will be created automatically (max. 100 records per import). Keywords must be separated with comma and are not case sensitive. Please use as exact keywords as possible to prevent wrong record creation. 

**Display additional overlay** can be toggled on to display real record duration overlay in EPG chart view even for channels without EPG data.

**EPG list mode**. Disabled for classic client side processing with greater network load, enabled for server side processing with greater server load but lesser traffic. Using client side processing you can reduce a maximal number of events to request to reduce your network throughput and server load.  

**Delete/reset all EPG data** can be used to clear your database in case of EPG issues

### FFMPEG support tab

This part offers a few settings regarding ffmpeg support. For advanced information and some usage examples please check the corresponding section of this manual. 
 
![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image008.jpg)

**Full path to ffmpeg** is required for this package to work but is not included with this software. On Synology DiskStation ffmpeg is preinstalled with Video and Media Stations. In most cases leaving the default value should be enough. With some protocols other versions may need to be used. In this case please check the corresponding section of this manual. 

**Use legacy recording method for http streams**. Some older devices offering http protocol (such as NetStream) can be recorded without ffmpeg using plain stream copy. This method is deprecated and should be used only if required.  

**Additional output arguments for ffmpeg** can be used to change your output, to encode or to decode your stream on the fly or to display additional output information from ffmpeg.

**Enable proxy for ffmpeg** enables proxy processing using following **Proxy URL** for ffmpeg.

### Advanced tab

This section covers a few advanced settings, which shouldn't normally be changed. 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image009.jpg)

**Full filename for tvstreamrecord database** can be changed to move or set the database for tvstreamrecord. For Docker and DSM7 installation the database will be moved automatically to the new share, on other systems it will be kept in the same folder. Changing the path will try to use the database if found or move the database there if not exists. 

**Purge database records** is used to automatically delete old EPG and records information after some time supplied 

**Server bind address**. Default `0.0.0.0` will make your server available from any local address. Any other choices (e.g. `127.0.0.1`) may be used to limit the access. Changing this setting requires package restart (stop and start using Package Center on Synology NAS).

**Server port is the port the server runs on**. Changing it also requires package restart. 

**Record name/path mask** is used to name resulting files according to placeholders. It can also be used to create subfolders (for example: %channelid%/%date%-%title%). Following placeholders are supported:

- `%date%`: classical time stamp placeholder YYYYMMDDHHMMSS
- `%title%`: record title placeholder (mostly alphanumeric)
- `%fulltitle%`: full record title placeholder with extended character support (UTF-8) 
- `%year%`, `%month%`, `%day%`: separate year, month and day placeholders YYYY, MM, DD
- `%channelid%`: channel ID placeholder

**Reset log** should be used to clear your log file if it's becoming too big or on output issues.

**Retry count for failed records** will retry failed records X times, useful on unstable connections.  

**Do not restart ffmpeg if that much seconds remains** to prevent creation of small files in case of premature termination. Some streams are buffering their data for some seconds so that a 50 seconds recording may still contain 60 seconds data, which is an expected behavior.  

**Enable postprocessing** and its **command** can be enabled and used for advanced video/audio postprocessing or for indexing the resulting file. Default value will index the new file for using with Synology Video/Media Station. Placeholder `%file%` for full filename. 

**Enable concurrent recording** is turned on by default. Please turn it off, if your stream provider supports just one stream per device. In this case all running records will be stopped as soon as a new one is to be started. 

**Alternative URL can be used**, if you have two identical devices, supporting one stream at a time each. In this case alternative URL will be used, if primary URL is already in use. Concurrent recording should be enabled.

**Password-free IPs** are used to bypass password while accessing this package from a LAN network and can be extended with other static IPs.

## Using this package

Here you will get a quick guide for the web interface. For configuration page please check the corresponding section of this manual. 

### Channels page

Here you can add, delete, import, enable or disable your channels. Disabled channels are not visible at Records or EPG pages.
The Controls column shows (left to right): a switch for enabling or disabling a particular channel, a play icon to create a record with this channel and a gear icon to edit or delete this channel. 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image010.jpg)
 
As for now you have two ways to add channels. You can normally add a channel by providing its ID, name, URL and file extension or you can import a .m3u playlist provided within your device as long as it has following syntax:

```
#EXTM3U
#EXTINF:0,channel name 1
http://10.0.0.1/stream/tunerequest000000000000000000000000000000000000000000000000
#EXTINF:0,channel name 2
http://10.0.0.1/stream/tunerequest000000000000000000000000000000000000000000000001
```

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image011.jpg)
![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image012.jpg)

**Please note, that adding a new playlist without appending will erase all old channels and records as well, due to the possibility of ID conflict!**

You can add/change a resulting file extension while creating new channels. With ffmpeg, file extension may be crucial for determining your output type. While importing from .m3u you can't specify any file extension. In case of empty extension the default one from configuration will be used automatically. 

Once added, you can edit and move your channels. To do this, please click on the gear symbol at the right of the table row. You're now able to edit the channel information as well as to assign a new ID. Using an existing ID will insert the current record before this ID and re-enumerate the others. 

You can also delete your channel from here. Please note, that deleting a channel will also delete all associated records. 

### Records page

Here you can schedule your records, turn them on and off, edit or delete them. You can also schedule recurrent records if weekdays are provided. Unlike 'normal' records, which are done after completion, here the next runtime will be automatically calculated and set. 

The Controls column shows (left to right): a progress bar for running records, a switch for enabling or disabling a particular record and a gear icon to edit or delete the record. 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image013.jpg)
![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image014.jpg)
 
### EPG chart page

If available, your Electronic Program Guide (EPG) is presented here in a chart form for a current or a selected date. You can disable a channel by clicking on an X icon next to its name. You can highlight events with specified keyword. You can also manually trigger EPG import from here (see the corresponding section of this manual for more information).

By clicking on an event you can either Record it, which will automatically create a record and redirect you to the Records tab, or you can Edit&Record your event, which will allow you to change record parameters and will not redirect you away. 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image015.png)

You can also use the zoom slider to enlarge the view or Flip chart to switch to the vertical view:

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image016.png)

### EPG list page

If available, your Electronic Program Guide (EPG) is presented here in a table form. You can search within this table and you can record your event (or stop records) directly as well. You can also manually trigger EPG import from here (see the corresponding section of this manual for more information).

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image017.png)

You can also bookmark your favorite searches by adding search keyword to your current URL, for example:

`127.0.0.1:8030/epglist&beach`

will always display events containing the keyword `beach`.

### Log page

Here you can see server side debug information. Please check this page if you encounter a behavior you can't explain. Please also consult the corresponding section of this manual.  

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image018.jpg)

### Mobile view

This is a mobile version of your record page. Here you can access most of the features of the desktop version including recording from EPG (if available). You can also create a shortcut icon on the home screen of your mobile device. 

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image019.jpg)![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image020.jpg)![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image021.jpg)
    
You will be automatically redirected to this view from the page root if you are using a handheld device. You can also access this view with a corresponding icon in the top left corner of the desktop version menu. Please note, that you must have some channels created to make use of this view. For that please check the corresponding section of this manual. 

## Further information

### FFMPEG support

This section covers most issues with ffmpeg streams. I ask to understand, that ffmpeg is neither part of this package nor can ffmpeg developers provide support for this package. This package simply provides a front end for this console based tool. All the advanced settings in this section may also require advanced skills in dealing with console applications.

On Synology systems ffmpeg is preinstalled and is normally called with `ffmpeg` only, which is the default setting. If it doesn't work, you may need to install the corresponding package and provide the full path for: 
VideoStation: `/volume1/@appstore/VideoStation/bin/ffmpeg`
MediaServer: `/volume1/@appstore/MediaServer/bin/ffmpeg`

Even if your system has ffmpeg installed, it may not support your stream type or protocol (e.g. Synology ffmpeg has no support for https). If you want to be sure, please visit http://ffmpeg.org/, download and extract the corresponding release and provide its full path in the configuration. Thus you can be sure to have the latest and fullest release available. For example, for x64 based Synology and other NAS you can use the file `ffmpeg-release-amd64-static.tar.xz` from https://johnvansickle.com/ffmpeg/.

Global rule is: if you can play your stream with your favorite media player, you should be able to record it with ffmpeg. If you have a terminal access to your system, you can do following steps in your terminal. Make sure that you have ffmpeg properly installed by typing and running: 

``` 
> ffmpeg 
```

from the console. You should see following output (only first line is displayed here):

![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image022.png)

Check your stream foo://10.0.0.1:1000 with a following command:

```
> ffmpeg -i foo://10.0.0.1:1000 -t 30 -acodec copy -vcodec copy out.mpg
```

This tells ffmpeg to save your stream (`-i streamaddress`) for a duration of (`-t xx`) seconds by copying audio (`-acodec copy`) and video (`-vcodec copy`) into an output file (`out.mpg`). If it works, you should see a lot of output text for the duration of 30 seconds and be able to locate the generated file in your current folder. 
 
![Image](https://raw.githubusercontent.com/Pavion/tvstreamrecord/gh-pages/readme/image023.png)
 
Otherwise you should check for any errors in console output. Make sure that you've provided a correct extension for your stream (.ts, .mpg, .avi, .mk4, .mkv and such): ffmpeg uses this to determine output file type. Look into ffmpeg documentation and experiment with your stream until you get your file.

If you want to provide additional output arguments for ffmpeg (`-f` for stream format or other codecs parameters), you can also do it at the Config page. First arguments are always `-i inputstreamname`, `-t recordduration`and last argument is `outputstreamname.extension` (you will see all arguments used at the Log page after each ffmpeg trigger).

You can now create a channel with some name, your stream address and your file extension and schedule some records.

Common parameter and their meaning:

`-f fmt` forces ffmpeg to use specified format (e.g. h264, mpg, mkv, avi)
`-loglevel quiet/fatal/error` can be used to provide (or restrict) additional log output
`-map 0:v -map 0:a` can be used to force all tracks (video and audio) of a stream to be recorded. Per default only one audio track might be recorded. 
`-ignore_unknown` ignores invalid stream parts (reported to be required for Fritz Box 6490 Cable) 

### EPG import

There are two ways to get EPG information. Please read this section carefully to avoid issues. 

**The first way** is to use third party EPG data, which is provided in XML format (XMLTV). 
If you have a free XMLTV provider from your region, you should add its address in Config > EPG. Now you should be able to import EPG by pressing the corresponding button or by enabling the automatic synchronization. As of now there is no direct feedback for this feature and full synchronization takes some time, so please check the log file for the progress or error status. 
If you are using their data, please consider to support them and their respective communities and to spread the word.  

If you don't have any free XMLTV provider and an x86 CPU, you may want to try using a third party tool mc2xml). For Synology you must download a latest Linux version in any public accessible folder. Browse the homepage of mc2xml) for more information regarding setup, accessing and running this tool. You must run it once manually to create a configuration file. Once properly configured, you can change following settings in Config > EPG to match your setup. For example:
- mc2xml full command line: `/volume1/public/mc2xml -D /volume1/public/mc2xml.dat -o /volume1/public/xmltv.xml -U`
- Initial path for an XMLTV import: `/volume1/public/xmltv.xml`
Note: use absolute paths everywhere to avoid path issues.

mc2xml) is a fully separate tool and so no further integration or support can be provided here. If you are using this tool, you should also consider to support and/or donate to its respectful author. 

In both cases  channel names you're using should match with those provided by your XMLTV provider (e.g. please use 'CNN' and not '1 - CNN' or 'epg.cnn.com' or 'My favorite news channel'). You can see those, if you open your provider's URL in a common web browser and search for corresponding `<display-name>` tag, for example:
`<display-name lang="en">CNN</display-name>`

The second way is to use a third-party EPG desktop software TV-Browser. With a [corresponding plug-in](https://www.tvbrowser.org/index.php?id=remotesoft) this package can be controlled remotely. Please visit [TSRPlugin page](https://pavion.github.io/TsrPlugin/index.html) for more information.

### License and disclaimer

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see http://www.gnu.org/licenses. 
Please note that the recording, keeping or distribution of streams may be forbidden by the law of your country or your local content provider. Author takes no responsibility for any records taken or used. 
If you are using XMLTV source for your EPG guide, please make sure, that your source provider allows accessing his data with third party applications.

Following packages and modules are licensed under their respective licenses. 

- Python
- [Bottle: Python Web Framework](https://bottlepy.org/)
- [CherryPy - A Minimalist Python Web Framework](https://cherrypy.org/)
- [Six](https://github.com/benjaminp/six)
- [SQLite](https://www.sqlite.org/)
- [jQuery](https://jquery.com/) and further based-on themes, modules and locales:
  - [jQueryUI](https://jqueryui.com/)
  - [jQuery Mobile](https://jquerymobile.com/)
  - [jQuery Mobile DateBox](http://dev.jtsage.com/DateBox/)
  - [SlickSwitch](https://github.com/LukeKirby/jQuery-slickswitch)
  - [DataTables](https://datatables.net/)
  - [TimePicker](https://timepicker.co/)
  - [File Tree](https://www.abeautifulsite.net/jquery-file-tree)
  
Some code snippets are taken from or inspired by several community help pages, tutorials, code samples and so on. I want to thank all the developers and contributors, whose work helped me so far.

### Troubleshooting

If you encounter an undefined error, please check the package log file. You can access it either by using the package frontend and navigating to the Log tab or by opening the 'log.txt' file. On Synology systems you can also open a Package Center, navigate to Installed tab, click on tvstreamrecord and select View log. The newest entry may give you a clue what went wrong. If it doesn't help, please contact me. 
If you encounter any issue with EPG or Log pages, you can reset both at the Config page.

### Modifying the package

Although this package is open sourced, author takes no responsibility for any damage resulting from altering or updating the source code of this package. If you're using a Docker or Synology repository, any changes you've made will be overwritten with a new version of this package. 

The best way to get this package altered is to contact author and provide your solution or addition. If you have a shell access to your DiskStation and you know what you do, you can still customize this package:

- You can add further [jQueryUI themes](http://jqueryui.com/themeroller/) by copying them into the css folder of this package 
- You can add or change locales in the js\i18n folder 
- You can add or change languages in the lang folder (see supplied dummy for more details)

If made correctly, you must be able to select your addition with reopening or refreshing a Config page. You can also send me your own translation to be included in following versions. 

## Contact and support information

If you have any questions, issues, ideas or feedback, feel free to contact me using one of the following ways:

- [German Synology community forum](http://www.synology-forum.de/showthread.html?37898)
- [E-Mail](mailto:tvstreamrecord@gmail.com) (support languages: English, German, Russian)
- GitHub users can also [open an issue](https://github.com/Pavion/tvstreamrecord/issues), comment my code or contact me there

**Feedback appreciated.** 
