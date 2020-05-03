import pymongo


def get_mongodb(user, password, host):
    """  mongodb+srv://ricepotato:<password@cluster0-gpvm5.gcp.mongodb.net/wetube?retryWrit """
    connection_string = (
        "mongodb+srv://{user}:{password}@{host}"
    )
    client = pymongo.MongoClient(
        connection_string, ssl=True, tlsAllowInvalidCertificates=True
    )
    return client
