# OpenScanCloud
Photogrammetry Web API

## Overview / Outline:
The OpenScan Cloud is intended to be a decentralized, open and free photogrammetry web API. 

The API can be used as a great addition to existing photogrammetry rigs like the OpenScan Mini or Classic but also any other rig. The only things needed to start a reconstruction are a user-specific (or public) token and of course an image set (preferably as a zip file).

I would also like to create a Desktop uploader, so that users can choose an image set, which then gets uploaded. As I have no experience with creating a Desktop GUI (besides node-red-dashboard ;)) I would highly appreciate any help on that part.

## Current functionality / http endpoints
Please feel free to add your thoughts on the design. Currently I implemented the following http endpoints:

- ### /createProject(token, project, photos, parts, filesize)
Calling this endpoint will initialize a project of a given *project* name, consisting of a certain number of *photos*, split into x *parts* and having a total *filesize*. If a project is larger then 200Mb it needs to be split into several parts as this is the current upload endpoints filesize limit.

If successful it will return statuscode 200 + *{'status':'created', 'ulink':[list of uploadlinks], 'credit':credit_used}* , where the uploadlinks are valid for 4 hours.

- ### /startProject(token, project)
Once a project is created and all part(s) are successfully uploaded, it is necessary to initialize the processing of the image set by calling this endpoint, which will return *{'status':'started'}*

- ### /getProjectInfo(token, project)
Calling this endpoint will return *{'dlink':downloadlink, 'status':status, 'ulink':uploadlinks}*. Note that with the public access token, anybody could guess the project name and thus gain access to the download link. Therefore it is highly adviced to use some randomized project name.

- ### /getTokenInfo(token)
Will return *credit, limit_filesize* and *limit_photos* for the given token.

## Token and credit system
### Credit
Credit will be used to monitor the overall usage of processing ressources. The credit value is bound to each token.

### Tokens
- Public Token
There will be a public token, with a certain amount of credit per time (e.g. 10 GB per day or so). People using this token won't have access to additional features like auto-email when the reconstruction is done + individual support. Furthermore the data submitted through this token will be used for further research and improvement of the processing engine (and future features of OpenScan). In case of high loads on the server side, sets created with private tokens might be prioritized (at some point in the future)

- Private Token
This token is bound to an individual and certain details (forename and surname and email address) in order to allow additional features, like email alerts and individual support.

## Discusion

Please feel free to share your thoughts and let me know if you need any additional information.

I will add a working python example soon :)
