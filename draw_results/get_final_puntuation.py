from auxiliars._1_asociando_bondad_a_las_particiones import main as getAssociationWithProbabilities
from auxiliars._2_evaluando_error import main as getPuntuacion
from auxiliars._3_componentes_continuos import main as getPartidosVersionContinua
from auxiliars._4_TAN import main as getPartidosTAN
from auxiliars._5_red_neuronal import main as getPartidosRedNeuronal
from auxiliars._6_dixonycoles import main as getDixonColes

def main():
    # 1 Calculo mi clustering y lo puntuacion
    particionClusterNB = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18, 19]]
    puntuacionClusterNB = getPuntuacion(getAssociationWithProbabilities(particionClusterNB))
    # 2 Calculo el puntuacion con discretización kmeans
    particionKmeans = [[0, 1, 2, 3, 4], [5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]
    puntuacionKmeans = getPuntuacion(getAssociationWithProbabilities(particionKmeans))
    # 3 Calculo el puntuacion tomando todos los componentes como continuos
    puntuacionComponentesContinuos = getPuntuacion(getPartidosVersionContinua())

    puntuacionRedNeuronal = getPuntuacion(getPartidosRedNeuronal())

    puntuacionRedTAN = getPuntuacion(getPartidosTAN())

    puntuacionDixonColes = getPuntuacion(getDixonColes())

    particionClusterFayyad = [[0, 1, 2, 3], [4, 5, 6, 7], [ 8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]
    puntuacionClusterFayyad = getPuntuacion(getAssociationWithProbabilities(particionClusterFayyad))

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


def media(arr):
    return (arr[0]+arr[1])/2

main()
