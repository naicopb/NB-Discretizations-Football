from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.primera_y_segunda

def main():
    historical = convertInArray(getHistorical())
    counter = 0
    counterEmpates = 0
    for i in range(0, len(historical)):
        counter += 1
        if historical[i]['FTR'] == 'D':
            counterEmpates += 1

    print(counter)
    print(counterEmpates)
    print(counterEmpates/counter)

def imprime(array):
    for i in range(0, len(array)):
        print(array[i])

def convertInArray(historico):
    array = []
    for jornada in historico:
        array.append(jornada)
    return array

def getHistorical():
    try:
        query = {}
        query['liga'] = 'primera_division'
        resultado = db.datos_completos.find(query)
        return resultado

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')

main()
