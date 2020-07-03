import requests
from tqdm import tqdm
import os

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

download_file("https://ztv-mcloud-bf-s3.zadn.vn/c3B279pqL2o/75a3ae8e1fcff691afde/17cfb1594a1ca342fa0d/720/Ahiru-no-Sora-Ep-06.mp4?authen=exp=1593915609~acl=/c3B279pqL2o/*~hmac=a107256507a845473e9d9cee2a7f9905","test.mp4")
