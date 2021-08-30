from json import dump, load
from requests import get
from socket import gethostname, gethostbyname
from re import match
from time import sleep
from os import getenv
# pip install --upgrade git+https://github.com/b-diggity/utilities.git@v0.0.3
from utilities.util import email_outlook as send_mail

NOIP_USER = getenv('NOIP_USER')
NOIP_PASS = getenv('NOIP_PASS')
DNSO_USER = getenv('DNSO_USER')
DNSO_PASS = getenv('DNSO_PASS')
MAIL_USER = getenv('MAIL_USER_OUTLOOK')
MAIL_KEY = getenv('MAIL_PASS_OUTLOOK')
DATA_DIR = getenv('JSON_DIR')


def get_public_address():
    pub = get('http://myip.dnsomatic.com/')

    ip_r = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
    if match(ip_r, pub.text) is not None:
        return pub.text
    else:
        sleep(5)
        pub = get('http://myip.dnsomatic.com/')
        if match(ip_r, pub.text) is not None:
            return pub.text
        else:
            print(f'Failure in getting public IP:\n{pub.text}')
            exit(1)


def get_private_address():
    priv_h = gethostname()
    priv = gethostbyname(priv_h)
    return priv


def update_dnsomatic(myip, site):
    headers = {
        'Content-Type': 'application/json'
        }
    url = f'https://{DNSO_USER}:{DNSO_PASS}@updates.dnsomatic.com/nic/update?hostname={site}&myip={myip}&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG'
    u = get(url, headers=headers)
    print(f'DNSOMATIC: {u.content}')

    return u.content


def update_noip(myip, myddns):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Cowpi v0.69 ANF'
        }
    url = f'https://{NOIP_USER}:{NOIP_PASS}@dynupdate.no-ip.com/nic/update?hostname={myddns}&myip={myip}'
    u = get(url, headers=headers)
    print(f'NOIP: {myddns} returned {u.content}')

    return u.content


if __name__ == "__main__":
    pub_ip = get_public_address()
    priv_ip = get_private_address()
    print(f'My Public: {pub_ip} || My Private: {priv_ip}')

    with open(f'{DATA_DIR}/dns.json') as dj:
        dns_data = load(dj)

    if dns_data['dnsomatic'] == 'true':
        dnsomatic_name = dns_data['dnsomatic_name']
        if pub_ip != dns_data['dnsomatic_ip']:
            m = update_dnsomatic(pub_ip, dnsomatic_name)

            if b'good' in m or b'noch' in m:
                dns_data['dnsomatic_ip'] = pub_ip
            else:
                print('Alert')
                raw_e = m.decode('utf-8').rstrip()
                err_m = f'DNSOMATIC {dnsomatic_name} failed to udpate to IP {pub_ip}.  Error: {raw_e}'
                send_mail(
                    subject='DNSOMATIC Update Failure',
                    message=err_m,
                    username=MAIL_USER,
                    password=MAIL_KEY
                )
        else:
            print('No update needed for DNSOMATIC')
    
    for d in dns_data['noip']:
        if 'private' in d and d['private'] == 'true':
            u_ip=priv_ip
        else:
            u_ip=pub_ip
        
        u_name = d['dns']

        if u_ip != d['ip']:
            m = update_noip(u_ip, u_name)
            if b'good' in m or b'noch' in m:
                d['ip'] = u_ip
            else:
                print('Alert')
                raw_e = m.decode('utf-8').rstrip()
                err_m=f'NOIP {u_name} failed to udpate to IP {u_ip}.  Error: {raw_e}'
                send_mail(
                    subject=f'NOIP Update Failure for {u_name}',
                    message=err_m,
                    username=MAIL_USER,
                    password=MAIL_KEY
                )
        else:
            print(f'No udpate needed for {u_name}')

    with open(f'{DATA_DIR}/dns.json', 'w') as dj:
        dump(dns_data, dj)       
