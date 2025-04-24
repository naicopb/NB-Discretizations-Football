import math
from pymongo import MongoClient
from auxiliars.moftbs.w_moftbs_node1_home_continous import main as getNode1_HomeTeam
from auxiliars.moftbs.w_moftbs_node1_away_continous import main as getNode1_AwayTeam
from auxiliars.moftbs.w_moftbs_node2_home_continous import main as getNode2_HomeTeam
from auxiliars.moftbs.w_moftbs_node2_away_continous import main as getNode2_AwayTeam

client = MongoClient('localhost:27017')
db = client.all_leagues_bbdd

def main():
    temporadas = ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    historical = convertInArray(getHistorical())
    #print(historical[0])

    superArray_node1_HomeTeam = getNode1_HomeTeam()
    superArray_node1_AwayTeam = getNode1_AwayTeam()
    superArray_node2_HomeTeam = getNode2_HomeTeam()
    superArray_node2_AwayTeam = getNode2_AwayTeam()


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
                array_resultados.append({'temporada': temporada, 'HomeTeam': historical[i]['HomeTeam'], 'AwayTeam': historical[i]['AwayTeam'], 'node1_HomeTeam': node1_HomeTeam, 'node1_AwayTeam': node1_AwayTeam, 'node2_HomeTeam':node2_HomeTeam, 'node2_AwayTeam':node2_AwayTeam, 'faltas': int(historical[i]['HF']) + int(historical[i]['AF'])})
                array_resultados[len(array_resultados)-1]['prob25'] = calculaProbabilidad(0, superArray_node1_HomeTeam[i], superArray_node1_AwayTeam[i], superArray_node2_HomeTeam[i], superArray_node2_AwayTeam[i], array_faltas_total, 0, 25)
                array_resultados[len(array_resultados)-1]['prob30'] = calculaProbabilidad(1, superArray_node1_HomeTeam[i], superArray_node1_AwayTeam[i], superArray_node2_HomeTeam[i], superArray_node2_AwayTeam[i], array_faltas_total, 25, 30)
                array_resultados[len(array_resultados)-1]['prob35'] = calculaProbabilidad(2, superArray_node1_HomeTeam[i], superArray_node1_AwayTeam[i], superArray_node2_HomeTeam[i], superArray_node2_AwayTeam[i], array_faltas_total, 30, 35)
                array_resultados[len(array_resultados)-1]['prob40'] = calculaProbabilidad(3, superArray_node1_HomeTeam[i], superArray_node1_AwayTeam[i], superArray_node2_HomeTeam[i], superArray_node2_AwayTeam[i], array_faltas_total, 35, 100)
                # Ahora ajusto
                array_resultados[len(array_resultados)-1]['prob25'], array_resultados[len(array_resultados)-1]['prob30'], array_resultados[len(array_resultados)-1]['prob35'], array_resultados[len(array_resultados)-1]['prob40'] = equilibrador_2(array_resultados[len(array_resultados)-1]['prob25'], array_resultados[len(array_resultados)-1]['prob30'], array_resultados[len(array_resultados)-1]['prob35'], array_resultados[len(array_resultados)-1]['prob40'])

                # 4) Actualizo el conteo de los nodos
                array_node_1 = actualizaNodes(array_node_1, node1_HomeTeam, node1_AwayTeam, int(historical[i]['HF']) + int(historical[i]['AF']))
                array_node_2 = actualizaNodes(array_node_2, node2_HomeTeam, node2_AwayTeam, int(historical[i]['HF']) + int(historical[i]['AF']))
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
    neoArrayResultados = []
    for i in range(0, len(array_resultados)):
        if array_resultados[i]['temporada'] not in ['2010-2011', '2011-2012']:
            neoArrayResultados.append(array_resultados[i])
        #if temporada == '2010-2011' or temporada == '2011-2012':
        #    print(temporada)
        #    print(devuelveClasParaKmeans(equipos_con_faltas_recibidas))
    #print(array_resultados)
    return neoArrayResultados

def probContinua_1_h(x):
    return [formula_1_h(0), formula_1_h(1), formula_1_h(2), formula_1_h(3)]

def formula_1_h(x):
    return 0.0654943221956917-0.0193429735758948*x+0.00397178828564835*math.pow(x, 2)-0.00028358560854042*math.pow(x, 3)+6.8766892619382e-06*math.pow(x, 4)

def probContinua_1_a(x):
    return [formula_1_a(0), formula_1_a(1), formula_1_a(2), formula_1_a(3)]

def formula_1_a(x):
    return 0.0613741807573562-0.0145178551327098*x+0.00302762826239106*math.pow(x, 2)-0.000219871549120026*math.pow(x, 3)+5.44337289832785e-06*math.pow(x, 4)

def probContinua_2_h(x):
    return [formula_2_h(0), formula_2_h(1), formula_2_h(2), formula_2_h(3)]

def formula_2_h(x):
    if x == 0 or x ==1:
        return 0.0357925257797423+0.0017725319123817*x
    else:
        return 0.0857924110508051-0.0242621343864778*x+0.00435949443892887*math.pow(x, 2)-0.000289675618545662*math.pow(x, 3)+6.5015697387541e-06*math.pow(x,4)

def probContinua_2_a(x):
    return [formula_2_a(0), formula_2_a(1), formula_2_a(2), formula_2_a(3)]

def formula_2_a(x):
    if x == 0 or x ==1:
        return 0.0868572754416132-0.0971641911643584*x+0.0644407891261536*math.pow(x, 2)-0.0209009871647753*math.pow(x, 3)+0.00373023015569814*math.pow(x, 4)-0.000382228034835604*math.pow(x, 5)+2.24059544179193e-05*math.pow(x, 6)-6.98590994686866e-07*math.pow(x, 7)+8.98621156449877e-09*math.pow(x, 8)
    else:
        return 0.065694739417699-0.0153668753417581*x+0.00311959666663275*math.pow(x, 2)-0.000226957382062124*math.pow(x, 3)+5.628634702616e-06*math.pow(x, 4)

def equilibrador(arr):
    a = arr[0]
    b = arr[1]
    c = arr[2]
    d = arr[3]
    if a == 0 and b == 0 and c == 0 and d == 0:
        return 0, 0, 0, 0
    else:
        return [a/(a+b+c+d), b/(a+b+c+d), c/(a+b+c+d), d/(a+b+c+d)]

def equilibrador_2(a, b, c, d):
    if a == 0 and b == 0 and c == 0 and d == 0:
        return 0, 0, 0, 0
    else:
        return a/(a+b+c+d), b/(a+b+c+d), c/(a+b+c+d), d/(a+b+c+d)

def calculaProbabilidad(num, array_a, array_b, array_c, array_d, arrayTotal, extremoInferior, extremoSuperior):
    if len(arrayTotal) == 0:
        return 0.25
    totalesFavor, totalesContra  = discriminaCantidades(arrayTotal, extremoInferior, extremoSuperior)
    prob_a_favor = array_a[num]
    prob_a_contra = probContra(num, array_a)
    prob_b_favor = array_b[num]
    prob_b_contra = probContra(num, array_b)
    prob_c_favor = array_c[num]
    prob_c_contra = probContra(num, array_c)
    prob_d_favor = array_d[num]
    prob_d_contra = probContra(num, array_d)
    numerador = totalesFavor/(totalesFavor+totalesContra)*prob_a_favor*prob_b_favor*prob_c_favor*prob_d_favor
    denominador1 = totalesFavor/(totalesFavor+totalesContra)*prob_a_favor*prob_b_favor*prob_c_favor*prob_d_favor
    denominador2 = totalesContra/(totalesFavor+totalesContra)*prob_a_contra*prob_b_contra*prob_c_contra*prob_d_contra
    return numerador/(denominador1+denominador2)

def probContra(num, array):
    sum = 0
    for i in range(0, len(array)):
        if i != num:
            sum += array[i]
    return sum

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
    for i in range(0, len(arrayClasificacion)):
        if arrayClasificacion[i]['equipo'] == equipo:
            return int(i)

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

main()
