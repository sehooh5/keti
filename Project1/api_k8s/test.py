import os
import requests
import zipfile

API_URL = "http://123.214.186.231:4882"
fname = "select_cam"
filename = "select_cam.zip"

if filename.find("zip") != -1:
    print("here")
    with open(filename, 'wb') as select_cam:
        data = requests.get(f"{API_URL}/download?filename={filename}")
        select_cam.write(data.content)

    zip_ref = zipfile.ZipFile(f'./{filename}', 'r')
    zip_ref.extractall(f'./{fname}')
    zip_ref.close()
    os.system(f"docker build -f {fname}/{fname} -t {fname}:latest .")
else:
    with open(filename, 'wb') as fname:
        data = requests.get(f"{API_URL}/download?filename={filename}")
        fname.write(data.content)
