https://medium.com/better-programming/introduction-to-locust-an-open-source-load-testing-tool-in-python-2b2e89ea1ff

When user has autorized or registered he gets a token that he must provides in each request to server.

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
###### VALID

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

Location: /api/chats

Cookies:
user_id={id}
token={...}
```
###### INVALID

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
###### VALID
```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

Location: /api/login

Cookies:
user_id={' '}
token={' '}
```

## Chats
### /api/chats

It is required access\_token and user\_id in request cookies.
#### REQUESTS

* `GET` get user`s chats

* `POST ` create chat

```
Content-type: application/x-www-form-urlencoded

Body:	title: {title}
```

* `DELETE` delete user from chat 

```
Params : chat_id={chat_id}

```
#### RESPONSES
###### VALID 
* `GET`

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

*  `POST`

```
Status: 201

Content-type: application/json

Body: {"status": "ok"}

```

*  `DELETE`

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

```

###### INVALID 

```
Status: 400/404/403

Content-type: application/json

Body:
{"error": "{description of error}"}

```

## Chat 

### /api/chats/{chat_id}
It is required access\_token and user\_id in request cookies.
#### REQUESTS

* `GET` get chat`s messages

* `POST ` send message in chat (only authorized user with access to chat)

```
Content-type: application/x-www-form-urlencoded

Body:	content: {content}
```

* ` PUT ` change chat title (only authorized user with access to chat)

```
Content-type: application/x-www-form-urlencoded

Body:	title: {title}
```

* `DELETE` delete user`s messege (only authorized user`s messages)

```
Params : id={mes_id}

```


#### RESPONSES
###### VALID 
* `GET`


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

*  `POST`

```
Status: 201

Content-type: application/json

Body: {"status": "ok"}

```

*  `PUT`

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

```

*  `DELETE`

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

```

###### INVALID 

```
Status: 400/404/403

Content-type: application/json

Body:
{"error": "{description of error}"}


```

## User

### /api/user/{user_id}
It is required access\_token and user\_id in request cookies.
#### REQUESTS

* `GET` get user information

```
Params : name={name}
```

* `POST ` create user and auth 

```
Content-type: application/x-www-form-urlencoded

Body:
		name: {name}
		password: {password}
		email: {email}

```

* ` PUT ` change user information (only authorized)

```
Content-type: application/x-www-form-urlencoded

Body:
		name: {name}
		email: {email}

```

* `DELETE` delete user (only authorized)

#### RESPONSES
###### VALID 
* `GET`


```
Status: 200

Content-type: application/json

Body:
{
  "user": 
    {
      "name": {name},
      "email": {email}
    }
}

```

*  `POST`

```
Status: 201

Content-type: application/json

Body: {"status": "ok"}

Location: /api/chats

Cookies:
user_id={id}
token={...}
```

*  `PUT`

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

```

*  `DELETE`

```
Status: 200

Content-type: application/json

Body: {"status": "ok"}

```

###### INVALID 

```
Status: 400/404/403

Content-type: application/json

Body:
{"error": "{description of error}"}


