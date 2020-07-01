line = "Z/X: Code Reunion - Tổ Đội Xóa Điểm Đen Tập 12 END Vietsub_1080p|https://ztv-mcloud-bf-s3.zadn.vn/0YADaMhB1RQ/4b98479567d58e8bd7c4/ffbbc2c92d8dc4d39d9c/720/Z-X-Code-Reunion-Ep-12_END.mp4?authen=exp=1593666525~acl=/0YADaMhB1RQ/*~hmac=b165a26bb0af85062d43b23c04718725#mp4"
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
