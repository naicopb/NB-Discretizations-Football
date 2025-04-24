from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.primera_y_segunda

def main():
    array = [
    {"homeTeam": "Alaves", "awayTeam": "Ath Bilbao"},
    {"homeTeam": "Alcorcon", "awayTeam": "Getafe"},
    {"homeTeam": "Alcoyano", "awayTeam": "Elche"},
    {"homeTeam": "Almeria", "awayTeam": "Granada"},
    {"homeTeam": "Ath Bilbao", "awayTeam": "Sociedad"},
    {"homeTeam": "Ath Madrid", "awayTeam": "Real Madrid"},
    {"homeTeam": "Barcelona", "awayTeam": "Espanol"},
    {"homeTeam": "Betis", "awayTeam": "Sevilla"},
    {"homeTeam": "Burgos", "awayTeam": "Numancia"},
    {"homeTeam": "Cadiz", "awayTeam": "Xerez"},
    {"homeTeam": "Cartagena", "awayTeam": "Murcia"},
    {"homeTeam": "Castellon", "awayTeam": "Villareal"},
    {"homeTeam": "Celta", "awayTeam": "La Coruna"},
    {"homeTeam": "Cordoba", "awayTeam": "Jaen"},
    {"homeTeam": "Eibar", "awayTeam": "Sociedad"},
    {"homeTeam": "Elche", "awayTeam": "Hercules"},
    {"homeTeam": "Fuenlabrada", "awayTeam": "Getafe"},
    {"homeTeam": "Getafe", "awayTeam": "Leganes"},
    {"homeTeam": "Gimnastic", "awayTeam": "Reus Deportiu"},
    {"homeTeam": "Granada", "awayTeam": "Malaga"},
    {"homeTeam": "Levante", "awayTeam": "Valencia"},
    {"homeTeam": "Llagostera", "awayTeam": "Girona"},
    {"homeTeam": "Lorca", "awayTeam": "Cartagena"},
    {"homeTeam": "Lugo", "awayTeam": "La Coruna"},
    {"homeTeam": "Malaga", "awayTeam": "Almeria"},
    {"homeTeam": "Mirandes", "awayTeam": "Burgos"},
    {"homeTeam": "Murcia", "awayTeam": "UCAM Murcia"},
    {"homeTeam": "Osasuna", "awayTeam": "Sociedad"},
    { "homeTeam": "Oviedo", "awayTeam": "Sp Gijon" },
    { "homeTeam": "Ponferradina", "awayTeam": "Leonesa" },
    { "homeTeam": "Reus Deportiu", "awayTeam": "Gimnastic" },
    { "homeTeam": "Santander", "awayTeam": "Ath Bilbao" },
    { "homeTeam": "Tenerife", "awayTeam": "Las Palmas" },
    { "homeTeam": "Valladolid", "awayTeam": "Numancia" },
    { "homeTeam": "Vallecano", "awayTeam": "Getafe" },
    { "homeTeam": "Villarreal", "awayTeam": "Valencia" },
    { "homeTeam": "Zaragoza", "awayTeam": "Huesca" }
    ]

    array2 = []
    for i in range(0, len(array)):
        neoObjeto = {}
        neoObjeto['homeTeam'] = array[i]['awayTeam']
        neoObjeto['awayTeam'] = array[i]['homeTeam']
        array[i]['partidos'] = 0
        neoObjeto['partidos'] = 0
        array[i]['empates'] = 0
        neoObjeto['empates'] = 0
        array2.append(array[i])
        array2.append(neoObjeto)



    historical = convertInArray(getHistorical())
    counter = 0
    counterEmpates = 0
    for i in range(0, len(historical)):
        for j in range(0, len(array2)):
            if historical[i]['HomeTeam'] == array2[j]['homeTeam'] and historical[i]['AwayTeam'] == array2[j]['awayTeam']:
                counter += 1
                array2[j]['partidos'] +=1
                print(historical[i]['FTR'] + ' Derby = ' + historical[i]['HomeTeam'] +' - ' + historical[i]['AwayTeam'])
                if historical[i]['FTR'] == 'D':
                    counterEmpates += 1
                    array2[j]['empates'] +=1

    for i in range(0, len(array2)):
        if array2[i]['partidos'] != 0:
            array2[i]['media'] = array2[i]['empates']/array2[i]['partidos']
    imprime(array2)
    print(counter)
    print(counterEmpates)
    print(counterEmpates/counter)

def imprime(array):
    for i in range(0, len(array)):
        print(array[i])

def convertInArray(historico):
    array = []
    for jornada in historico:
        array.append(jornada)
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
