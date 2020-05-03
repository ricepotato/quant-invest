import ssl
import pymongo
import configparser


def get_mongo_client(host, user, password):
    """  mongodb+srv://ricepotato:<password>@cluster0-gpvm5.gcp.mongodb.net/wetube?retryWrit """
    connection_string = f"mongodb+srv://{user}:{password}@{host}"
    client = pymongo.MongoClient(
        connection_string, ssl=True, tlsAllowInvalidCertificates=True
    )
    return client


def get_db():
    config = configparser.ConfigParser()
    config.read("conf/mongodb.conf")
    section = host = config["mongodb"]
    host = section["host"]
    user = section["user"]
    password = section["password"]

    client = get_mongo_client(host, user, password)
    return client
