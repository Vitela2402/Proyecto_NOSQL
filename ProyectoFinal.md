# Proyecto Final

## API

### Importación del API

```python
import requests
import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["ProyectStore"]
collection = my_db["Carts"]
response = []
response.append(requests.get(url="https://fakestoreapi.com/carts", headers={'User-Agent':'Custom'}))
response[0] = response[0].json()
print(response[0])
collection.insert_many(response[0])

collection2 = my_db["Users"]
response = []
response.append(requests.get(url="https://fakestoreapi.com/users", headers={'User-Agent':'Custom'}))
response[0] = response[0].json()
print(response[0])
collection2.insert_many(response[0])

collection3 = my_db["Products"]
response = []
response.append(requests.get(url="https://fakestoreapi.com/products", headers={'User-Agent':'Custom'}))
response[0] = response[0].json()
print(response[0])
collection3.insert_many(response[0])
```


## monetdb
#### Objetivo Base Columnar
El objetivo de esta base de datos columnar es poder facilitar la lectura, la vista, y búsqueda de la información que creímos más pertinente de la API que descargamos.

#### Importacion

```
docker exec monetdb monetdb create -p monetdb ProyectStore
docker exec -it monetdb  mclient -u monetdb -d ProyectStore

CREATE USER "ProyectStore" WITH PASSWORD 'ProyectStore' NAME 'ProyectStore' SCHEMA "sys";
CREATE SCHEMA "ProyectStore" AUTHORIZATION "ProyectStore";
ALTER USER "ProyectStore" SET SCHEMA "ProyectStore";
\q

docker exec -it monetdb  mclient -u ProyectStore -d ProyectStore

CREATE TABLE users (
c_v numeric (10),
c_id varchar(200),
address_city varchar(200),
address_geolocation varchar(200),
address_number int,
address_street varchar(200),
address_zipcode varchar(200),
email varchar(200),
id int,
name_firstname varchar(200),
name_lastname varchar(200),
password varchar(200),
phone varchar(200),
username varchar(200));

CREATE TABLE carts (
c_v numeric (10), 
c_id varchar (200), 
date date, id int, 
products varchar (200), 
userid int);

CREATE TABLE products(
c_id varchar(200),
category varchar(200),
description varchar(200),
id int,
image varchar(200),
price double,
rating_count int,
rating_rate double,
title varchar(300)
);

COPY INTO users FROM 'Users.csv' ON CLIENT USING DELIMITERS ',', E'\n', '';
COPY INTO carts FROM 'Carts.csv' ON CLIENT USING DELIMITERS ',', E'\n', '';
COPY INTO products FROM 'Products.csv' ON CLIENT USING DELIMITERS ',', E'\n', '';
```
#### Queries

1)

```SQL

```

2)
```SQL

```

3)

```SQL

```

## Neo4j

#### Importacion
.....Parar, en docker, los containers que ocupen los puertos 7474 o 7687.....
docker run \
    -p 7474:7474 -p 7687:7687 \
    -v $PWD/data:/data -v $PWD/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS=\[\"apoc\"\] \
    neo4j:4.0

.....Abrir navegador y poner la siguiente liga.....
http://localhost:7474/browser/

.....Clave y usuario para iniciar sesión.....
neo4j

.....Cargar api en neo4j.....
CALL apoc.load.json("http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline");




.......para entrar a terminal neo4j......
docker exec -it testneo4j bash
cypher-shell -u neo4j -p test


#### Queries


## Conclusion

PURA EXPLICACION
