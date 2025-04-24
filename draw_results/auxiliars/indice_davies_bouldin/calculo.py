import statistics
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans


def main(num_clusters):
    arrayInicial = [{'position': 1, 'puntos': 0.6922398589065256}, {'position': 2, 'puntos': 0.6954624781849913}, {'position': 3, 'puntos': 0.6230058774139379}, {'position': 4, 'puntos': 0.5431111111111111}, {'position': 5, 'puntos': 0.547486033519553}, {'position': 6, 'puntos': 0.46462063086104005}, {'position': 7, 'puntos': 0.44727891156462585}, {'position': 8, 'puntos': 0.4588859416445623}, {'position': 9, 'puntos': 0.37551695616211744}, {'position': 10, 'puntos': 0.4327485380116959}, {'position': 11, 'puntos': 0.4530386740331492}, {'position': 12, 'puntos': 0.3923076923076923}, {'position': 13, 'puntos': 0.386952636282395}, {'position': 14, 'puntos': 0.3855855855855856}, {'position': 15, 'puntos': 0.4270833333333333}, {'position': 16, 'puntos': 0.3524904214559387}, {'position': 17, 'puntos': 0.40607734806629836}, {'position': 18, 'puntos': 0.37626262626262624}, {'position': 19, 'puntos': 0.3664185277088503}, {'position': 20, 'puntos': 0.33163265306122447}]

    array = [[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]]
    arrayPosibilidades = devolvedorTodasLasPosibilidades(array, num_clusters)
    neoArray = []
    for i in range(0, len(arrayPosibilidades)):
        neoArray.append(arrayPosibilidades[i])
    X = getX(arrayInicial)
    neoArray = getLabels(neoArray)
    array_db = []
    for i in range(0, len(neoArray)):
        array_db.append(davies_bouldin_score(X, neoArray[i]))

    minimum = 10
    index = 0
    otro =[]
    for i in range(0, len(array_db)):
        if array_db[i] < minimum:
            minimum = array_db[i]
            index = i
        if array_db[i] == 0.18578383897386633:
            otro.append(array[i])
    print(array_db)
    print(minimum)
    print(neoArray[i])
    print(otro)

    #print(neoArray[:100])
    #print(neoArray[77])
    """
    print(X)
    kmeans = KMeans(n_clusters=3, random_state=30)
    labels = kmeans.fit_predict(X)
    print(labels)
    db_index = davies_bouldin_score(X, labels)
    print(db_index)
    """


def getX(array):
    neoArray = []
    for i in range(0, len(array)):
        neoArray.append([array[i]['puntos']])
    return neoArray

def getLabels(array):
    neoArray = []
    for i in range(0, len(array)):
        neoSubArray = []
        for j in range(0, len(array[i])):
            for k in range(0, len(array[i][j])):
                neoSubArray.append(j)
        neoArray.append(neoSubArray)
    return neoArray
"""
def diferenciaEntreAmplitudes(array, minInicial):
    min = minInicial
    max = 0
    for i in range(0, len(array)):
        if len(array[i]) < min:
            min = len(array[i])
        if len(array[i]) > max:
            max = len(array[i])
    return max-min

def distanciaEntreCentroides(array):
    neoArray = []
    for i in range(0, len(array)-1):
        neoArray.append(abs(array[i]-array[i+1]))
    return  min(neoArray)



def devuelveElMaximoDe(arrayDeObjetos, cosa):
    elemento = arrayDeObjetos[0]
    maximo = arrayDeObjetos[0][cosa]
    for i in range(0, len(arrayDeObjetos)):
        if arrayDeObjetos[i][cosa] > maximo:
            maximo = arrayDeObjetos[i][cosa]
            elemento = arrayDeObjetos[i]
    return elemento

def devuelveElMinimoDe(arrayDeObjetos, cosa):
    elemento = arrayDeObjetos[0]
    minimo = arrayDeObjetos[0][cosa]
    for i in range(0, len(arrayDeObjetos)):
        if arrayDeObjetos[i][cosa] < minimo:
            minimo = arrayDeObjetos[i][cosa]
            elemento = arrayDeObjetos[i]
    return elemento


def calculaVarianza(array):
    if len(array) == 1:
        return 0
    return statistics.variance(array)

def calculaDiferencias(centros):
    arrayDeDiferencias = []
    if len(centros) == 1:
        return [0]
    for i in range(0, len(centros) - 1):
        arrayDeDiferencias.append(abs(centros[i] - centros[i+1]))
    return arrayDeDiferencias

def calculaVarianzasDeSubconjuntos(particion, arrayInicial):
    varianzas = []
    for i in range(0, len(particion)):
        subArray = []
        for j in range(0, len(particion[i])):
            subArray.append(arrayInicial[particion[i][j]]['puntos'])
        if len(subArray) == 1:
            varianzas.append(0)
        else:
            varianzas.append(statistics.variance(subArray))
    return varianzas

def calculaCentroides(particion, arrayInicial):
    centroides = []
    for i in range(0, len(particion)):
        suma = 0
        for j in range(0, len(particion[i])):
            suma += arrayInicial[particion[i][j]]['puntos']
        centroides.append(suma/len(particion[i]))
    return centroides

"""
def devolvedorTodasLasPosibilidades(array, num_clusters):
    definitiveArray = []
    nuevasParticiones = array
    for i in range(0, 100000):
        particiones = particionaArray(nuevasParticiones)
        nuevasParticiones = []
        for i in range(0, len(particiones)):
            if len(particiones[i]) < 6 and particiones[i] not in array:
                array.append(particiones[i])
                nuevasParticiones.append(particiones[i])
            if len(particiones[i]) == 5:
                definitiveArray.append(particiones[i])
    return definitiveArray

def particionaArray(array):
    neoNeoArray = []
    for i in range(0, len(array)):
        for j in range(0, len(array[i])):
            arrayBaseInicial = []
            arrayBaseFinal = []
            for k in range(0, j):
                arrayBaseInicial.append(array[i][k])
            for k in range(j+1, len(array[i])):
                arrayBaseFinal.append(array[i][k])
            for elemento in particionaElemento(array[i][j]):
                neoArray = []
                for elementoInicial in arrayBaseInicial:
                    neoArray.append(elementoInicial)
                for subElemento in elemento:
                    neoArray.append(subElemento)
                for elementoFinal in arrayBaseFinal:
                    neoArray.append(elementoFinal)
                neoNeoArray.append(neoArray)
    return neoNeoArray


def particionaElemento(array):
    neoNeoArray = []
    for j in range(1, len(array)):
        neoArray = []
        array1 = []
        array2 = []
        for k in range(0, j):
            array1.append(array[k])
        for k in range(j, len(array)):
            array2.append(array[k])
        if array1 != []:
            neoArray.append(array1)
        if array2 != []:
            neoArray.append(array2)
        neoNeoArray.append(neoArray)
    return neoNeoArray

main(5)
