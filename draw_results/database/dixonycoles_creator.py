import sys
from pymongo import MongoClient
import penaltyblog as pb
from datetime import datetime

client = MongoClient('localhost:27017')
db = client.primera_y_segunda
db2 = client.datos_finales_paper


def main():
    liga = 'primera_division'
    historical = convertInArray(getHistorical('primera_division'))
    arrayRespuesta = []
    neoArray = []
    for temporada in ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']:
        neoArray = crearArrayConClasificaciones(getElementsDeTemporada(historical, temporada))
        fb = pb.scrapers.FootballData('ESP La Liga', temporada)
        df = fb.get_fixtures()

        goals_home = convertInArray(df["goals_home"])
        goals_away = convertInArray(df["goals_away"])
        team_home = convertInArray(df["team_home"])
        team_away = convertInArray(df["team_away"])

        for jornada in range(1, 39):
            if jornada == 1:
                partialGoalsHome = getPartialElements(jornada, goals_home)
                partialGoalsAway = getPartialElements(jornada, goals_away)
                partialTeamHome = getPartialElements(jornada, team_home)
                partialTeamAway = getPartialElements(jornada, team_away)
            else:
                partialGoalsHome = getPartialElements(jornada-1, goals_home)
                partialGoalsAway = getPartialElements(jornada-1, goals_away)
                partialTeamHome = getPartialElements(jornada-1, team_home)
                partialTeamAway = getPartialElements(jornada-1, team_away)
            clf = pb.models.DixonColesGoalModel(
            partialGoalsHome, partialGoalsAway, partialTeamHome, partialTeamAway
            )
            clf.fit()
            for i in range((jornada-1)*10, jornada*10):
                #print('H - ' + neoArray[i]['homeTeam'])
                #print('A - ' + neoArray[i]['awayTeam'])
                if excepciones(temporada, neoArray[i]['homeTeam'], neoArray[i]['awayTeam']):
                    neoArray[i]['probabilidad_total_empate'] = 0
                else:
                    neoArray[i]['probabilidad_total_empate'] = clf.predict(neoArray[i]['homeTeam'], neoArray[i]['awayTeam']).draw
                arrayRespuesta.append(neoArray[i])
            print(str(jornada) + ' de la temporada ' + str(temporada))
        print(len(arrayRespuesta))
    insertData(arrayRespuesta)

    """
    print(goals_home)

    clf = pb.models.DixonColesGoalModel(
    goals_home, goals_away, team_home, team_away
    )
    clf.fit()
    for i in range(0, len(neoArray)):
        neoArray[i]['probabilidad_total_empate'] = clf.predict(neoArray[i]['homeTeam'], neoArray[i]['awayTeam']).draw
        arrayRespuesta.append(neoArray[i])
    """
    #break
    return arrayRespuesta

def excepciones(temporada, home, away):
    excepcionesArray = [
        ['2020-2021','Sevilla','Alaves'],
        ['2020-2021','Eibar','Barcelona'],
        ['2020-2021', 'Elche', 'Ath Bilbao'],
        ['2020-2021', 'Real Madrid', 'Villarreal'],
        ['2020-2021', 'Valladolid', 'Ath Madrid'],
        ['2020-2021', 'Ath Bilbao', 'Real Madrid'],
        ['2020-2021', 'Ath Madrid', 'Osasuna'],
        ['2020-2021', 'Barcelona', 'Celta'],
        ['2020-2021', 'Cadiz', 'Elche'],
        ['2020-2021', 'Villarreal', 'Sevilla'],
        ['2020-2021', 'Sevilla', 'Valencia']
    ]
    for i in range(0, len(excepcionesArray)):
        if temporada == excepcionesArray[i][0] and home == excepcionesArray[i][1] and away == excepcionesArray[i][2]:
            return True
    return False

def getPartialElements(jornada, array):
    neoArray = []
    for i in range(0, jornada*10):
        neoArray.append(array[i])
    return neoArray

def convertInArray(historical):
    array = []
    for element in historical:
        array.append(element)
    return array

### Funciones para el manejo de base de datos
def getHistorical(liga):
    try:
        query = {}
        query['liga'] = liga
        resultado = db.datos_completos.find(query)
        return resultado

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')

### Funciones para el manejo de base de datos
def getHistorical(liga):
    try:
        query = {}
        query['liga'] = liga
        resultado = db.datos_completos.find(query)
        return resultado

    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')

### Funciones que permiten crear los elementos básicos del array

def getElementsDeTemporada(historical, temporada):
    array = []
    for element in historical:
        if element['temporada'] == temporada:
            array.append(element)
    return array


def crearArrayConClasificaciones(historical):
    array = []
    for element in historical:
        array.append(crearElementosBasicosDelObject(element))
    array = sorted(array, key=lambda x: (-x['date'], x['homeTeam'], x['awayTeam']))

    for i in range(0, len(array)):
        array[i]['numero_partido'] = i + 1
        array[i]['node3_goals_expectative'] = 0
    return array


def crearElementosBasicosDelObject(object):
        neoObject = {}
        neoObject['date'] = calcularTiempo(object['Date'])
        neoObject['week'] = getWeek(neoObject['date'])
        neoObject['liga'] = object['liga']
        neoObject['temporada'] = object['temporada']
        neoObject['partido'] = object['HomeTeam'] + ' - ' + object['AwayTeam']
        neoObject['homeTeam'] = object['HomeTeam']
        neoObject['awayTeam'] = object['AwayTeam']
        neoObject['winner'] = object['FTR']
        neoObject['FTHG'] = object['FTHG']
        neoObject['FTAG'] = object['FTAG']
        neoObject['B365D'] = object['B365D']
        neoObject['BWD'] = object['BWD']
        neoObject['WHD'] = object['WHD']
        return neoObject

def calcularTiempo(fecha):
    if len(fecha.split('/')[2]) == 2:
        return datetime.strptime('20' + fecha.split('/')[2] + '-' + fecha.split('/')[1] + '-' + fecha.split('/')[0], "%Y-%m-%d").timestamp()
    return datetime.strptime(fecha.split('/')[2] + '-' + fecha.split('/')[1] + '-' + fecha.split('/')[0], "%Y-%m-%d").timestamp()

def getWeek(fecha):
    # Viernes 2 de Enero de 2009
    initialTime = 1230854400
    multiplicador_cuatro = 86400*4
    multiplicador_tres = 86400*3

    valorActual = initialTime
    for i in range(0, 100000):
        if i % 2 == 0:
            valorActual += multiplicador_tres
        if i % 2 == 1:
            valorActual += multiplicador_cuatro
        if valorActual > fecha:
            return i

def insertData(array):
    try:
        resultado = db2.dixonycoles_2.insert_many(array)
        return 'Todo OK'
    except ImportError:
        platform_specific_module = None
        return ('Ha habido un error')


main()
