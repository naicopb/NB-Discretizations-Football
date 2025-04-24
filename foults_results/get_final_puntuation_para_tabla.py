import numpy as np
from auxiliars._6_main_clustering_fayyad_para_tabla import main as getFayyad

from auxiliars.prueba_rps import main as getPuntuation

def main():
    temporadas = ['2021-2022', '2022-2023', '2023-2024']

    print(temporadas[-1])
    # 6 Calculo partidos con clustering Fayyad
    partidosFayyad = getFayyad(temporadas)
    dataToEvaluateTrue6, dataToEvaluatePredicted6 = prepareData(partidosFayyad, temporadas[-1])
    #print(dataToEvaluateTrue2)
    #print(dataToEvaluatePredicted2)
    puntuation6 = getPuntuation(dataToEvaluateTrue6, dataToEvaluatePredicted6)
    print("Fayyad - RPS:", puntuation6)




def prepareData(neoArray, temporada):
    array = []
    for i in range(0, len(neoArray)):
        if neoArray[i]['temporada'] == temporada:
            array.append(neoArray[i])
    print(len(array))
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
