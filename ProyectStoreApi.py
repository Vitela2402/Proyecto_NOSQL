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