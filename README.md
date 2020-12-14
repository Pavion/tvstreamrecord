tvstreamrecord
==============

## About

This software is useful for setting recurrent recordings with your favorite 
streaming device (e.g. Fritz!Box Cable) or provider (e.g. MagentaTV). 
This software uses [ffmpeg](https://ffmpeg.org) as a recording library and 
supports [TVBrowser](https://www.tvbrowser.org) (with corresponding plugin). 

## Docker

This tool now moves towards Docker. 
Docker will create images based on commits to master. 

Internal port: `8030/TCP`
Internal mount (changeable): `/volume1/common`

Latest image can be pulled with:

```
docker pull pavion/tvstreamrecord:latest
```

or run with all required arguments: 

```
docker run --daemon -v /videos:/volume1/common --publish 8030:8030 --name tvstreamrecord pavion/tvstreamrecord
```

## using Docker on Synology 

**This is a preview feature**

- Install official Docker package from Package Center and open Docker
- Go to Image and select Add > Image from URL
- Enter `pavion/tvstreamrecord` with no credentials and press Add
- Wait until the installation is completed, select the new image and press Launch
- Change container name and press Advanced Settings
- Volume tab -> Add folder -> select your target folder then enter `/volume1/common` as mount path
- Port settings tab -> change local port from Auto to 8030 (or any other port)
- Press Apply then Next then Apply to create and launch your container
- You should now see a new running container which contains all you should need

Feedback appreciated.
