# Proyecto Final

Authors: Yul Padilla, Pablo Vitela, Juan Manuel Ambriz


## API

### Importación del API 
.

```python
# Guardar ProyectStoreApi.py o copiar los siguiente 

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
#### Queries Mongodb

1) A través del products_id nos dice, con count, cuántos hay de cada producto y lo contabiliza en sum:
```
  db.Carts.aggregate( [ { $group: { "_id": "$products",  count: { $sum:1 } } }]);
```

2) Cuántas veces se agregó al carrito cada producto:
```
 db.Carts.aggregate([ { $unwind: '$products' }, { $project: { _id: 0, "products.productId": 1, 'products.quantity': 1 } }, { $group: { _id: "$products" } }]);
```

3) Da información de usuario por pedido:
```

db.Carts.aggregate([{$lookup: {from: "Users", localField: "userId",  foreignField: "id", as: "UserInfo"}} ])
```

## Monetdb
#### Objetivo Base Columnar
El objetivo de esta base de datos columnar es poder facilitar la lectura, la vista, y búsqueda de la información de la API que descargamos.

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
date date, 
num int, 
products_id int,
quantity int, 
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

# CAMBIAR PATH

copy offset 2 into Users from '/path/to/my/Users.csv' on client using delimiters ',',E'\n',E'\"' null as ' ';
copy offset 2 into Carts from '/path/to/my/Carts.csv' on client using delimiters ',',E'\n',E'\"' null as ' ';
copy offset 2 into Products from '/path/to/my/Products.csv' on client using delimiters ',',E'\n',E'\"' null as ' ';
```
#### Queries

1) Cuál es el producto más caro:


```
SELECT price, count(*) as number FROM product GROUP BY product, price LIMIT 10;
```



2) Cuál es el producto con más rating count:

```
SELECT rating_count, count(*) as number FROM product GROUP BY rating_count LIMIT 10;
```

3) Cuántos productos son para hombres:


```
SELECT category, count(*) as number FROM product WHERE category='men's clothing' GROUP BY category;
```

```
## Neo4j

#### Importacion

Abrir http://localhost:7474/browser/

LOAD CSV WITH HEADERS from "file:///Users.csv" as row create (n:users) set n =row 
LOAD CSV WITH HEADERS from "file:///Products.csv" as row create (n:products) set n =row
LOAD CSV WITH HEADERS from "file:///Carts.csv" as row create (n:carts) set n =row 

MATCH (u:users),(c:carts) WHERE u.id = c.userId CREATE (u)-[:addProducts]->(c)
MATCH (c:carts),(p:products) WHERE c.products_id = p.id CREATE (c)-[:CONTAINS]->(p)
```

#### Queries
1) Cuál es el precio más alto de todos los productos:
```
 match (p:products) return p.title as Titles, p.category as Categories, max(p.price) as max_price order by max_price desc
```
2) La última fecha en la que agrego un producto al carrito cada usuario:
```
 match (u:users)-[:addProducts]->(c:carts) return u.username as name, max(c.date) as max_ord_date order by max_ord_date
```
3) Cuántos productos se agregaron al carrito por categoría:

```
 match (p:products)<-[:ORDERS]-(c:carts) return p.category as name, count(c.products_id) as products_count order by p.category
```

