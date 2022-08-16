# How to run script.py

### DOM XSS in jQuery anchor href attribute sink using location.search source

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "javascript:alert(document.cookie)"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "javascript:alert(document.cookie)" -p 127.0.0.1:8080`
