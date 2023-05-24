import pandas as pd
import pgeocode
import time
import json

def coordinates(stad, steden):
    stadje = steden.loc[steden['place_name'] == stad]
    latitude = list(stadje['latitude'])[0]
    longitude = list(stadje['longitude'])[0]
    coordinate = str(latitude) + ',' + str(longitude) +';'
    return coordinate

with open("graph.txt", "r") as fp:
    graph = json.load(fp)

print(graph)

#conn = http.client.HTTPSConnection("trueway-matrix.p.rapidapi.com")

bel = pgeocode.Nominatim(country="BE")
steden = pd.DataFrame(bel._data)

headers = {
    'X-RapidAPI-Key': "871bf0c6a2msh23c0570c42956d3p1eec5fjsn8bfa2c9e0d94",
    'X-RapidAPI-Host': "trueway-matrix.p.rapidapi.com"
    }

for k, v in graph.items():
    route = "/CalculateDrivingMatrix?origins=" + coordinates(k, steden)
    for vk in v.keys():
        route += coordinates(vk, steden)
    
    i = 0
    for k in v.keys():
        v[k] = i
        i += 1
    print(v)
    time.sleep(1)
    #conn.request("GET", route, headers=headers)

    #res = conn.getresponse()
    #data = res.read()

    #distances = json.loads(data.decode("utf-8"))
    #durations = distances['durations']
    #i = 1
    #for k in v.keys():
        #v[k] = durations[i][0]
        #i += 1