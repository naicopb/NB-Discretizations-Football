from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.datos_finales_paper

def main():
    return convertInArray(getHistorical())

def getHistorical():
    try:
        query = {}
        resultado = db.dixonycoles_2.find(query)
        return resultado

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')

def convertInArray(historical):
    array = []
    for element in historical:
        array.append(element)
    return array
