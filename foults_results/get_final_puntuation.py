import numpy as np
from auxiliars._1_main_con_clustering_chulo import main as getNBConClustering
from auxiliars._2_main_componentes_continuos import main as getNBComponentesContinuos
from auxiliars._3_main_con_clustering_kmeans import main as getNBConKmeans
from auxiliars._4_main_nn_saca_resultados import main as getNN
from auxiliars._5_main_componentes_moftbs import main as getMOFTBS
from auxiliars._6_main_clustering_fayyad import main as getFayyad

from auxiliars.prueba_rps import main as getPuntuation

def main():

    # 1 Calculo partidos con clustering
    partidosNBConCluster = getNBConClustering()
    dataToEvaluateTrue1, dataToEvaluatePredicted1 = prepareData(partidosNBConCluster)
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation1 = getPuntuation(dataToEvaluateTrue1, dataToEvaluatePredicted1)
    print("Proposed Model - RPS:", puntuation1)

    # 2 Calculo partidos con componentes continuos
    partidosComponentesContinuos = getNBComponentesContinuos()
    dataToEvaluateTrue2, dataToEvaluatePredicted2 = prepareData(partidosComponentesContinuos)
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation2 = getPuntuation(dataToEvaluateTrue2, dataToEvaluatePredicted2)
    print("Componentes continuos - RPS:", puntuation2)

    # 3 Calculo partidos con clustering kmeans
    partidosKmeans = getNBConKmeans()
    dataToEvaluateTrue3, dataToEvaluatePredicted3 = prepareData(partidosKmeans)
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation3 = getPuntuation(dataToEvaluateTrue3, dataToEvaluatePredicted3)
    print("K-means - RPS:", puntuation3)


    # 4 Calculo partidos con componentes continuos
    partidosNN = getNN()
    dataToEvaluateTrue4, dataToEvaluatePredicted4 = prepareData(partidosNN)
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation4 = getPuntuation(dataToEvaluateTrue4, dataToEvaluatePredicted4)
    print("Neuronal Network - RPS:", puntuation4)

    # 5 Calculo partidos con clustering kmeans
    partidosMOFTBS = getMOFTBS()
    dataToEvaluateTrue5, dataToEvaluatePredicted5 = prepareData(partidosMOFTBS)
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation5 = getPuntuation(dataToEvaluateTrue5, dataToEvaluatePredicted5)
    print("MoTBFs - RPS:", puntuation5)

    # 6 Calculo partidos con clustering Fayyad
    partidosFayyad = getFayyad()
    dataToEvaluateTrue6, dataToEvaluatePredicted6 = prepareData(partidosFayyad)
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation6 = getPuntuation(dataToEvaluateTrue6, dataToEvaluatePredicted6)
    print("Fayyad - RPS:", puntuation6)




def prepareData(array):
    extremos = [[0, 25], [25, 30], [30, 35], [35, 100]]
    true_labels = []
    predicted_probs = []
    for i in range(0, len(array)):
        for j in range(0, len(extremos)):
            if array[i]['faltas'] > extremos[j][0] and array[i]['faltas'] < extremos[j][1]:
                true_labels.append(j)
                predicted_probs.append([array[i]['prob25'], array[i]['prob30'], array[i]['prob35'], array[i]['prob40']])
    return np.array(true_labels), np.array(predicted_probs)

main()
