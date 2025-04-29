from pymongo import MongoClient
import numpy as np


client = MongoClient('localhost:27017')
db = client.all_leagues_bbdd
db2 = client.articulo3


def main():
    temporadas = ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    historical = convertInArray(getHistorical())
    array_faltas_total = []
    array_resultados = []

    data = []
    labels = []
    for temporada in temporadas:
        print(temporada)
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

                prediction = []
                # 3) Calculo la probabilidad
                if temporada in ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']:
                    prediction.append([node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam])
                    array_resultados.append({'temporada': temporada, 'HomeTeam': historical[i]['HomeTeam'], 'AwayTeam': historical[i]['AwayTeam'], 'faltas': int(historical[i]['HF']) + int(historical[i]['AF'])})
                    array_resultados[len(array_resultados)-1]['prob25'], array_resultados[len(array_resultados)-1]['prob30'], array_resultados[len(array_resultados)-1]['prob35'], array_resultados[len(array_resultados)-1]['prob40'] = calculaProbabilidad(np.array(data), np.array(labels), np.array(prediction))
                data.append([node1_HomeTeam, node1_AwayTeam, node2_HomeTeam, node2_AwayTeam])
                labels.append([clasifica(int(historical[i]['HF']) + int(historical[i]['AF']))])

                # 5) Actualizo el listado de faltas y puntos de cada equipo
                equipos_con_faltas_efectuadas[historical[i]['HomeTeam']] += int(historical[i]['HF'])
                equipos_con_faltas_efectuadas[historical[i]['AwayTeam']] += int(historical[i]['AF'])
                equipos_con_faltas_recibidas[historical[i]['HomeTeam']] += int(historical[i]['AF'])
                equipos_con_faltas_recibidas[historical[i]['AwayTeam']] += int(historical[i]['HF'])

                # 6) Guardo los partidos correspondientes a a las diez últimas temporadas
    print('meto resultados')
    if len(array_resultados) > 0:
        insertHistorical(array_resultados)
        array_resultados = []
    return array_resultados

def clasifica(num):
    if num <= 25:
        return 0
    if num <= 30:
        return 1
    if num <= 35:
        return 2
    return 3

def equilibrador(a, b, c, d):
    if a == 0 and b == 0 and c == 0 and d == 0:
        return 0, 0, 0, 0
    else:
        return a/(a+b+c+d), b/(a+b+c+d), c/(a+b+c+d), d/(a+b+c+d)

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
            return i

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

def calculaProbabilidad(data, labels, nuevos_datos):
    # Inicialización de pesos y sesgos
    input_size = 4
    hidden_size = 4
    output_size = 4

    weights_input_hidden = np.random.uniform(size=(input_size, hidden_size))
    bias_hidden = np.zeros((1, hidden_size))

    weights_hidden_output = np.random.uniform(size=(hidden_size, output_size))
    bias_output = np.zeros((1, output_size))

    # Entrenamiento
    learning_rate = 0.1
    epochs = 10000

    for epoch in range(epochs):
        # Capa oculta
        hidden_activation = sigmoid(np.dot(data, weights_input_hidden) + bias_hidden)

        # Capa de salida con softmax
        output_activation = softmax(np.dot(hidden_activation, weights_hidden_output) + bias_output)

        # Cálculo de error
        error = labels - output_activation

        # Entropía cruzada categórica
        loss = -np.sum(labels * np.log(output_activation + 1e-15)) / len(labels)

        # Backpropagation
        d_output = error  # No se necesita sigmoid_derivative aquí
        error_hidden = d_output.dot(weights_hidden_output.T)
        d_hidden = error_hidden * sigmoid_derivative(hidden_activation)

        # Actualización de pesos y sesgos
        weights_hidden_output += hidden_activation.T.dot(d_output) * learning_rate
        bias_output += np.sum(d_output, axis=0, keepdims=True) * learning_rate
        weights_input_hidden += data.T.dot(d_hidden) * learning_rate
        bias_hidden += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

    # ...

    # Predicciones finales
    final_hidden_activation = sigmoid(np.dot(data, weights_input_hidden) + bias_hidden)
    raw_output_activation = np.dot(final_hidden_activation, weights_hidden_output) + bias_output
    final_output_activation = softmax(raw_output_activation)

    predictions = np.argmax(final_output_activation, axis=1)

    # Capa oculta
    nuevas_hidden_activation = sigmoid(np.dot(nuevos_datos, weights_input_hidden) + bias_hidden)

    # Capa de salida con softmax
    nuevas_output_activation = softmax(np.dot(nuevas_hidden_activation, weights_hidden_output) + bias_output)

    # Probabilidades finales para cada clase
    probabilidades_finales = nuevas_output_activation
    print(probabilidades_finales)
    return probabilidades_finales[0][0], probabilidades_finales[0][1], probabilidades_finales[0][2], probabilidades_finales[0][3]


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def sigmoid_derivative(x):
    return x * (1 - x)

def insertHistorical(array):
    try:
        db2.articulo3_nn.insert_many(array)
        return ('Datos insertados satisfactoriamente')

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')


main()
