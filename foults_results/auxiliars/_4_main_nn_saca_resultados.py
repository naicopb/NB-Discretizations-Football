from pymongo import MongoClient
import numpy as np


client = MongoClient('localhost:27017')
db = client.articulo3

def main():
    return convertInArray(getHistorical())

def convertInArray(historical):
    array = []
    for element in historical:
        array.append(element)
    return array

def getHistorical():
    try:
        query = {}
        resultado = db.articulo3_nn.find(query)
        return resultado

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')
