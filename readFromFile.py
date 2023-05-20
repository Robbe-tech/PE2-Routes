import pandas as pd
import pgeocode

graph = {}

def coordinates(stad, steden):
    stad = steden.loc[steden['place_name'] == van]
    postcode = list(stad['postal_code'])[0]
    latitude = list(stad['latitude'])[0]
    longitude = list(stad['longitude'])[0]
    coordinate = str(latitude) + ',' + str(longitude) +';'
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
        print(coordinates(van, steden))
        if (van in graph.keys()):
            graph[van][naar] = 0
        else:
            graph[van] = {naar: 0}
    elif(data[n+1] == '\n' and data[n] != '\n'):
        #Einde N-weg
        van = data[n].strip()
        naar = data[n-1].strip()
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
        if (van in graph.keys()):
            graph[van][naar1] = 0
            graph[van][naar2] = 0
        else:
            graph[van] = {naar1: 0}
            graph[van][naar2] = 0

#with open("graph.txt", "w") as fp:
    #json.dump(graph, fp)