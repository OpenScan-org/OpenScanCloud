import tkinter
import os
import requests
import time
from zipfile import ZipFile
import sys
from tkinter import filedialog
import webbrowser
import threading
from sys import exit

def browse_button_bg():
    threading.Thread(target=browse_button).start()


def browse_button():
    folder = filedialog.askdirectory()
    if folder == '':
        return
    folderpath.set(folder)
    statustext.set('Selected ' + folder)
    list = []

    for i in os.listdir(folder):
        if os.path.splitext(i)[1] in allowed_extensions:
            list.append(i)
    if len(list) == 0:
        statustext.set('No images found, allowed formats:'+ str(allowed_extensions))
        upload['state'] = 'disabled'
        return

    filesize = 0
    for i in list:
        filesize = filesize + os.path.getsize(folder + '/' + i)

    statustext.set('Selected: ' + folder + '\nFound ' + str(len(list)) + ' photos with total filesize of ' +
                   str(int(filesize/1000000)) + 'MB')
    upload['state']='active'
    msg['filesize'] = filesize
    msg['folder'] = folder + '/'
    msg['filelist'] = list
    msg['photos'] = len(list)
    msg['token'] = token.get()


def page1():
    naviUpload.grid_forget()
    enterToken.grid_forget()
    verifyToken.grid_forget()
    browse.grid(row=2, column=0, sticky='e')
    upload.grid(row=2, column=1, sticky='w')

    naviSettings.grid(row=4, columnspan=2)
    statustext.set('Select the folder containing your photos:')


def page2():
    browse.grid_forget()
    upload.grid_forget()
    naviSettings.grid_forget()
    enterToken.grid(row=2, columnspan=2)
    naviUpload.grid(row=4, columnspan=2)
    verifyToken.grid(row=3, columnspan=2)
    if token.get() == '':
        statustext.set('Please enter a valid OpenScanCloud token')
        naviUpload['state'] = 'disabled'
    else:
        statustext.set('Your OpenScanCloud token:')
        naviUpload['state'] = 'active'


def OpenScanCloud(cmd, msg):
    r = requests.get(server + cmd, auth=(user, pw), params=msg)
    return r

def verify_bg():
    threading.Thread(target=verify).start()

def verify():
    verifyToken['state'] = 'disabled'
    statustext.set('Verifying Token ...')
    msg['token'] = token.get()
    if len(token.get()) < 15:
        statustext.set('Invalid Token')
        verifyToken['state'] = 'active'
        return
    r = OpenScanCloud('getTokenInfo', msg)
    if r.status_code != 200:
        statustext.set('Could not verify token, please try again:')
        naviUpload['state'] = 'disabled'
        verifyToken['state'] = 'active'
        return
    try:
        with open(active_directory + '/token.txt', 'w') as file:
            file.write(msg['token'])
        credit = round(int(r.json()['credit']) / 1000000000, 2)
        filesize = round(int(r.json()['limit_filesize']) / 1000000, 2)
        statustext.set('Token verified and saved.\nYou can upload a total of ' + str(credit) + 'GB\nWith a maximum size of '+str(filesize)+'MB per set')
        naviUpload['state'] = 'active'
    except:
        statustext.set('ERROR: Could not save token.')
    verifyToken['state'] = 'active'


def uploader_bg():
    threading.Thread(target=uploader).start()

def uploader():
    upload['state'] = 'disabled'
    browse['state'] = 'disabled'

    statustext.set('Preparing upload ...')
    r = OpenScanCloud('getTokenInfo', msg)
    if r.status_code != 200:
        statustext.set('Connection failed')
        upload['state'] = 'active'
        browse['state'] = 'active'

        return

    msg2 = r.json()

    if msg['filesize'] > msg2['credit']:
        statustext.set('Not enough credit, please contact cloud@openscan.eu')
        upload['state'] = 'active'
        browse['state'] = 'active'
        return

    if msg['filesize'] > msg2['limit_filesize']:
        statustext.set('Filesize limit exceeded')
        upload['state'] = 'active'
        browse['state'] = 'active'
        return

    zipAndSplit()
    uploadAndStart()
    browse['state'] = 'active'

def zipAndSplit():
    statustext.set('Creating zip ...')

    dir_tmp = active_directory + '/tmp/'

    if not os.path.isdir(dir_tmp):
        os.mkdir(dir_tmp)


    for i in os.listdir(dir_tmp):
        if os.path.isfile(dir_tmp + i):
            os.remove(dir_tmp + i)

    projectname = str(int(time.time()*100))+ '-OSC.zip'
    file = dir_tmp + projectname

    msg['project'] = projectname
    with ZipFile(file, 'w') as zip:
        for i in msg['filelist']:
            statustext.set('Adding to zip: ' + i)
            zip.write(msg['folder'] + i, i)

    msg['filesize'] = os.path.getsize(file)

    msg['partslist'] = [file]

    if os.path.getsize(file) > size_to_split:
        msg['partslist'] = []
        number = 1
        with open(file, 'rb') as f:
            chunk = f.read(size_to_split)
            while chunk:
                statustext.set('Splitting archive into chunks: ' + str(number))
                with open(file + '_' + str(number), 'wb+') as chunk_file:
                    chunk_file.write(chunk)
                msg['partslist'].append(file + '_' + str(number))
                number += 1
                chunk = f.read(size_to_split)
        os.remove(file)
    msg['parts'] = len(msg['partslist'])
    statustext.set('preparing project on the OpenScanCloud server')
    r = OpenScanCloud('createProject', msg)
    if r.status_code != 200:
        statustext.set('ERROR: Could not create project')
        return
    msg['ulink'] = ''
    msg['ulink'] = r.json()['ulink']

def uploadAndStart():
    if msg['ulink'] == '':
        statustext.set('ERROR: Upload not started')
        return
    i = 0

    filelist = msg['partslist']
    ulinks = msg['ulink']

    for file in filelist:
        statustext.set('uploading part ' + str(i+1) + ' of ' + str(len(filelist)))
        link = ulinks[i]
        i = i+1

        data = open(file, 'rb').read()
        r = requests.post(url=link, data=data, headers={'Content-type': 'application/octet-stream'})
        if r.status_code != 200:
            statustext.set('ERROR: could not upload file' + str(i))
            return
        os.remove(file)

    statustext.set('starting project')
    r = OpenScanCloud('startProject', msg)
    if r.status_code != 200:
        statustext.set('ERROR: could not start processing')
    statustext.set('processing started ... you will get an email soon')
    try:
        os.rmdir(active_directory + '/tmp/')
    except:
        pass

## OSC Settings
size_to_split = 200000000 #200MB is the maximum part size (total zip file can be up to 2GB)
limit_filesize = 0
limit_photos = 0
credit = 0
allowed_extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG']
user = 'openscan'
pw = 'free'
server = 'http://openscanfeedback.dnsuser.de:1334/'
msg = {}

active_directory = os.path.dirname(os.path.realpath(sys.argv[0]))

# TKinter Setup

window = tkinter.Tk()
window.title('OpenScan Desktop Uploader')
window.geometry('500x220')
window.resizable(0,0)
window.grid_columnconfigure((0, 1), weight=1)
window.grid_rowconfigure((0, 1, 2, 4, 5), weight=1,minsize=30)

statustext = tkinter.StringVar()
folderpath = tkinter.StringVar()
token = tkinter.StringVar()


title = tkinter.Label(window, text="--OpenScan Uploader --", font='Helvetica 18 bold')
status = tkinter.Label(window, textvariable=statustext)
naviUpload = tkinter.Button(text="UPLOAD", command=page1, cursor="hand2")
naviSettings = tkinter.Button(text="SETTINGS", command=page2, cursor="hand2")

link = tkinter.Button(text="GITHUB", cursor="hand2")
link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/OpenScanEu/OpenScanCloud"
                                                      "#current-functionality--desktop-uploader-for-windows--download"))
donate = tkinter.Button(text="DONATE", cursor="hand2")
donate.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.patreon.com/bePatron?u=51974655"))

browse = tkinter.Button(text="Select folder", command=browse_button_bg)
upload = tkinter.Button(text = 'Upload Photos', command=uploader_bg)

enterToken = tkinter.Entry(textvariable=token, justify='center')
verifyToken = tkinter.Button(text="Verify and Save Token", cursor="hand2", command=verify_bg)

title.grid(row=0, columnspan=2)
status.grid(row=1, columnspan=2, sticky="ew")
donate.grid(row=5, column=1, sticky='ew')
link.grid(row=5, column=0, sticky='ew')
upload['state']='disabled'


if os.path.isfile(active_directory + '/token.txt'):
    with open(active_directory + '/token.txt', 'r') as file:
        token.set(file.read())
    page1()
else:
    token.set('')
    statustext.set('Please go to SETTINGS and enter a valid token')
    page2()

window.mainloop()

exit()
