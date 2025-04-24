from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.datos_finales_paper

import numpy as np
import GPy

def main():
    particiones = convertInArray(getHistorical())
    print(particiones[0])
    maxWAP = 0
    objetoWAP = {}
    maxWAR = 0
    objetoWAR = {}
    maxWAPWAR = 0
    objetoWAPWAR = {}
    maxMediaWAPWAR = 0
    objetoMediaWAPWAR = {}

    for i in range(0, len(particiones)):
        if particiones[i]['probWAP'] > maxWAP:
            maxWAP = particiones[i]['probWAP']
            objetoWAP = particiones[i]
        if particiones[i]['probWAR'] > maxWAR:
            maxWAR = particiones[i]['probWAR']
            objetoWAR = particiones[i]
        if particiones[i]['probWAPWAR'] > maxWAPWAR:
            maxWAPWAR = particiones[i]['probWAPWAR']
            objetoWAPWAR = particiones[i]
        if (particiones[i]['probWAP'] + particiones[i]['probWAR'])/2 > maxMediaWAPWAR:
            maxMediaWAPWAR = (particiones[i]['probWAP'] + particiones[i]['probWAR'])/2
            objetoMediaWAPWAR = particiones[i]


    print('#######')
    print('WAP')
    print(maxWAP)
    print(objetoWAP['particion'])
    print(objetoWAP['WAP'])
    print(objetoWAP['WAR'])
    print('#######')
    print('WAR')
    print(maxWAR)
    print(objetoWAR['particion'])
    print(objetoWAR['WAP'])
    print(objetoWAR['WAR'])
    print('#######')
    print('WAPWAR')
    print(maxWAPWAR)
    print(objetoWAPWAR['particion'])
    print(objetoWAPWAR['WAP'])
    print(objetoWAPWAR['WAR'])
    print('#######')
    print('mediaWAPWAR')
    print(maxMediaWAPWAR)
    print(objetoMediaWAPWAR['particion'])
    print(objetoMediaWAPWAR['WAP'])
    print(objetoMediaWAPWAR['WAR'])
    print('#######')

def getHistorical():
    try:
        resultado = db.particiones_con_probDeBondad_asociada_3.find({})
        return resultado

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')

def convertInArray(historical):
    array = []
    for element in historical:
        array.append(element)
    return array

main()
