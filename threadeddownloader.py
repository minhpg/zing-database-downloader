import os
import threading
import requests
from tqdm import tqdm
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from os import path


processes=[]
threads=[]

def download_file(url,local_filename):
    if not os.path.isdir(local_filename):
        r = requests.get(url, stream=True)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(local_filename, 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        return local_filename
        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")
    else:
        return local_filename

def wget(line):
    a = line.find("|")
    name = line[0:a-1]
    url = line[a+1:len(line)]
    if "https" not in url:
        url = url.replace("//","https://")
    print(name)
    print(url)
    download_file(url,"./downloaded/"+name+".mp4")
    uploadDrive("./downloaded/"+name+".mp4")

def download(src):
    source = open(src,"r")
    while True:
        line = source.readline()
        if not line:
            break
        else:
            print(line)
            processes.append(line)
    for i in processes:
        t = threading.Thread(target=wget,args=[i])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

def create_credential():
    auth_and_save_credential()


# Authentication + token creation
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
# Create GoogleDrive instance with authenticated GoogleAuth instance.


def uploadDrive(file_path):
    file1 = drive.CreateFile({'title': file_path.replace("./downloaded/","")})
    file1.SetContentFile(file_path)
    file1.Upload()
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    os.remove(file_path)
    file1 = None


drive = create_drive_manager()
links = os.listdir("links")
print(links)
for i in links:
    download("links/"+i)
