import numpy as np
from sklearn.cluster import KMeans

def main(num_clusters):
    array = [{'position': 1, 'porcentaje': 0.8009009009009009}, {'position': 2, 'porcentaje': 0.7563063063063062}, {'position': 3, 'porcentaje': 0.6743243243243244}, {'position': 4, 'porcentaje': 0.5666666666666667}, {'position': 5, 'porcentaje': 0.5216216216216216}, {'position': 6, 'porcentaje': 0.5099099099099098}, {'position': 7, 'porcentaje': 0.4806306306306306}, {'position': 8, 'porcentaje': 0.45855855855855865}, {'position': 9, 'porcentaje': 0.4398398398398399}, {'position': 10, 'porcentaje': 0.4247247247247247}, {'position': 11, 'porcentaje': 0.4204704704704705}, {'position': 12, 'porcentaje': 0.40875875875875883}, {'position': 13, 'porcentaje': 0.3972472472472473}, {'position': 14, 'porcentaje': 0.3834334334334334}, {'position': 15, 'porcentaje': 0.3711711711711711}, {'position': 16, 'porcentaje': 0.3626126126126126}, {'position': 17, 'porcentaje': 0.3517517517517518}, {'position': 18, 'porcentaje': 0.34609609609609604}, {'position': 19, 'porcentaje': 0.3422922922922923}, {'position': 20, 'porcentaje': 0.32497497497497496}]

    array_kmeans = getArrayKmeans(array, num_clusters)
    print(array_kmeans)
    #print(len(array_kmeans))

    array_clusterbayesiano = getArrayBayesiano(array, num_clusters)


def getArrayBayesiano(array, num_clusters):
    return array

def getArrayKmeans(array, num_clusters):
    #creo el clustering para la clasificación histórica
    X_historica = []
    y_historica = []
    for i in range(0, len(array)):
        X_historica.append([array[i]['position']])
        y_historica.append(array[i]['porcentaje'])

    #continuo con la creación del clustering historico
    X_historica = np.array(X_historica)
    kmeans_historico = KMeans(n_clusters=num_clusters,init='k-means++', n_init = 10 ,max_iter=300, tol=0.0001,  random_state= 111  , algorithm='elkan').fit(X_historica)

    categorias_historicas = []
    categorias_historicas.append(kmeans_historico.predict(X_historica))

    return reconvertirArray(categorias_historicas[0])

def reconvertirArray(array):
    neoArray = []
    actualCaracter = array[0]
    counter = 1
    for i in range(0, len(array)):
        if array[i] == actualCaracter:
            counter += 1
            if i == len(array)-1:
                neoArray = addElements(neoArray, counter)
        else:
            neoArray = addElements(neoArray, counter)
            actualCaracter = array[i]
            counter = 1
    return neoArray

def addElements(array, num):
    if len(array) == 0:
        for i in range(0, num-1):
            array.append(1)
    else:
        neoNumber = array[-1] + 1
        for i in range(0, num):
            array.append(neoNumber)
    return array

main(5)
