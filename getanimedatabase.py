import requests
import re
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool

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
    a = geteps(i)
    a = list(dict.fromkeys(a))
    for p in a:
        print(i.replace("https://tv.zing.vn/",""))
        getmp4(p,i.replace("https://tv.zing.vn/",""))

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
    open(post_title,"wb").write(response.content) #cache
    list = []
    file = open(post_title,"r")
    file2 = open("links/"+title.replace(" ","").replace("/","")+".txt","w") #cache links
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
                        file2.write(filtered(newlist[0])+"\n")

    file2 = open("links/"+title.replace(" ","").replace("/","")+".txt","r") #read from cache
    file3 = open("links/"+post_title.replace("https://tv.zing.vn/","").replace("/","")+".txt","a")  #create new text file with links in the correct format
    read = file2.readline()
    print(read)
    file3.write(read)
    os.remove("links/"+title.replace(" ","").replace("/","")+".txt") #remove cache file
    os.remove(post_title)

def geteps(link):
    response = requests.get(link) #get original movie post
    soup = BeautifulSoup(response.content,"html.parser")
    eps = soup.find_all("a",href=True) #get eps pages
    ep_list=[]
    for i in eps: #filter out /video/id links only
        if filter.search(i["href"]):
            ep_list.append("https://tv.zing.vn"+i["href"])
    return(ep_list)

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
if __name__ == '__main__':
    if not os.path.isfile("out.txt"):

        a = getallmovie(link)

        file = open("difference.txt","r").readlines()
        file = [x.replace('\n', '') for x in file]

        final = set(a).difference(file)
        out = open("out.txt","w")
        for i in final:
            out.write(i+"\n")
    final = [x.replace('\n', '') for x in open("out.txt","r").readlines()]
    p = Pool(processes=10)
    p.map(get,final)
    p.close()
    p.join()
