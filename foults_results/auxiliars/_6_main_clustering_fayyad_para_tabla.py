from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.all_leagues_bbdd

def main(temporadas):
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
                #print(node1_HomeTeam)
                #print(node1_AwayTeam)
                node2_HomeTeam = asignaNodoFaltas(historical[i]['HomeTeam'], equipos_con_faltas_efectuadas)
                node2_AwayTeam = asignaNodoFaltas(historical[i]['AwayTeam'], equipos_con_faltas_recibidas)
                #print(node2_HomeTeam)
                #print(node2_AwayTeam)

                # 3) Calculo la probabilidad
                #25, 30, 35 mas
                if temporada in temporadas[-1]:
                    array_resultados.append({'temporada': temporada, 'HomeTeam': historical[i]['HomeTeam'], 'AwayTeam': historical[i]['AwayTeam'], 'faltas': int(historical[i]['HF']) + int(historical[i]['AF'])})
                    array_resultados[len(array_resultados)-1]['prob25'], array_resultados[len(array_resultados)-1]['prob30'], array_resultados[len(array_resultados)-1]['prob35'], array_resultados[len(array_resultados)-1]['prob40'] = equilibrador(calculaProbabilidad(0, 25, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total), calculaProbabilidad(25, 30, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total), calculaProbabilidad(30, 35, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total), calculaProbabilidad(35, 1000, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total))
                    #array_resultados[len(array_resultados)-1]['prob25'] = calculaProbabilidad(0, 25, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total)
                    #array_resultados[len(array_resultados)-1]['prob30'] = calculaProbabilidad(25, 30, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total)
                    #array_resultados[len(array_resultados)-1]['prob35'] = calculaProbabilidad(30, 35, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total)
                    #array_resultados[len(array_resultados)-1]['prob40'] = calculaProbabilidad(35, 1000, node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam, array_node_11, array_node_12, array_node_21, array_node_22 , array_faltas_total)
                    #print(array_resultados[len(array_resultados)-1]['prob25'])
                    #print(array_resultados[len(array_resultados)-1]['prob30'])
                    #print(array_resultados[len(array_resultados)-1]['prob35'])
                    #print(array_resultados[len(array_resultados)-1]['prob40'])
                    #print(array_resultados[len(array_resultados)-1]['prob25'] + array_resultados[len(array_resultados)-1]['prob30'] + array_resultados[len(array_resultados)-1]['prob35'] + array_resultados[len(array_resultados)-1]['prob40'])

                # 4) Actualizo el conteo de los nodos
                array_node_11 = actualizaNodes(array_node_1, node1_HomeTeam, int(historical[i]['HF']) + int(historical[i]['AF']))
                array_node_12 = actualizaNodes(array_node_2, node1_AwayTeam, int(historical[i]['HF']) + int(historical[i]['AF']))
                array_node_21 = actualizaNodes(array_node_2, node2_HomeTeam, int(historical[i]['HF']) + int(historical[i]['AF']))
                array_node_22 = actualizaNodes(array_node_2, node2_AwayTeam, int(historical[i]['HF']) + int(historical[i]['AF']))
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
     #  print(array_resultados[i])
    return array_resultados
        #break

def equilibrador(a, b, c, d):
    if a == 0 and b == 0 and c == 0 and d == 0:
        return 0, 0, 0, 0
    else:
        return a/(a+b+c+d), b/(a+b+c+d), c/(a+b+c+d), d/(a+b+c+d)

def calculaProbabilidad(extremoInferior, extremoSuperior, node1_home, node1_away, node2_home, node2_away, array_node_11, array_node_12, array_node_21, array_node_22, arrayTotal):
    node11Favor, node11Contra, node12Favor, node12Contra, node21Favor, node21Contra, node22Favor, node22Contra = -1, -1, -1, -1, -1, -1, -1, -1
    totalesFavor, totalesContra  = discriminaCantidades(arrayTotal, extremoInferior, extremoSuperior)
    for i in range(0, len(array_node_11)):
        if array_node_11[i]['elemento1'] == node1_home:
            node11Favor, node11Contra = discriminaCantidades(array_node_11[i]['cantidad'], extremoInferior, extremoSuperior)
    for i in range(0, len(array_node_11)):
        if array_node_12[i]['elemento1'] == node1_away:
            node12Favor, node12Contra = discriminaCantidades(array_node_12[i]['cantidad'], extremoInferior, extremoSuperior)
    for i in range(0, len(array_node_21)):
        if array_node_21[i]['elemento1'] == node2_home:
            node21Favor, node21Contra = discriminaCantidades(array_node_21[i]['cantidad'], extremoInferior, extremoSuperior)
    for i in range(0, len(array_node_22)):
        if array_node_22[i]['elemento1'] == node2_away:
            node22Favor, node22Contra = discriminaCantidades(array_node_22[i]['cantidad'], extremoInferior, extremoSuperior)
    #print('----------')
    #print(totalesFavor)
    #print(totalesContra)
    #print(node1Favor)
    #print(node1Contra)
    #print(node2Favor)
    #print(node2Contra)
    if totalesFavor == 0 or totalesContra == 0:
        return 0
    numerador = (totalesFavor/(totalesFavor+totalesContra))*(node11Favor/totalesFavor)*(node12Favor/totalesFavor)*(node21Favor/totalesFavor)*(node22Favor/totalesFavor)
    denominador1 = (totalesFavor/(totalesFavor+totalesContra))*(node11Favor/totalesFavor)*(node12Favor/totalesFavor)*(node21Favor/totalesFavor)*(node22Favor/totalesFavor)
    denominador2 = (totalesContra/(totalesFavor+totalesContra))*(node11Contra/totalesContra)*(node12Contra/totalesContra)*(node21Contra/totalesContra)*(node22Contra/totalesContra)
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

def actualizaNodes(array, node1, cantidad):
    esta = False
    for i in range(0, len(array)):
        if array[i]['elemento1'] == node1:
            array[i]['cantidad'].append(cantidad)
            esta = True
            break
    if esta == False:
        array.append({'elemento1': node1, 'cantidad':[cantidad]})
    return array

def asignaNodoFaltas(equipo, listado):
    arrayClasificacion = []
    for key in listado.keys():
        arrayClasificacion.append({'equipo': key, 'faltas': listado[key]})
    arrayClasificacion = sorted(arrayClasificacion, key=lambda x: (-x['faltas']))
    return asignaNodoPorPosicion(equipo, arrayClasificacion)

def asignaNodoPorPosicion(equipo, arrayClasificacion):
    for i in range(0, len(arrayClasificacion)):
        if arrayClasificacion[i]['equipo'] == equipo:
            return int(i/4)

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

#main()
