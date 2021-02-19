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

    ip_r = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'  # pylint: disable=anomalous-backslash-in-string
    if re.match(ip_r, pub.text) is not None:
        return pub.text
    else:
        sleep(5)
        pub = requests.get('http://myip.dnsomatic.com/')
        if re.match(ip_r, pub.text) is not None:
            return pub.text
        else:
            print(f'Failure in getting public IP:\n{pub.text}')
            exit(1)

def get_private_address():
    priv_h = socket.gethostname()
    priv = socket.gethostbyname(priv_h)
    return priv

def update_dnsomatic(myip, site):
    headers = {
        'Content-Type': 'application/json'
        }
    url = f'https://{DNSO_USER}:{DNSO_PASS}@updates.dnsomatic.com/nic/update?hostname={site}&myip={myip}&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG'
    u = requests.get(url, headers=headers)
    print(f'DNSOMATIC: {u.content}')

    return u.content

def update_noip(myip, myddns):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Cowpi v0.69 Boomala'
        }
    url = f'https://{NOIP_USER}:{NOIP_PASS}@dynupdate.no-ip.com/nic/update?hostname={myddns}&myip={myip}'
    u = requests.get(url, headers=headers)
    print(f'NOIP: {myddns} returned {u.content}')

    return u.content

def main():
    pub_ip = get_public_address()
    priv_ip = get_private_address()
    print(f'My Public: {pub_ip} || My Private: {priv_ip}')

    data_dir = '/opt/scripts/data'
    with open(f'{data_dir}/dns.json') as dj:
        dns_data = json.load(dj)

    if dns_data['dnsomatic'] == 'true':
        if pub_ip != dns_data['dnsomatic_ip']:
            m = update_dnsomatic(pub_ip, dns_data['dnsomatic_name'])

            if b'good' in m or b'noch' in m:
                dns_data['dnsomatic_ip'] = pub_ip
        else:
            print('No updated needed for DNSOMATIC')
    
    for d in dns_data['noip']:
        if 'private' in d and d['private'] == 'true':
            u_ip=priv_ip
        else:
            u_ip=pub_ip
        
        if u_ip != d['ip']:
            m = update_noip(u_ip, d['dns'])
            if b'good' in m or b'noch' in m:
                d['ip'] = u_ip
        else:
            print(f'No udpate needed for {d["dns"]}')

    with open(f'{data_dir}/dns.json', 'w') as dj:
        json.dump(dns_data, dj)       

main()
