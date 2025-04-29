from auxiliars._1_asociando_bondad_a_las_particiones import main as getAssociationWithProbabilities
from auxiliars._2_evaluando_error import main as getPuntuacion
from auxiliars._3_componentes_continuos import main as getPartidosVersionContinua
from auxiliars._4_TAN import main as getPartidosTAN
from auxiliars._5_red_neuronal import main as getPartidosRedNeuronal
from auxiliars._6_dixonycoles import main as getDixonColes

def main():
    temporadas = ['2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    #temporadas = ['2014-2015', '2015-2016','2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']

    particionIgualMagnitud = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]

    # 1 Calculo mi clustering y lo puntuacion
    particionClusterNB = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18, 19]]
    puntuacionClusterNB = getPuntuacion(isInTemporadas(getAssociationWithProbabilities(particionClusterNB), temporadas))

    # 2 Calculo el puntuacion con discretización kmeans
    particionKmeans = [[0, 1, 2, 3, 4], [5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]
    puntuacionKmeans = getPuntuacion(isInTemporadas(getAssociationWithProbabilities(particionKmeans), temporadas))

    # 3 Calculo el puntuacion tomando todos los componentes como continuos
    puntuacionComponentesContinuos = getPuntuacion(isInTemporadas(getPartidosVersionContinua(particionIgualMagnitud), temporadas))

    puntuacionRedNeuronal = getPuntuacion(isInTemporadas(getPartidosRedNeuronal(), temporadas))

    puntuacionRedTAN = getPuntuacion(isInTemporadas(getPartidosTAN(), temporadas))

    puntuacionDixonColes = getPuntuacion(isInTemporadas(getDixonColes(), temporadas))

    particionClusterFayyad = [[0, 1, 2, 3], [4, 5, 6, 7], [ 8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]
    puntuacionClusterFayyad = getPuntuacion(isInTemporadas(getAssociationWithProbabilities(particionClusterFayyad), temporadas))

    print('1.1. puntuacion del modelo con discretización naive-bayes')
    print(puntuacionClusterNB)
    print(media(puntuacionClusterNB))
    print('1.2. puntuacion del modelo con discretización kmeans')
    print(puntuacionKmeans)
    print(media(puntuacionKmeans))
    print('1.3. puntuacion del modelo con componentes continuos')
    print(puntuacionComponentesContinuos)
    print(media(puntuacionComponentesContinuos))
    print('#########')
    print('2.1. puntuacion del modelo con discretización naive-bayes')
    print(puntuacionClusterNB)
    print(media(puntuacionClusterNB))
    print('2.2. puntuacion del modelo de redes neuronales')
    print(puntuacionRedNeuronal)
    print(media(puntuacionRedNeuronal))
    print('2.3. puntuacion del modelo con red TAN')
    print(puntuacionRedTAN)
    print(media(puntuacionRedTAN))
    print('#########')
    print('3.1. puntuacion del modelo con discretización naive-bayes')
    print(puntuacionClusterNB)
    print(media(puntuacionClusterNB))
    print('3.2. puntuacion del modelo dixon y coles')
    print(puntuacionDixonColes)
    print(media(puntuacionDixonColes))
    print('3.3. puntuacion del modelo Fayyad')
    print(puntuacionClusterFayyad)
    print(media(puntuacionClusterFayyad))

def isInTemporadas(arrayPartidos, temporadas):
    neoArray = []
    for temporada in temporadas:
        for i in range(0, len(arrayPartidos)):
            if arrayPartidos[i]['temporada'] == temporada:
                neoArray.append(arrayPartidos[i])
    return neoArray


def media(arr):
    return (arr[0]+arr[1])/2

main()
