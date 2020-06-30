import requests
import re
from bs4 import BeautifulSoup
import os


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

def getmp4(ep_list):
    for i in ep_list:
            response = requests.get(i) #request ep page
            soup = BeautifulSoup(response.content,"html.parser")
            homepage = soup.find("title")
            title = homepage.text.strip()
            open("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/cache","wb").write(response.content) #cache
            list = []
            file = open("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/cache","r")
            file2 = open("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/links/"+title.replace(" ","")+".txt","w") #cache links
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

            file2 = open("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/links/"+title.replace(" ","")+".txt","r") #read from cache
            file3 = open("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/links/"+link.replace("https://tv.zing.vn/","")+".txt","a")  #create new text file with links in the correct format
            read = file2.readline()
            print(read)
            file3.write(read)
            os.remove("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/links/"+title.replace(" ","")+".txt") #remove cache file

    os.remove("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/cache")

def geteps(link):
    response = requests.get(link) #get original movie post
    soup = BeautifulSoup(response.content,"html.parser")
    eps = soup.find_all("a",href=True) #get eps pages
    ep_list=[]
    for i in eps: #filter out /video/id links only
        if filter.search(i["href"]):
            ep_list.append("https://tv.zing.vn"+i["href"])
    return(ep_list)

link = "https://tv.zing.vn/number24"

filter1 = re.compile('playlist.sources.push') #regex filters
filter240 = re.compile('240p')
filter360 = re.compile('360p')
filter480 = re.compile('480p')
filter720 = re.compile('720p')
filter1080 = re.compile('1080p')
filtervip = re.compile('VIP')
filter = re.compile("/video/id")



ep_list = geteps(link)
getmp4(list(dict.fromkeys(ep_list)))
