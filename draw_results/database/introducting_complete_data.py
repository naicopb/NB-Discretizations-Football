from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.primera_y_segunda
import csv

def main ():
    with open('./data/22-23_primera.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        array_de_objetos = []
        line_count = 0
        array_keys = []
        for row in csv_reader:
            if line_count == 0:
                for i in range(0, len(row)):
                    array_keys.append(row[i])
                line_count += 1
            else:
                object = {}
                object['temporada'] = '2022-2023'
                object['liga'] = 'primera_division'
                object['numero_partido'] = line_count
                for i in range(0, len(array_keys)):
                    object[array_keys[i]] = row[i]
                line_count += 1
                array_de_objetos.append(object)
        return insertHistorical(array_de_objetos)


def insertHistorical(array):
    try:
        db.datos_completos.insert_many(array)
        return ('Datos insertados satisfactoriamente')

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')


print(main())
