import subprocess
import os
from dotenv import load_dotenv
import pyudev
import time

load_dotenv()
FNULL = open(os.devnull, 'w') #prevent output
available=[]

def get_active_devices():
    for ping in range(int(os.getenv("IP_RANGE_LO")),int(os.getenv("IP_RANGE_HI"))):
        address='.'.join(os.getenv("STATIC_IP").split(".")[:3])+'.'+str(ping)
        if address != os.getenv("STATIC_IP"):
            res = subprocess.call(['ping', '-w', '1', address],stdout=FNULL, stderr=subprocess.STDOUT)
            if res == 0:
                available.append(address)
    return available
