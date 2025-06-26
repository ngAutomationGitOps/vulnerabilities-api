from pymongo import MongoClient


def get_db():
    client = MongoClient("mongodb://128.2.99.223:27017/")
    return client["vulnerabilities"]

