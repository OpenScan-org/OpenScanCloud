import os
import requests
import time
from zipfile import ZipFile

################ That's all you need to change : ###################

dir_images = '/images/' # enter the directory of your images
dir_temp = '/temp/' # enter your temporary directory
token = ''# enter your token (send me a mail to cloud@openscan.eu with your forename and surname to get a free token)

################ No need to change anything below ##################

size_to_split = 200000000
limit_filesize = 0
limit_photos = 0
credit = 0
allowed_extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG']
user = 'openscan'
pw = 'free'
server = 'http://openscanfeedback.dnsuser.de:1334/'
msg= {}
msg['token'] = token

def OpenScanCloud(cmd, msg):
    r = requests.get(server + cmd, auth=(user, pw), params=msg)
    if r.status_code == 200:
        return r
    else:
        return r

def uploadAndStart(filelist, ulinks):
    i = 0
    for file in filelist:
        print('uploading part ' + str(i+1) + ' of ' + str(len(filelist)))
        link = ulinks[i]
        cmd = 'curl -# -X POST ' + link + ' --header Content-Type:application/octet-stream --data-binary @"' + file
        i = i+1
        os.system(cmd)
        os.remove(file)
    print('starting project')
    r = OpenScanCloud('startProject', msg)
    if r.status_code != 200:
        print('ERROR: could not start processing')
    print('processing started ... you will get an email soon')
    print('thank you for testing OpenScanCloud')

def getAndVerifyToken():
    print('verifying token')
    global limit_filesize
    global limit_photos
    global credit

    tokenInfo = OpenScanCloud('getTokenInfo', msg)
    if tokenInfo.status_code != 200:
        print('ERROR: invalid token')
        exit()

    limit_filesize = tokenInfo.json()['limit_filesize']
    limit_photos = tokenInfo.json()['limit_photos']
    credit = tokenInfo.json()['credit']

def prepareSet():
    print('preparing imageset')
    # load images:
    list = os.listdir(dir_images)

    for i in list:
        if os.path.splitext(i)[1] not in allowed_extensions:
            list.remove(i)
    if len(list) == 0:
        print('ERROR: no images found in ' + dir_images)
        exit()

    filesize = 0
    for i in list:
        filesize = filesize + os.path.getsize(dir_images + i)

    msg['photos'] = len(list)

    if filesize > limit_filesize or len(list) > limit_photos:
        print('ERROR: Limits exceeded')
        exit()
    return list

def zipAndSplit(imagelist):
    print('zipping images')
    for i in os.listdir(dir_temp):
        os.remove(dir_temp + i)

    projectname = str(int(time.time()*100))+ '-OSC.zip'
    file = dir_temp + projectname

    print('projectname: ' + projectname)
    msg['project'] = projectname
    with ZipFile(file, 'w') as zip:
        for i in imagelist:
            zip.write(dir_images + i, i)

    msg['filesize'] = os.path.getsize(file)

    msg['partslist'] = [file]

    if os.path.getsize(file) > size_to_split:
        msg['partslist'] = []
        number = 1
        with open (file, 'rb') as f:
            chunk = f.read(size_to_split)
            while chunk:
                with open(file + '_' + str(number), 'wb+') as chunk_file:
                    chunk_file.write(chunk)
                msg['partslist'].append(file + '_' + str(number))
                number += 1
                chunk = f.read(size_to_split)
        os.remove(file)
    msg['parts'] = len(msg['partslist'])
    print('preparing project on the OpenScanCloud server')
    r = OpenScanCloud('createProject', msg)
    if r.status_code != 200:
        print('ERROR: Could not create project')
        exit()
    msg['ulink'] = r.json()['ulink']

getAndVerifyToken()
imagelist = prepareSet()
zipAndSplit(imagelist)
uploadAndStart(msg['partslist'], msg['ulink'])
