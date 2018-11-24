import ipfsapi
import psutil
import time
import subprocess
from urllib.request import urlopen
import os

def ipfs_check():
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
    except:
        for proc in psutil.process_iter():
            if proc.name() == "ipfs":
                proc.kill()

    subprocess.Popen(["ipfs","daemon"])

def python_check():
    try:
        urlopen('http://127.0.0.1:8000', timeout=1)
    except:
        subprocess.Popen(["python3","/home/warproxxx/IPFS/manage.py", "runserver"])
        
while True:
    ipfs_check()
    python_check()
    
    time.sleep(60)