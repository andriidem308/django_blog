# REST API Blog with Django
Here I have created a simple blog with users, posts and availability to like these posts.

To start the project you need to do following steps:
1. clone this repository with `git clone`
2. go to cloned repository with `cd django_blog`
3. create and activate virtual environment
4. install requirements with command `make requirements` in your terminal
5. migrate database tables with `make migrations`, then `make migrate`
6. run application with `make run`


There is a list of possible urls:

**1. Creates a user**

POST http://127.0.0.1:8000/users/users/, 

data example: 
`{"username": "testuser", "password": "testpassword"}`


**2. Show list of users**

GET http://127.0.0.1:8000/users/users/, 


**3. Get a token for user**

POST http://127.0.0.1:8000/api/token/

data example: 
`{"username": "testuser", "password": "testpassword"}`


**4. Refresh token**

POST http://127.0.0.1:8000/api/token/refresh

data example: 
`{"refresh": "$REFRESH_TOKEN$"}`

**5. Show posts**

GET http://127.0.0.1:8000/api/posts/

headers: 
`{"Authorization": "Bearer $ACCESS_TOKEN$"}`

**6. Create post**

POST http://127.0.0.1:8000/api/posts/

data example:
`{"content": "Some text inside post"}`

headers: 
`{"Authorization": "Bearer $ACCESS_TOKEN$"}`

**7. Like post**

POST http://127.0.0.1:8000/api/posts/1/post_like/

headers: 
`{"Authorization": "Bearer $ACCESS_TOKEN$"}`

**8. Unlike post**

POST http://127.0.0.1:8000/api/posts/1/post_unlike/

headers: 
`{"Authorization": "Bearer $ACCESS_TOKEN$"}`

**9. Analytics**

GET http://127.0.0.1:8000/api/analytics?date_from=2023-03-03&date_to=2023-04-03

**10. Run bot which creates users, their posts and likes some posts**

GET http://127.0.0.1:8000/api/bot_run

<br><br>
Also we can **delete** users and posts using method **DELETE** for requests to endpoints we used to create them
