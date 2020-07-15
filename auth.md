When user has autorized or registered he gets a token that he must provides in each request to server.
## REGISTRATION 
#### REQUEST
```
POST /api/reg

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

Location: /api/chats

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
POST /api/login

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

Location: /api/chats

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


## Deauthorization 
It is required access\_token and user\_id in request cookies.
#### REQUEST 
```
GET /api/logout

```
#### RESPONSE
* valid request

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

Location: /api/login

Cookies:
user_id={' '}
token={' '}
```

## Chats` page
It is required access\_token and user\_id in request cookies.
#### REQUEST

```
GET /api/chats
```
#### RESPONSE

```
Status: 200

Content-type: application/json

Body:
{
  "chats": [
    {
      "id": {id},
      "last_message": {last_message},
      "last_message_time": {last_message},
      "sender_id": {sender_id},
      "title": {title}
    },
    ...
    ]
}

```

## Create new chat
It is required access\_token and user\_id in request cookies.
#### REQUEST
```
POST /api/chats

Content-type: application/x-www-form-urlencoded

Body:
title: {title}
```
#### RESPONSE
* valid request

```
Status: 201

Content-type: application/json

Body: {"status": "ok"}

Location: /api/chats/{chat_id}

```
* invalid request

```
Status: 400 or 409

Content-type: application/json

Body:
{"error": "{description of error}"}

```

## Chat`s messages
It is required access\_token and user\_id in request cookies.
#### REQUEST

```
GET /api/chats/{chat_id}
```
#### RESPONSE

```
Status: 200

Content-type: application/json

Body:
{
  "messages": [
    {
      "content": {content},
      "id": {id},
      "sender_id": {sender_id},
      "time": {time}
    },
     ...
    ]
}

```

## Send message
It is required access\_token and user\_id in request cookies.
#### REQUEST
```
POST /api/chats/{chat_id}

Content-type: application/x-www-form-urlencoded

Body:
content: {content}
```
#### RESPONSE
* valid request

```
Status: 201

Content-type: application/json

Body: {"status": "ok"}

```
* invalid request

```
Status: 400 or 404

Content-type: application/json

Body:
{"error": "{description of error}"}


