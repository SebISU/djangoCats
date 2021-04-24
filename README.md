# Django Cats

To run this app the first time follow these steps:
1. `docker-compose build`
2. `docker-compose run web make migration`
3. `docker-compose run web make migrate`
4. `docker-compose run web make superuser`
5. `docker-compose up`

Server runs on `http://127.0.0.1:8000/`  
Go to `http://127.0.0.1:8000/admin/`  
You can login with credentials:  
- username: admin
- password: admin

----
# Endpoints
## Login 
path /login/

GET - info

POST - Pass username and password. Token as a response

{  
    "username": "sdfg",  
    "password": "sdfggfds"  
}  

## Users
path /users/id/ id=user_id

GET - get info about user and list of his cats

{  
    "id": 1,  
    "cats": [  
        {  
            "id": 1,  
            "name": "romek",  
            "bodyColor": "1",  
            "gender": true,  
            "owner": 1  
        },  
        {  
            "id": 4,  
            "name": "bunia",  
            "bodyColor": "4",  
            "gender": false,  
            "owner": 1  
        }]  
}  

## Hunting
path /hunting/idcat/  idcat=id cat

GET - info about cat

{  
    "id": 5,
    "name": "arnold",  
    "bodyColor": "5",  
    "gender": true,  
    "owner": 1  
}  

POST - Passing info about hunting. Date, list of loots ...

{  
    "loots":["mouse", "rat", "fish", "bird"],  
    "dateStart" : "2021-03-22",  
    "dateEnd" : "2021-03-22",  
    "hunter" : 1  
}  
