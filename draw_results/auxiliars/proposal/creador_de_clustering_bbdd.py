from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.datos_finales_paper

import numpy as np
import GPy

def main():
    particiones = convertInArray(getHistorical())
    counter = 0
    WAP = 0
    WAR = 0
    for i in range(0, len(particiones)):
        counter += 1
        WAP += particiones[i]['WAP']
        WAR += particiones[i]['WAR']

    WAP = WAP/counter
    WAR = WAR/counter
    WAPWAR = (WAP+WAR)/2

    array_wap_true_node1 = []
    array_wap_true_node2 = []
    array_wap_true_node3 = []
    array_wap_false_node1 = []
    array_wap_false_node2 = []
    array_wap_false_node3 = []

    array_war_true_node1 = []
    array_war_true_node2 = []
    array_war_true_node3 = []
    array_war_false_node1 = []
    array_war_false_node2 = []
    array_war_false_node3 = []

    array_wapwar_true_node1 = []
    array_wapwar_true_node2 = []
    array_wapwar_true_node3 = []
    array_wapwar_false_node1 = []
    array_wapwar_false_node2 = []
    array_wapwar_false_node3 = []

    for i in range(0, len(particiones)):
        if particiones[i]['WAP'] > WAP:
            particiones[i]['claseWAP'] = 1
            array_wap_true_node1.append(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'])
            array_wap_true_node2.append(particiones[i]['varianzaMaximaDeLasparticiones'])
            array_wap_true_node3.append(particiones[i]['diferenciaEntreAmplitudes'])
        else:
            particiones[i]['claseWAP'] = 0
            array_wap_false_node1.append(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'])
            array_wap_false_node2.append(particiones[i]['varianzaMaximaDeLasparticiones'])
            array_wap_false_node3.append(particiones[i]['diferenciaEntreAmplitudes'])

        if particiones[i]['WAR'] > WAR:
            particiones[i]['claseWAR'] = 1
            array_war_true_node1.append(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'])
            array_war_true_node2.append(particiones[i]['varianzaMaximaDeLasparticiones'])
            array_war_true_node3.append(particiones[i]['diferenciaEntreAmplitudes'])
        else:
            particiones[i]['claseWAR'] = 0
            array_war_false_node1.append(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'])
            array_war_false_node2.append(particiones[i]['varianzaMaximaDeLasparticiones'])
            array_war_false_node3.append(particiones[i]['diferenciaEntreAmplitudes'])

        if (particiones[i]['WAP'] + particiones[i]['WAR'])/2 > WAPWAR:
            particiones[i]['claseWAPWAR'] = 1
            array_wapwar_true_node1.append(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'])
            array_wapwar_true_node2.append(particiones[i]['varianzaMaximaDeLasparticiones'])
            array_wapwar_true_node3.append(particiones[i]['diferenciaEntreAmplitudes'])
        else:
            particiones[i]['claseWAPWAR'] = 0
            array_wapwar_false_node1.append(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'])
            array_wapwar_false_node2.append(particiones[i]['varianzaMaximaDeLasparticiones'])
            array_wapwar_false_node3.append(particiones[i]['diferenciaEntreAmplitudes'])

    print('llego hasta aquí')
    for i in range(0, len(particiones)):
        particiones[i]['probWAP'] = calculaProbabilidad(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'], array_wap_true_node1, array_wap_false_node1, particiones[i]['varianzaMaximaDeLasparticiones'], array_wap_true_node2, array_wap_false_node2, particiones[i]['diferenciaEntreAmplitudes'], array_wap_true_node3, array_wap_false_node3)
        particiones[i]['probWAR'] = calculaProbabilidad(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'], array_war_true_node1, array_war_false_node1, particiones[i]['varianzaMaximaDeLasparticiones'], array_war_true_node2, array_war_false_node2, particiones[i]['diferenciaEntreAmplitudes'], array_war_true_node3, array_war_false_node3)
        particiones[i]['probWAPWAR'] =  calculaProbabilidad(particiones[i]['distanciaMinimaEntreCentroidesConsecutivos'], array_wapwar_true_node1, array_wapwar_false_node1, particiones[i]['varianzaMaximaDeLasparticiones'], array_wapwar_true_node2, array_wapwar_false_node2, particiones[i]['diferenciaEntreAmplitudes'], array_wapwar_true_node3, array_wapwar_false_node3)
        print(str(i) + ' de ' + str(len(particiones)) + ' - ' + str(i/len(particiones)))

    insertData(particiones)

def calculaProbabilidad(node1, array_true_node1, array_false_node1, node2, array_true_node2, array_false_node2, node3, array_true_node3, array_false_node3):
    probNode1_X = calculaProbabilidadContinua(node1, array_true_node1)/(calculaProbabilidadContinua(node1, array_true_node1)+calculaProbabilidadContinua(node1, array_false_node1))
    probNode1_NX = calculaProbabilidadContinua(node1, array_false_node1)/(calculaProbabilidadContinua(node1, array_true_node1)+calculaProbabilidadContinua(node1, array_false_node1))

    probNode2_X = calculaProbabilidadContinua(node2, array_true_node2)/(calculaProbabilidadContinua(node2, array_true_node2)+calculaProbabilidadContinua(node2, array_false_node2))
    probNode2_NX = calculaProbabilidadContinua(node2, array_false_node2)/(calculaProbabilidadContinua(node2, array_true_node2)+calculaProbabilidadContinua(node2, array_false_node2))

    probNode3_X = calculaProbabilidadContinua(node3, array_true_node3)/(calculaProbabilidadContinua(node3, array_true_node3)+calculaProbabilidadContinua(node3, array_false_node3))
    probNode3_NX = calculaProbabilidadContinua(node3, array_false_node3)/(calculaProbabilidadContinua(node3, array_true_node3)+calculaProbabilidadContinua(node3, array_false_node3))

    numerador = 0.5*probNode1_X*probNode2_X*probNode3_X
    denominador1 = 0.5*probNode1_X*probNode2_X*probNode3_X
    denominador2 = 0.5*probNode1_NX*probNode2_NX*probNode3_NX

    return numerador/(denominador1+denominador2)

def calculaProbabilidadContinua(node, array):
    return (1/(np.sqrt(2*np.var(array)*np.pi)))*np.exp(-((pow((node-np.mean(array)), 2))/(2*np.var(array))))

def insertData(array):
    try:
        resultado = db.particiones_con_probDeBondad_asociada_3.insert_many(array)
        return 'Todo OK'
    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')

def getHistorical():
    try:
        resultado = db.particiones_con_error_asociado_3.find({})
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
