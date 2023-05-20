import pandas as pd
import pgeocode

graph = {}

def coordinates(stad, steden, n):
    stadje = steden.loc[steden['place_name'] == van]
    coordinate = 0
    if(len(stadje) == 1):
        postcode = list(stadje['postal_code'])[0]
        latitude = list(stadje['latitude'])[0]
        longitude = list(stadje['longitude'])[0]
        coordinate = str(latitude) + ',' + str(longitude) +';'
    else:
        print(n)
        print(stad)
    return coordinate

i = 0

text_file = open("N-wegen.txt", "r", encoding='utf-8')
data = text_file.readlines()
text_file.close()

bel = pgeocode.Nominatim(country="BE")
steden = pd.DataFrame(bel._data)

for n in range(2, len(data) - 1):
    if(data[n-2] == '\n' and data[n] != '\n'):
        #Vorige lijn is dan weg, begin weg
        van = data[n].strip()
        naar = data[n+1].strip()
        coordinates(van, steden, n)
        if (van in graph.keys()):
            graph[van][naar] = 0
        else:
            graph[van] = {naar: 0}
    elif(data[n+1] == '\n' and data[n] != '\n'):
        #Einde N-weg
        van = data[n].strip()
        naar = data[n-1].strip()
        coordinates(van, steden, n)
        if (van in graph.keys()):
            graph[van][naar] = 0
        else:
            graph[van] = {naar: 0}
    elif(data[n-1] != '\n' and data[n] != '\n'):
        #[ Data[n-1] = '\n' ] zijn de wegen
        #Midden van de weg
        van = data[n].strip()
        naar1 = data[n+1].strip()
        naar2 = data[n-1].strip()
        coordinates(van, steden, n)
        if (van in graph.keys()):
            graph[van][naar1] = 0
            graph[van][naar2] = 0
        else:
            graph[van] = {naar1: 0}
            graph[van][naar2] = 0

#with open("graph.txt", "w") as fp:
    #json.dump(graph, fp)