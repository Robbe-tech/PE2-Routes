import pandas as pd
import pgeocode
import time
import requests
import json

graph = {}

def coordinates(stad, steden):
    stadje = steden.loc[steden['place_name'] == stad]
    latitude = list(stadje['latitude'])[0]
    longitude = list(stadje['longitude'])[0]
    coordinate = str(latitude) + ',' + str(longitude)
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

length = 0
for k, v in graph.items():
    for kv in v.keys():
        if(kv == k):
            v.pop(kv)

for v in graph.values():
    length += len(v)
print(length)

payload={}
headers = {}

for k, v in graph.items():
    for vk in v.keys():
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + coordinates(k, steden) + "&destinations=" + coordinates(vk, steden) + "&key=AIzaSyDSrzlCIqDzpxM7qP9GWqViU4tP0NvZEck"
        response = requests.request("GET", url, headers=headers, data=payload)
        respond = json.loads(response.text)
        v[vk] = respond["rows"][0]["elements"][0]["duration"]["value"]
        time.sleep(0.1)

with open("graph.txt", "w") as fp:
    json.dump(graph, fp)