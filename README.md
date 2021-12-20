# OpenScanCloud
Photogrammetry Web API

## Overview / Outline:
The OpenScan Cloud is intended to be a decentralized, open and free photogrammetry web API. 

The API can be used as a great addition to existing photogrammetry rigs like the OpenScan Mini or Classic but also any other rig. The only things needed to start a reconstruction are a user-specific (or public) token and of course an image set (preferably as a zip file).

Note that the application is totally free (and hopefully I can keep it free/donation-based in the future). Your data will be transferred through Dropbox and stored/processed on my personal servers. I will use those image sets and resulting 3d models for further research, but none of your data will be published without your explicit consent!

If you like the project, feel free to support my work on [BuyMeACoffee](https://www.buymeacoffee.com/OpenScan)

Thank you :)

## Current functionality / desktop uploader for Windows ( [Download](https://github.com/OpenScanEu/OpenScanCloud/raw/main/uploader/Uploader.win.zip))
![Desktop Uploader for Windows](https://i.imgur.com/jUSTf1o.png)

### KNOWN ISSUE: Unfortunately, for some users the software might time-out when establishing a connection to my servers. This can be identified if it does not change for several minutes... Sorry :) I will try my best to release and update as soon as possible.

The Uploader is a standalone .exe, which should be able to run on any Windows machine. It allows you to select either a folder or a zip file containing images and uploading those to the OpenScanCloud and initialize the processing. All you need is an individual token (apply by email to cloud@openscan.eu) and some images. 

## Current functionality / Beta Firmware for OpenScan Classic & Mini (See [Sourecode](https://github.com/OpenScanEu/OpenScanCloud/blob/main/uploader/firmware_beta.json))
![Firmware for OpenScan Pi](https://i.redd.it/yrmopdyr9ts71.png)

Install the latest Beta Firmware for the OpenScan and OpenScan Mini by running the following command:

```sudo wget -O /home/pi/.node-red/flows_raspberrypi.json https://raw.githubusercontent.com/OpenScanEu/OpenScanCloud/main/uploader/firmware_beta.json && node-red-restart```

You will need to reboot the Raspberry Pi after the install + 1-2mins.

## Current functionality / python uploader (See [Sourecode](https://github.com/OpenScanEu/OpenScanCloud/blob/main/uploader/uploader.py))
The python script can be a starting point to create your own solution. Currently you only need to change a handful of parameters at the beginning of the file. Note, that the 'requests' module is needed (```pip install requests```)

## Current functionality / http endpoints
Please feel free to add your thoughts on the design. Currently I implemented the following http endpoints:

- ### /createProject(token, project, photos, parts, filesize)
Calling this endpoint will initialize a project of a given *project* name, consisting of a certain number of *photos*, split into x *parts* and having a total *filesize*. If a project is larger then 200Mb it needs to be split into several parts as this is the current upload endpoints filesize limit.

If successful it will return statuscode 200 + *{'status':'created', 'ulink':[list of uploadlinks], 'credit':credit_used}* , where the uploadlinks are valid for 4 hours.

- ### /startProject(token, project)
Once a project is created and all part(s) are successfully uploaded, it is necessary to initialize the processing of the image set by calling this endpoint, which will return *{'status':'started'}*

- ### /getProjectInfo(token, project)
Calling this endpoint will return *{'dlink':downloadlink, 'status':status, 'ulink':uploadlinks}*.

- ### /getTokenInfo(token)
Will return *credit, limit_filesize* and *limit_photos* for the given token.

## Token and credit system
### Credit
Credit will be used to monitor the overall usage of processing ressources. The credit value is bound to each token.

### Tokens
- Public Token
There will be a public token, with a certain amount of credit per time (e.g. 10 GB per day or so). People using this token won't have access to additional features like auto-email when the reconstruction is done + individual support. Furthermore the data submitted through this token will be used for further research and improvement of the processing engine (and future features of OpenScan). In case of high loads on the server side, sets created with private tokens might be prioritized (at some point in the future)

- Private Token
This token is bound to an individual and certain details (forename and surname and email address) in order to allow additional features, like email alerts and individual support. At the current stage, the image sets submitted will be used for internal research and testing. No images/3d models will be published.

## Changelog
- 2021-12-20 added Texture to the 3d model + improved firmware
- 2021-10-11 added Beta Firmware for OpenScanPi 
- 2021-10-08 added a Windows Uploader GUI in /uploader
