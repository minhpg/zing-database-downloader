import os
import threading
import requests
from tqdm import tqdm
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from os import path
import re
from bs4 import BeautifulSoup

processes=[]
threads=[]
def getallmovie(link):
    pages = []
    movie_list=[]
    for i in range(50):
        pages.append(link+"?page="+str(i))
    for link in pages:
        response = requests.get(link) #get original movie post
        soup = BeautifulSoup(response.content,"html.parser")
        movie = soup.find_all("a",href=True) #get eps pages
        for b in movie:
            a = (b["href"])
            if not filter2.search(a) and not filter3.search(a) and not filter4.search(a) and not filter5.search(a) and not filter6.search(a) and not filter7.search(a) and not filter8.search(a):
                if not filter9.search(a) and not filter10.search(a) and not filter11.search(a) and not filter12.search(a) and not filter13.search(a):
                    movie_list.append("https://tv.zing.vn"+a)
    movie_list = list(dict.fromkeys(movie_list))
    if "https://tv.zing.vn/" in movie_list:
        movie_list.remove("https://tv.zing.vn/")
        return movie_list
    else:
        return movie_list
def get(i):
    print(i)
    a = geteps(i)
    a = list(dict.fromkeys(a))
    for s in a:
        getmp4(s,i)
def filtered(s):
    l = 0
    r = 0
    for i in range(0,len(s)):
        if(s[i] == '"'):
            l = i
            break
    for i in range(l+1,len(s)):
        if(s[i] == '"'):
            r = i
            break
    return s[l+1:r]
def getmp4(link,post_title):
    response = requests.get(link) #request ep page
    soup = BeautifulSoup(response.content,"html.parser")
    homepage = soup.find("title")
    title = homepage.text.strip()
    open("cache","wb").write(response.content) #cache
    list = []
    file = open("cache","r")
    file2 = open("links/"+title.replace(" ","").replace("/",""),"w") #cache links
    for line in file:
        a = file.readline()
        if filter1.search(a):
            for i in range(5):
                a = file.readline()
                newlist=[]
                newlist.append(a)
                s = filtered(newlist[0])
                if not s == "" and not filtervip.search(s):
                    if filter240.search(s) or filter360.search(s) or filter480.search(s) or filter720.search(s) or filter1080.search(s): #filter qualities
                        file2.write(title+"_"+filtered(newlist[0])+"|")
                    else:
                        file2.write(filtered(newlist[0])+"#mp4"+"\n")

    file2 = open("links/"+title.replace(" ","").replace("/",""),"r") #read from cache
    file3 = open("links/"+post_title.replace("https://tv.zing.vn/","").replace("/",""),"a")  #create new text file with links in the correct format
    read = file2.readline()
    print(read)
    file3.write(read)
    os.remove("links/"+title.replace(" ","").replace("/","")) #remove cache file
    os.remove("cache")
def geteps(link):
    response = requests.get(link) #get original movie post
    soup = BeautifulSoup(response.content,"html.parser")
    eps = soup.find_all("a",href=True) #get eps pages
    ep_list=[]
    for i in eps: #filter out /video/id links only
        if filter.search(i["href"]):
            ep_list.append("https://tv.zing.vn"+i["href"])
    return(ep_list)
def download_file(url,local_filename):
    if not os.path.isdir(local_filename):
        try:
            r = requests.get(url, stream=True)
        except:
            return None
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
def wget(line,folder_id):
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
        uploadDrive("./downloaded/"+name+".mp4",folder_id)
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
            processes.append(line)
    threads=[]
    for i in processes:
        t = threading.Thread(target=wget,args=[i,folder_id])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
def uploadDrive(file_path,folder_id):
    file1 = drive.CreateFile({'title': file_path.replace("./downloaded/",""),'parents': [{'id': folder_id}]})
    file1.SetContentFile(file_path)
    file1.Upload()
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    os.remove(file_path)
    file1 = None
def createfolder(name):
    folder = drive.CreateFile({'title' : name.replace(".txt",""), 'mimeType' : 'application/vnd.google-apps.folder','parents': [{'id': "1UfkjCuMxzVarx5S4E06ar3oxf5ftEqD7"}]})
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

link = "https://tv.zing.vn/the-loai/Anime/IWZ9ZII0.html"

filter1 = re.compile('playlist.sources.push') #regex filters
filter240 = re.compile('240p')
filter360 = re.compile('360p')
filter480 = re.compile('480p')
filter720 = re.compile('720p')
filter1080 = re.compile('1080p')
filtervip = re.compile('VIP')
filter = re.compile("/video/id")
filter2 = re.compile("//zingtv.vn")
filter3 = re.compile("//zingmp3.vn/")
filter4 = re.compile("//zingnews.vn")
filter5 = re.compile("//zingnews.vn")
filter6 = re.compile("javascript")
filter7 = re.compile("#")
filter8 = re.compile("/the-loai/")
filter9 = re.compile("/video")
filter10 = re.compile("/id-invaded")
filter11 = re.compile("adtima")
filter12 = re.compile("//zingtv.vn/huong-dan/Lien-He")
filter13 = re.compile("//zingtv.vn/tnc")

drive = create_drive_manager()

links = getallmovie(link)
for i in links:
    print(i)
    ep_list = geteps(i)
    for p in ep_list:
        getmp4(p,i.replace("https://tv.zing.vn/","").replace("/",""))
    i = i.replace("https://tv.zing.vn/","").replace("/","")
    download("links/"+i,i)
    processes=[]
    threads=[]
    folder_id = None
    os.remove("links/"+i)
    print(i)
