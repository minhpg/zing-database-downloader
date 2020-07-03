import os
import threading
import requests
from tqdm import tqdm
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from os import path
from multiprocessing import Pool


processes=[]
threads=[]

def download_file(url,local_filename):
    os.system("wget -O '"+local_filename+"' "+url)
    return local_filename

def wget(i):
    drive = create_drive_manager()
    line = i[0]
    folder_id = i[1]
    a = line.find("|")
    print(a)
    name = line[0:a-1]
    url = line[a+1:len(line)]
    if "https://" not in url:
        url = url.replace("//","https://")
        if "|" in url:
            url = url.replace(url[0:url.find("|")+1],"")
    print(name)
    print(url)
    a = download_file(url,"./downloaded/"+name+".mp4")
    if not a:
        return None
    else:
        uploadDrive("./downloaded/"+name+".mp4",folder_id,drive)

def download(src,name):
    source = open(src,"r")
    folder_id = createfolder(name)
    processes=[]
    while True:
        line = source.readline()
        if not line:
            break
        else:
            print(line)
            processes.append([line,folder_id])
    threads=[]
    p = Pool(20)
    p.map(wget,processes)
    p.close()
    p.join()

def uploadDrive(file_path,folder_id):
    file1 = drive.CreateFile({'title': file_path.replace("./downloaded/",""),'parents': [{'id': folder_id}]})
    file1.SetContentFile(file_path)
    file1.Upload()
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    os.remove(file_path)
    file1 = None

def createfolder(name):
    folder = drive.CreateFile({'title' : name.replace(".txt",""), 'mimeType' : 'application/vnd.google-apps.folder','parents': [{'id': "1vhhreNp0ORUHo-dOUM3ybm50iAwLtGCB"}]})
    folder.Upload()
    folder_id = folder['id']
    return folder_id

def create_credential():
    auth_and_save_credential()
def create_drive_manager():
    gAuth = GoogleAuth()
    typeOfAuth = None
    if not path.exists("credentials.txt"):
        typeOfAuth = input("Nhập 'Y' để lưu file credentials mới: ")
    bool = True if typeOfAuth == "Y" or path.exists("credentials.txt") else False
    authorize_from_credential(gAuth, bool)
    drive: GoogleDrive = GoogleDrive(gAuth)
    return drive
def authorize_from_credential(gAuth, isSaved):
    if not isSaved: #no credential.txt wanted
        auth_no_save(gAuth)
    if isSaved and not path.exists("credentials.txt"):
        create_credential()
        gAuth.LoadCredentialsFile("credentials.txt")
    if isSaved and gAuth.access_token_expired:
        gAuth.LoadCredentialsFile("credentials.txt")
        gAuth.Refresh()
        print("Token đã được làm mới!")
        gAuth.SaveCredentialsFile("credentials.txt")
    gAuth.Authorize()
    print("Đã được cấp quyền GoogleAPI!")
def auth_and_save_credential():
    gAuth = GoogleAuth()
    gAuth.LocalWebserverAuth()
    gAuth.SaveCredentialsFile("credentials.txt")
def auth_no_save(gAuth):
    gAuth.LocalWebserverAuth()

if __name__ == '__main__':
    drive = create_drive_manager()
    links = os.listdir("links")
    print(links)
    for i in links:
        download("links/"+i,i)
        processes=[]
        threads=[]
        folder_id = None
        links.remove(i)
        os.remove("links/"+i)
