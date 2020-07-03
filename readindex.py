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

file = open("index.txt","r")
cache = open("printout.txt","w")

s = file.readlines()
for p in range(10000000):
    a = filtered(s)
    if (len(filtered(s)[1])) == 0:
        for o in a[0]:
            if not "https://drive.google.com/" in o:
                print("https://tv.zing.vn/"+o)
                cache.write("https://tv.zing.vn/"+o)
            else:
                cache.write(o)
                print(o)
    for i in a[2]:
        s.remove(i)
