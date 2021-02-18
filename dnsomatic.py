import json
import requests
import socket
import re
from time import sleep
import os

NOIP_USER = os.getenv('NOIP_USER')
NOIP_PASS = os.getenv('NOIP_PASS')
DNSO_USER = os.getenv('DNSO_USER')
DNSO_PASS = os.getenv('DNSO_PASS')

def get_public_address():
    pub = requests.get('http://myip.dnsomatic.com/')

    if re.match('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', pub.text) is not None:
        return pub.text
    else:
        sleep(5)
        pub = requests.get('http://myip.dnsomatic.com/')
        if re.match('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', pub.text) is not None:
            return pub.text
        else:
            print(f'Failure in getting public IP:\n{pub.text}')
            exit(1)

def get_private_address():
    priv_h = socket.gethostname()
    priv = socket.gethostbyname(priv_h)
    return priv

def update_dnsomatic():
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Cowpi v0.69 Boomala'
        }
def update_noip(myip, myddns):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Cowpi v0.69 Boomala'
        }
    url = f'https://{NOIP_USER}:{NOIP_PASS}@dynupdate.no-ip.com/nic/update?hostname={myddns}&myip={myip}'
    u = requests.get(url, headers=headers)
    print(u.content)

def main():
    pub_ip = get_public_address()
    priv_ip = get_private_address()
    print(f'My Public: {pub_ip} || My Private: {priv_ip}')

