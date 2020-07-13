When user has autorized or registered he gets a token that he must provides in each request to server.
## REGISTRATION 
#### REQUEST
```
POST /registration

Content-type: application/x-www-form-urlencoded

Body:
name: {name}
password: {password}
email: {email}
```
#### RESPONSE
* valid request

```
Status: 201

Content-type: application/json

Body: {"status": "ok"}

Location: /chats

Cookies:
user_id={id}
token={...}
```
* invalid request

```
Status: 400

Content-type: application/json

Body:
{"error": "{description of error}"}

```
## Authorization 
#### REQUEST
```
POST /login

Content-type: application/x-www-form-urlencoded

Body:
name: {name}
password: {password}
```
#### RESPONSE
* valid request

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

Location: /chats

Cookies:
user_id={id}
token={...}
```
* invalid request

```
Status: 400

Content-type: application/json

Body:
{"error": "{description of error}"}

```





