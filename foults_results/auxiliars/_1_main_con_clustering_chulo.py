from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.all_leagues_bbdd

def main():
    temporadas = ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    historical = convertInArray(getHistorical())
    #print(historical[0])
    array_node_1 = []
    array_node_2 = []
    array_faltas_total = []
    array_resultados = []
    #
    arrayMUYAUXILIARCONFALTAS = []
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
                node2_HomeTeam = asignaNodoFaltas(historical[i]['HomeTeam'], equipos_con_faltas_efectuadas)
                node2_AwayTeam = asignaNodoFaltas(historical[i]['AwayTeam'], equipos_con_faltas_recibidas)

                # 3) Calculo la probabilidad
                #25, 30, 35 mas
                if temporada in ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']:
                    array_resultados.append({'temporada': temporada, 'HomeTeam': historical[i]['HomeTeam'], 'AwayTeam': historical[i]['AwayTeam'], 'faltas': int(historical[i]['HF']) + int(historical[i]['AF'])})
                    array_resultados[len(array_resultados)-1]['prob25'], array_resultados[len(array_resultados)-1]['prob30'], array_resultados[len(array_resultados)-1]['prob35'], array_resultados[len(array_resultados)-1]['prob40'] = equilibrador(calculaProbabilidad(0, 25, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total), calculaProbabilidad(25, 30, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total), calculaProbabilidad(30, 35, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total), calculaProbabilidad(35, 1000, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total))
                    #array_resultados[len(array_resultados)-1]['prob25'] = calculaProbabilidad(0, 25, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total)
                    #array_resultados[len(array_resultados)-1]['prob30'] = calculaProbabilidad(25, 30, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total)
                    #array_resultados[len(array_resultados)-1]['prob35'] = calculaProbabilidad(30, 35, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total)
                    #array_resultados[len(array_resultados)-1]['prob40'] = calculaProbabilidad(35, 1000, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_1, array_node_2, array_faltas_total)
                    #print(array_resultados[len(array_resultados)-1]['prob25'])
                    #print(array_resultados[len(array_resultados)-1]['prob30'])
                    #print(array_resultados[len(array_resultados)-1]['prob35'])
                    #print(array_resultados[len(array_resultados)-1]['prob40'])

                # 4) Actualizo el conteo de los nodos
                array_node_1 = actualizaNodes(array_node_1, node1_HomeTeam[0], node1_AwayTeam[0], int(historical[i]['HF']) + int(historical[i]['AF']))
                array_node_2 = actualizaNodes(array_node_2, node2_HomeTeam[0], node2_AwayTeam[0], int(historical[i]['HF']) + int(historical[i]['AF']))
                array_faltas_total.append(int(historical[i]['HF']) + int(historical[i]['AF']))
                #print(array_node_1)
                #print(array_node_2)
                #arrayMUYAUXILIARCONFALTAS.append(int(historical[i]['HF']) + int(historical[i]['AF']))
                #arrayMUYAUXILIARCONFALTAS.sort()
                #print(arrayMUYAUXILIARCONFALTAS)

                # 5) Actualizo el listado de faltas y puntos de cada equipo
                equipos_con_faltas_efectuadas[historical[i]['HomeTeam']] += int(historical[i]['HF'])
                equipos_con_faltas_efectuadas[historical[i]['AwayTeam']] += int(historical[i]['AF'])
                equipos_con_faltas_recibidas[historical[i]['HomeTeam']] += int(historical[i]['AF'])
                equipos_con_faltas_recibidas[historical[i]['AwayTeam']] += int(historical[i]['HF'])

                # 6) Guardo los partidos correspondientes a a las diez últimas temporadas

    #for i in range(0, len(array_resultados)):
    #    print(array_resultados[i])
    return array_resultados
        #break

def equilibrador(a, b, c, d):
    if a == 0 and b == 0 and c == 0 and d == 0:
        return 0, 0, 0, 0
    else:
        return a/(a+b+c+d), b/(a+b+c+d), c/(a+b+c+d), d/(a+b+c+d)

def calculaProbabilidad(extremoInferior, extremoSuperior, node1_home, node1_away, node2_home, node2_away, array_node_1, array_node_2, arrayTotal):
    node1Favor, node1Contra, node2Favor, node2Contra = -1, -1, -1, -1
    totalesFavor, totalesContra  = discriminaCantidades(arrayTotal, extremoInferior, extremoSuperior)
    for i in range(0, len(array_node_1)):
        if array_node_1[i]['elemento1'] == node1_home[1] and array_node_1[i]['elemento2'] == node1_away[1]:
            aux1_node1Favor, aux1_node1Contra = discriminaCantidades(array_node_1[i]['cantidad'], extremoInferior, extremoSuperior)
        if array_node_1[i]['elemento1'] == node1_home[3] and array_node_1[i]['elemento2'] == node1_away[3]:
            aux2_node1Favor, aux2_node1Contra = discriminaCantidades(array_node_1[i]['cantidad'], extremoInferior, extremoSuperior)
    node1Favor, node1Contra = aux1_node1Favor*node1_home[2] + aux2_node1Favor*node1_home[4], aux1_node1Contra*node1_away[2] + aux2_node1Contra*node1_away[4]
    for i in range(0, len(array_node_2)):
        if array_node_2[i]['elemento1'] == node2_home[1] and array_node_2[i]['elemento2'] == node2_away[1]:
            aux1_node2Favor, aux1_node2Contra = discriminaCantidades(array_node_2[i]['cantidad'], extremoInferior, extremoSuperior)
        if array_node_2[i]['elemento1'] == node2_home[3] and array_node_2[i]['elemento2'] == node2_away[3]:
            aux2_node2Favor, aux2_node2Contra = discriminaCantidades(array_node_2[i]['cantidad'], extremoInferior, extremoSuperior)
    node2Favor, node2Contra = aux1_node2Favor*node2_home[2] + aux2_node2Favor*node2_home[4], aux1_node2Contra*node2_away[2] + aux2_node2Contra*node2_away[4]

    #print('----------')
    #print(totalesFavor)
    #print(totalesContra)
    #print(node1Favor)
    #print(node1Contra)
    #print(node2Favor)
    #print(node2Contra)
    if totalesFavor == 0 or totalesContra == 0:
        return 0
    numerador = (totalesFavor/(totalesFavor+totalesContra))*(node1Favor/totalesFavor)*(node2Favor/totalesFavor)
    denominador1 = (totalesFavor/(totalesFavor+totalesContra))*(node1Favor/totalesFavor)*(node2Favor/totalesFavor)
    denominador2 = (totalesContra/(totalesFavor+totalesContra))*(node1Contra/totalesContra)*(node2Contra/totalesContra)
    if denominador1 + denominador2 == 0:
        return 0
    return numerador/(denominador1+denominador2)

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
    arrayClasificacion = []
    for key in listado.keys():
        arrayClasificacion.append({'equipo': key, 'faltas': listado[key]})
    arrayClasificacion = sorted(arrayClasificacion, key=lambda x: (-x['faltas']))
    return asignaNodoPorPosicion(equipo, arrayClasificacion)

def asignaNodoPorPosicion(equipo, arrayClasificacion):
    realValue = 0
    centroides = []
    for i in range(0, len(arrayClasificacion)):
        if arrayClasificacion[i]['equipo'] == equipo:
            faltas = arrayClasificacion[i]['faltas']
            realValue = int(i/4)
    if len(arrayClasificacion) < 20:
        return [realValue, 0, 1, 1, 0]

    for i in range(0, 5):
        centr = 0
        for j in range(4*i + 0, 4*i + 4):
            centr = centr + arrayClasificacion[j]['faltas']
        centroides.append(centr/4)
    if faltas > centroides[0]:
        return [realValue, 0, 1, 1, 0]
    if faltas < centroides[4]:
        return [realValue, 3, 0, 4, 1]

    for i in range(0, len(centroides)-1):
        if faltas <= centroides[i] and faltas >= centroides[i+1]:
            return [realValue, i, (centroides[i] - faltas)/(centroides[i] - centroides[i+1]), i+1, (faltas -centroides[i+1])/(centroides[i] - centroides[i+1])]
    return [realValue, 0, 1, 1, 0]

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
