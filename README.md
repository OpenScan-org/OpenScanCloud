# OpenScanCloud
Photogrammetry Web API

## Overview / Outline:
The OpenScan Cloud is intended to be a decentralized, open and free photogrammetry web API. 

The API can be used as a great addition to existing photogrammetry rigs like the OpenScan Mini or Classic but also any other rig. The only things needed to start a reconstruction are a user-specific token and of course an image set (preferably as a zip file).

Note that the application is totally free (and hopefully I can keep it free/donation-based in the future). Your data will be transferred through Dropbox and stored/processed on my local servers. I will use those image sets and resulting 3d models for further research, but none of your data will be published without your explicit consent!

If you like the project, feel free to support my work on [Patreon](https://www.patreon.com/bePatron?u=51974655)

Thank you :)

## Current functionality / Web Uploader through the browser

![image](https://github.com/user-attachments/assets/d6619cd9-f54c-4795-8ee4-a6e16f038743)

Upload up to 2GB of photos through the Web interface without the need for any additional app!

## Current functionality / desktop uploader for Windows ( [Download ZIP](https://github.com/OpenScanEu/OpenScanCloud/raw/main/uploader/OpenScanUploader.zip))

* updated 2022-05-12 

![image](https://user-images.githubusercontent.com/57842400/168089502-314cec43-0555-49e3-9043-06a5b5068906.png)

Enter your token

![image](https://user-images.githubusercontent.com/57842400/168090093-0900defb-6f92-4978-b2ba-e4946e7882d5.png)

Select your folder and upload the photos to the OpenScanCloud


The Uploader is a standalone .exe, which should be able to run on any Windows machine. It allows you to select either a folder containing images and uploading those to the OpenScanCloud. All you need is an individual token (apply by email to cloud@openscan.eu) and some images. Note, that the program will create a temporary folder and an additional .txt file containing the token in the same directory as the .exe file.

[SourceCode (Python)](https://github.com/OpenScanEu/OpenScanCloud/raw/main/uploader/WindowsUploader.py)

## Current functionality / Beta Firmware for OpenScan Classic & Mini
Uploading through the firmware can be done with one click and has been implemented in all recent firmware versions.
See [Github-OpenScan2](https://github.com/OpenScanEu/OpenScan2/) for more details

## Current functionality / python uploader (See [Sourecode](https://github.com/OpenScanEu/OpenScanCloud/blob/main/uploader/uploader.py))
The python script can be a starting point to create your own solution. Currently you only need to change a handful of parameters at the beginning of the file. Note, that the 'requests' module is needed (```pip install requests```)

## Current functionality / http endpoints
Please feel free to add your thoughts on the design. Currently I implemented the following http endpoints:

# Flask API Reference for OpenScan User

## Authentication

This API uses HTTP Basic Authentication. The following credentials are required for access:

- Username: `openscan`
- Password: `free`

Unauthorized access will result in a 401 Unauthorized response.

## Endpoints

### 1. Request Token

Request a new token for access to the service.

```
GET /requestToken
```

#### Parameters

| Name     | Type   | Description                    |
|----------|--------|--------------------------------|
| mail     | string | Email address of the requester |
| forename | string | First name of the requester    |
| lastname | string | Last name of the requester     |

#### Responses

| Status | Description                                |
|--------|--------------------------------------------|
| 200    | Success. Returns an empty object `{}`      |
| 400    | Bad Request. Missing fields or unknown error |

### 2. Get Token Info

Retrieve information about a specific token.

```
GET /getTokenInfo
```

#### Parameters

| Name  | Type   | Description                        |
|-------|--------|------------------------------------|
| token | string | The token to retrieve information for |

#### Responses

| Status | Description                                |
|--------|--------------------------------------------|
| 200    | Success. Returns JSON object with token info |
| 400    | Bad Request. Missing token or token doesn't exist |

#### Success Response Fields

- `credit`
- `limit_filesize`
- `limit_photos`

### 3. Get Project Info

Retrieve information about a specific project.

```
GET /getProjectInfo
```

#### Parameters

| Name    | Type   | Description                     |
|---------|--------|---------------------------------|
| token   | string | The token associated with the project |
| project | string | The project identifier          |

#### Responses

| Status | Description                                |
|--------|--------------------------------------------|
| 200    | Success. Returns JSON object with project info |
| 400    | Bad Request. Missing fields or token doesn't exist |
| 401    | Unauthorized. Project doesn't exist        |

#### Success Response Fields

- `dlink` 
- `status`
- `ulink`

### 4. Create Project

Create a new project associated with a token.

```
GET /createProject
```

#### Parameters

| Name     | Type    | Description                      |
|----------|---------|----------------------------------|
| token    | string  | The token to associate with the project |
| project  | string  | The project identifier           |
| photos   | integer | Number of photos                 |
| parts    | integer | Number of parts                  |
| filesize | integer | File size                        |

#### Responses

| Status | Description                                |
|--------|--------------------------------------------|
| 200    | Success. Returns JSON object               |
| 400    | Bad Request. Various error conditions      |

#### Success Response Object

```json
{
  "status": "created",
  "ulink": [array of upload links],
  "credit": remaining credit
}
```

### 5. Reset Project

Reset an existing project.

```
GET /resetProject
```

#### Parameters

| Name    | Type   | Description                     |
|---------|--------|---------------------------------|
| token   | string | The token associated with the project |
| project | string | The project identifier          |

#### Responses

| Status | Description                                |
|--------|--------------------------------------------|
| 200    | Success. Returns an empty object `{}`      |
| 400    | Bad Request. Missing fields or doesn't exist |

### 6. Start Project

Start an existing project.

```
GET /startProject
```

#### Parameters

| Name    | Type   | Description                     |
|---------|--------|---------------------------------|
| token   | string | The token associated with the project |
| project | string | The project identifier          |

#### Responses

| Status | Description                                |
|--------|--------------------------------------------|
| 200    | Success. Returns JSON object               |
| 400    | Bad Request. Various error conditions      |

#### Success Response Object

```json
{
  "status": "initialized"
}
```

---

## Token and credit system
### Credit
Credit will be used to monitor the overall usage of processing ressources. The credit value is bound to each token.

### Tokens
- Private Token
This token is bound to an individual and certain details (forename and surname and email address) in order to allow additional features, like email alerts and individual support. At the current stage, the image sets submitted will be used for internal research and testing. No images/3d models will be published.

## Changelog
- 2022-05-11 changed Readme.md, removed beta firmware (as this has been implemented in the main branch See [Github-OpenScan2](https://github.com/OpenScanEu/OpenScan2/) for more details)
- 2021-12-20 added Texture to the 3d model + improved firmware
- 2021-10-11 added Beta Firmware for OpenScanPi 
- 2021-10-08 added a Windows Uploader GUI in /uploader
