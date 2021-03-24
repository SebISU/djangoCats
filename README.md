# Api w DRF


## Logowanie
/login/
GET - informacja
POST - przekazanie username oraz password, w odpowiedzi token
{
    "username": "sdfg",
    "password": "sdfggfds"
}


## Users
/users/<id>/ id=user
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
/hunting/<catid>/  catid=id kota
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
