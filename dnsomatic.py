from json import dump, load, loads
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
DNS_UPDATES = getenv('DNS_UPDATES')


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
    noip_list = []
    dnsomatic_list = []

    noip_public = loads(DNS_UPDATES).get('noip').get('public')
    noip_private = loads(DNS_UPDATES).get('noip').get('private')
    dnsomatic = loads(DNS_UPDATES).get('dnsomatic')
    pub_ip = get_public_address()
    priv_ip = get_private_address()
    
    print(f'My Public: {pub_ip} || My Private: {priv_ip}')

    try:
        with open(f'{DATA_DIR}/dns.json') as dj:
            dns_data = load(dj)
    except:
        dns_data = loads('{}')

    if dnsomatic:
        print(f'DNSOMATIC Updates for {dnsomatic}')
        for dns_site in dnsomatic:
            dnsomatic_ip = ''

            if dns_data.get('dnsomatic') is not None:
                for item in dns_data.get('dnsomatic'):
                    for k in item:
                        if k == dns_site:
                            dnsomatic_ip = item[k]

            if pub_ip != dnsomatic_ip:
                m = update_dnsomatic(pub_ip, dns_site)

                if b'good' in m or b'noch' in m:
                    dnsomatic_list.append({dns_site: pub_ip})
                else:
                    print('Alert')
                    raw_e = m.decode('utf-8').rstrip()
                    err_m = f'DNSOMATIC {dns_site} failed to udpate to IP {pub_ip}.  Error: {raw_e}'
                    print(err_m)
                    send_mail(
                        subject='DNSOMATIC Update Failure',
                        message=err_m,
                        username=MAIL_USER,
                        password=MAIL_KEY
                    )
            else:
                print('No update needed for DNSOMATIC')
                dnsomatic_list.append({dns_site: pub_ip})
    
    if noip_public:
        print(f'NOIP Public Updates for {noip_public}')
        for dns_public in noip_public:
            print(dns_public)
            noip_ip = ''

            if dns_data.get('noip') is not None:
                for item in dns_data.get('noip'):
                    for k in item:
                        if k == dns_public:
                            noip_ip = item[k]

            if noip_ip != pub_ip:
                m = update_noip(pub_ip, dns_public)
                if b'good' in m or b'noch' in m:
                    noip_list.append({dns_public: pub_ip})
                else:
                    print('Alert')
                    raw_e = m.decode('utf-8').rstrip()
                    err_m=f'NOIP {dns_public} failed to udpate to IP {pub_ip}.  Error: {raw_e}'
                    send_mail(
                        subject=f'NOIP Update Failure for {dns_public}',
                        message=err_m,
                        username=MAIL_USER,
                        password=MAIL_KEY
                    )
            else:
                print(f'No udpate needed for {dns_public}')
                noip_list.append({dns_public: pub_ip})

    if noip_private:
        print(f'NOIP Private Updates for {noip_private}')
        for dns_private in noip_private:
            print(dns_private)
            noip_ip = ''

            if dns_data.get('noip') is not None:
                for item in dns_data.get('noip'):
                    for k in item:
                        if k == dns_private:
                            noip_ip = item[k]

            if noip_ip != priv_ip:
                m = update_noip(priv_ip, dns_private)
                if b'good' in m or b'noch' in m:
                    noip_list.append({dns_private: priv_ip})
                else:
                    print('Alert')
                    raw_e = m.decode('utf-8').rstrip()
                    err_m=f'NOIP {dns_private} failed to udpate to IP {priv_ip}.  Error: {raw_e}'
                    send_mail(
                        subject=f'NOIP Update Failure for {dns_private}',
                        message=err_m,
                        username=MAIL_USER,
                        password=MAIL_KEY
                    )
            else:
                print(f'No udpate needed for {dns_private}')
                noip_list.append({dns_private: priv_ip})

    dns_json = {
        'noip': noip_list,
        'dnsomatic': dnsomatic_list
    }

    print(dns_json)
    
    with open(f'{DATA_DIR}/dns.json', 'w') as dj:
        dump(dns_json, dj)       
