import pydrive
import os
import threading
import requests
from tqdm import tqdm
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from os import path
from multiprocessing.dummy import Pool as ThreadPool

threads = []
processes = []

def check_empty(i):
    listfile=[]
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(i["id"])}).GetList()
    #listfile.append("https://drive.google.com/folders/"+i["id"])
    listfile.append(i["title"])
    #listfile.append("%")
    #for p in file_list:
    #    listfile.append(p["title"])
    #listfile.append("%")
    return listfile

def get_empty_folder(id):
    folder_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(id)}).GetList()
    pool = ThreadPool(2)
    results = pool.map(check_empty,folder_list)
    pool.close()
    pool.join()
    return results
def delete_file(drive, id):
    drive.auth.service.files().delete(fileId=id).execute()
def filtered(s):
    list = 0
    l = 0
    r = 0
    for i in range(0,len(s)):
        if "%" in s[i]:
            l = i
            break
    for i in range(l+1,len(s)):
        if "%" in s[i]:
            r = i
            break
    return [s[l-2:l],s[l+1:r],s[l-2:r+1]]

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



list = []
id = "1vhhreNp0ORUHo-dOUM3ybm50iAwLtGCB"
drive = create_drive_manager()
if not os.path.isfile("index.txt"):
    results = get_empty_folder(id)
    file = open("index.txt","w")
    for i in results:
        for p in i:
            file.write(p+"\n")





if not os.path.isfile("printout.txt"):
    s = open("1.txt","r").readlines()
    cache = open("printout.txt","w")
    for p in range(10000000):
        a = filtered(s)
        if (len(filtered(s)[1])) == 0:
            for o in a[0]:
                if not "https://drive.google.com/" in o:
                    print(o)
                    cache.write(o)
        for i in a[2]:
            s.remove(i)
index = open("index.txt","r").readlines()
print(index)
printout = open("printout.txt","r").readlines()
print(printout)
difference = set(index).difference(printout)
file = open("difference.txt","w")
for i in difference:
    file.write("https://tv.zing.vn/"+i)
