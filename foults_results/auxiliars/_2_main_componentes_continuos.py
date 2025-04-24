from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.all_leagues_bbdd

import numpy as np

def main():
    temporadas = ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    historical = convertInArray(getHistorical())

    array_faltas_total = []
    array_resultados = []

    array_node1_ht_0 = []
    array_node1_ht_25 = []
    array_node1_ht_30 = []
    array_node1_ht_35 = []
    array_node1_at_0 = []
    array_node1_at_25 = []
    array_node1_at_30 = []
    array_node1_at_35 = []
    array_node2_ht_0 = []
    array_node2_ht_25 = []
    array_node2_ht_30 = []
    array_node2_ht_35 = []
    array_node2_at_0 = []
    array_node2_at_25 = []
    array_node2_at_30 = []
    array_node2_at_35 = []
    totalPartidos_0 = 0
    totalPartidos_25 = 0
    totalPartidos_30 = 0
    totalPartidos_35 = 0
    totalPartidosTotal = 0

    for temporada in temporadas:
        #array_partidos_por_temporada = []
        equipos_con_faltas_recibidas = {}
        equipos_con_faltas_efectuadas = {}
        arbitro_con_faltas = {}
        for i in range(0, len(historical)):
            if historical[i]['temporada'] == temporada:

                # 1) Creo los arrays si no están creados
                if historical[i]['HomeTeam'] not in equipos_con_faltas_recibidas.keys():
                    equipos_con_faltas_recibidas[historical[i]['HomeTeam']] = 0
                    equipos_con_faltas_efectuadas[historical[i]['HomeTeam']] = 0

                if historical[i]['AwayTeam'] not in equipos_con_faltas_efectuadas.keys():
                    equipos_con_faltas_recibidas[historical[i]['AwayTeam']] = 0
                    equipos_con_faltas_efectuadas[historical[i]['AwayTeam']] = 0

                # 2) Asigno a cada equipo su nodo
                node1_HomeTeam = asignaNodoFaltas(historical[i]['HomeTeam'], equipos_con_faltas_recibidas)
                node1_AwayTeam = asignaNodoFaltas(historical[i]['AwayTeam'], equipos_con_faltas_efectuadas)
                #print(node1_HomeTeam)
                #print(node1_AwayTeam)
                node2_HomeTeam = asignaNodoFaltas(historical[i]['HomeTeam'], equipos_con_faltas_efectuadas)
                node2_AwayTeam = asignaNodoFaltas(historical[i]['AwayTeam'], equipos_con_faltas_recibidas)
                #print(node2_HomeTeam)
                #print(node2_AwayTeam)

                # 3) Calculo la probabilidad
                #25, 30, 35 mas
                if temporada in ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']:
                    array_resultados.append({'temporada': temporada, 'HomeTeam': historical[i]['HomeTeam'], 'AwayTeam': historical[i]['AwayTeam'], 'faltas': int(historical[i]['HF']) + int(historical[i]['AF'])})
                    #array_resultados[len(array_resultados)-1]['prob25'], array_resultados[len(array_resultados)-1]['prob30'], array_resultados[len(array_resultados)-1]['prob35'], array_resultados[len(array_resultados)-1]['prob40'] = equilibrador(calculaProbabilidad(0, 25, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total), calculaProbabilidad(25, 30, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total), calculaProbabilidad(30, 35, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total), calculaProbabilidad(35, 1000, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total))
                    #array_resultados[len(array_resultados)-1]['prob25'] = calculaProbabilidad(node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, )


                    array_resultados[len(array_resultados)-1]['prob25'] = calculaProbabilidad(node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node1_ht_0, array_node1_at_0, array_node2_ht_0, array_node2_at_0, np.concatenate((array_node1_ht_25, array_node1_ht_30, array_node1_ht_35)), np.concatenate((array_node1_at_25, array_node1_at_30, array_node1_at_35)), np.concatenate((array_node2_ht_25, array_node2_ht_30, array_node2_ht_35)), np.concatenate((array_node2_ht_25, array_node2_ht_30, array_node2_ht_35)), totalPartidos_0, totalPartidosTotal)
                    array_resultados[len(array_resultados)-1]['prob30'] = calculaProbabilidad(node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node1_ht_25, array_node1_at_25, array_node2_ht_25, array_node2_at_25, np.concatenate((array_node1_ht_0, array_node1_ht_30, array_node1_ht_35)), np.concatenate((array_node1_at_0, array_node1_at_30, array_node1_at_35)), np.concatenate((array_node2_ht_0, array_node2_ht_30, array_node2_ht_35)), np.concatenate((array_node2_ht_0, array_node2_ht_30, array_node2_ht_35)), totalPartidos_25, totalPartidosTotal)
                    array_resultados[len(array_resultados)-1]['prob35'] = calculaProbabilidad(node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node1_ht_30, array_node1_at_30, array_node2_ht_30, array_node2_at_30, np.concatenate((array_node1_ht_0, array_node1_ht_25, array_node1_ht_35)), np.concatenate((array_node1_at_0, array_node1_at_25, array_node1_at_35)), np.concatenate((array_node2_ht_0, array_node2_ht_25, array_node2_ht_35)), np.concatenate((array_node2_ht_0, array_node2_ht_25, array_node2_ht_35)), totalPartidos_30, totalPartidosTotal)
                    array_resultados[len(array_resultados)-1]['prob40'] = calculaProbabilidad(node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node1_ht_35, array_node1_at_35, array_node2_ht_35, array_node2_at_35, np.concatenate((array_node1_ht_0, array_node1_ht_25, array_node1_ht_30)), np.concatenate((array_node1_at_0, array_node1_at_25, array_node1_at_30)), np.concatenate((array_node2_ht_0, array_node2_ht_25, array_node2_ht_30)), np.concatenate((array_node2_ht_0, array_node2_ht_25, array_node2_ht_30)), totalPartidos_35, totalPartidosTotal)


                # 4) Añado elemento a los arrays:
                if (int(historical[i]['HF']) + int(historical[i]['AF'])) >= 0 and (int(historical[i]['HF']) + int(historical[i]['AF'])) < 25:
                    array_node1_ht_0.append(node1_HomeTeam)
                    array_node1_at_0.append(node1_AwayTeam)
                    array_node2_ht_0.append(node2_HomeTeam)
                    array_node2_at_0.append(node2_AwayTeam)
                    totalPartidos_0 += 1
                if (int(historical[i]['HF']) + int(historical[i]['AF'])) >= 25 and (int(historical[i]['HF']) + int(historical[i]['AF'])) < 30:
                    array_node1_ht_25.append(node1_HomeTeam)
                    array_node1_at_25.append(node1_AwayTeam)
                    array_node2_ht_25.append(node2_HomeTeam)
                    array_node2_at_25.append(node2_AwayTeam)
                    totalPartidos_25 += 1
                if (int(historical[i]['HF']) + int(historical[i]['AF'])) >= 30 and (int(historical[i]['HF']) + int(historical[i]['AF'])) < 35:
                    array_node1_ht_30.append(node1_HomeTeam)
                    array_node1_at_30.append(node1_AwayTeam)
                    array_node2_ht_30.append(node2_HomeTeam)
                    array_node2_at_30.append(node2_AwayTeam)
                    totalPartidos_30 += 1
                if (int(historical[i]['HF']) + int(historical[i]['AF'])) >= 35 and (int(historical[i]['HF']) + int(historical[i]['AF'])) < 100:
                    array_node1_ht_35.append(node1_HomeTeam)
                    array_node1_at_35.append(node1_AwayTeam)
                    array_node2_ht_35.append(node2_HomeTeam)
                    array_node2_at_35.append(node2_AwayTeam)
                    totalPartidos_35 += 1
                totalPartidosTotal += 1

                # 5) Actualizo el listado de faltas y puntos de cada equipo
                equipos_con_faltas_efectuadas[historical[i]['HomeTeam']] += int(historical[i]['HF'])
                equipos_con_faltas_efectuadas[historical[i]['AwayTeam']] += int(historical[i]['AF'])
                equipos_con_faltas_recibidas[historical[i]['HomeTeam']] += int(historical[i]['AF'])
                equipos_con_faltas_recibidas[historical[i]['AwayTeam']] += int(historical[i]['HF'])

                # 6) Guardo los partidos correspondientes a a las diez últimas temporadas
    #for i in range(0, len(array_resultados)):
    #    print(array_resultados[i])
    #    print(float(array_resultados[i]['prob25']) + float(array_resultados[i]['prob30']) +float(array_resultados[i]['prob35']) + float(array_resultados[i]['prob40']) )
    return array_resultados
        #break

def equilibrador(a, b, c, d):
    if a == 0 and b == 0 and c == 0 and d == 0:
        return 0, 0, 0, 0
    else:
        return a/(a+b+c+d), b/(a+b+c+d), c/(a+b+c+d), d/(a+b+c+d)

def calculaProbabilidad(value1, value2, value3, value4, arr1, arr2, arr3, arr4, arrNo1, arrNo2, arrNo3, arrNo4, partidosPro, partidosTotal):
    probValue1 = calculaProbabilidadContinua(value1, arr1)/(calculaProbabilidadContinua(value1, arr1)+calculaProbabilidadContinua(value1, arrNo1))
    probValue1_N = calculaProbabilidadContinua(value1, arrNo1)/(calculaProbabilidadContinua(value1, arr1)+calculaProbabilidadContinua(value1, arrNo1))

    probValue2 = calculaProbabilidadContinua(value2, arr2)/(calculaProbabilidadContinua(value2, arr2)+calculaProbabilidadContinua(value2, arrNo2))
    probValue2_N = calculaProbabilidadContinua(value2, arrNo2)/(calculaProbabilidadContinua(value2, arr2)+calculaProbabilidadContinua(value2, arrNo2))

    probValue3 = calculaProbabilidadContinua(value3, arr3)/(calculaProbabilidadContinua(value3, arr3)+calculaProbabilidadContinua(value3, arrNo3))
    probValue3_N = calculaProbabilidadContinua(value3, arrNo3)/(calculaProbabilidadContinua(value3, arr3)+calculaProbabilidadContinua(value3, arrNo3))

    probValue4 = calculaProbabilidadContinua(value4, arr4)/(calculaProbabilidadContinua(value4, arr4)+calculaProbabilidadContinua(value4, arrNo4))
    probValue4_N = calculaProbabilidadContinua(value4, arrNo4)/(calculaProbabilidadContinua(value4, arr4)+calculaProbabilidadContinua(value4, arrNo4))

    if partidosTotal == 0:
        return 0
    numerador = (partidosPro/partidosTotal)*probValue1*probValue2*probValue3*probValue4
    denominador1 = (partidosPro/partidosTotal)*probValue1*probValue2*probValue3*probValue4
    denominador2 = ((partidosTotal-partidosPro)/partidosTotal)*probValue1_N*probValue2_N*probValue3_N*probValue4_N
    if denominador1 == 0 and denominador2 == 0:
        return 0
    return numerador/(denominador1+denominador2)

def calculaProbabilidadContinua(goles, array):
    return (1/(np.sqrt(2*np.var(array)*np.pi)))*np.exp(-((pow((goles-np.mean(array)), 2))/(2*np.var(array))))

def discriminaCantidades(array, extremoInferior, extremoSuperior):
    cantFavor = 0
    cantContra = 0
    for i in range(0, len(array)):
        if array[i] >= extremoInferior and array[i] < extremoSuperior:
            cantFavor += 1
        else:
            cantContra += 1
    return cantFavor, cantContra

def actualizaNodes(array, node1, node2, cantidad):
    esta = False
    for i in range(0, len(array)):
        if array[i]['elemento1'] == node1 and array[i]['elemento2'] == node2:
            array[i]['cantidad'].append(cantidad)
            esta = True
            break
    if esta == False:
        array.append({'elemento1': node1, 'elemento2': node2, 'cantidad':[cantidad]})
    return array

def asignaNodoFaltas(equipo, listado):
    return listado[equipo]

def convertInArray(historical):
    array = []
    for element in historical:
        array.append(element)
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
