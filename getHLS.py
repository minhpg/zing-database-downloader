from lxml import html, etree
import re
import requests
from selenium import webdriver
from seleniumwire import webdriver
import time
from bs4 import BeautifulSoup
import os

fireFoxOptions = webdriver.FirefoxOptions()
os.environ['MOZ_HEADLESS'] = '1'

def fetch_m3u8(link):
    url = link
    driver = webdriver.Firefox()
    m3u8 = []
    a = 0
    while True:
        if len(m3u8)<1:
            a+=1
            driver.get(url)
            for request in driver.requests:
                try:
                    if ".m3u8" in request.path:
                        line = str(request.path)
                        m3u8.append(line)
                        print(line)
                except:
                    pass
        if a<5:
            break
        else:
            break
    soup = BeautifulSoup(driver.page_source,"html.parser")
    homepage = soup.find("title")
    post_title = homepage.text.replace(" ","")
    post_title = post_title.replace("(","")
    post_title = post_title.replace(")","")
    file = open("/Users/minhpg/Desktop/anivsub.org/moekawaiistream/"+post_title,"w")
    for i in m3u8:
        file.write(i+"\n")
    driver.quit()

links = "https://tv.zing.vn/video/id/IWZEAUO9.html"
fetch_m3u8(links)
