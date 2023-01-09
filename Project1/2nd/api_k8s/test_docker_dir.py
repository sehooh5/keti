import os
import requests
import zipfile

os.system(f"docker build -f select_cam/index -t index:latest .")
