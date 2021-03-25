# Api w DRF


## Logowanie
path /login/

GET - informacja

POST - przekazanie username oraz password, w odpowiedzi token

{
    "username": "sdfg",
    "password": "sdfggfds"
}


## Users
path /users/id/ id=user

GET - uzyskanie informacji o uzytkowniku oraz listy jego kotow

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
path /hunting/idcat/  idcat=id kota

GET - informacje o kocie

{
    "id": 5,
    "name": "arnold",
    "bodyColor": "5",
    "gender": true,
    "owner": 1
}

POST - przekazanie informacji o polowaniu. Daty, lista zdobyczy ...

{
    "loots":["mouse", "rat", "fish", "bird"],
    "dateStart" : "2021-03-22",
    "dateEnd" : "2021-03-22",
    "hunter" : 1
}

# Zadania DevOps

Postawiem na serwerze Linode, poniewaz mam kod rabatowy.

Zapraszam pod adres IP: 139.162.156.157

Username:admin
password:admin

Api sprawdzalem postmanem, moge podeslac ss-y

# React

Nie uczylem sie
