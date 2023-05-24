import http.client
import json

conn = http.client.HTTPSConnection("trueway-matrix.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "871bf0c6a2msh23c0570c42956d3p1eec5fjsn8bfa2c9e0d94",
    'X-RapidAPI-Host': "trueway-matrix.p.rapidapi.com"
    }
#x = long + ',' + lat + ';'
Brussel = "50.8504,4.3488;"
Antwerpen = "51.2213,4.4051;"
Mechelen = "51.0259,4.4776;"
route = "/CalculateDrivingMatrix?origins=" + Brussel + Antwerpen + Mechelen

conn.request("GET", route, headers=headers)

res = conn.getresponse()
data = res.read()

distances = json.loads(data.decode("utf-8"))

#import http.client

#conn = http.client.HTTPSConnection("trueway-directions2.p.rapidapi.com")

#headers = {
#    'X-RapidAPI-Key': "871bf0c6a2msh23c0570c42956d3p1eec5fjsn8bfa2c9e0d94",
#    'X-RapidAPI-Host': "trueway-directions2.p.rapidapi.com"
#}

#conn.request("GET", "/FindDrivingRoute?stops=40.629041%2C-74.025606%3B40.630099%2C-73.993521%3B40.644895%2C-74.013818%3B40.627177%2C-73.980853", headers=headers)

#res = conn.getresponse()
#data = res.read()

#print(data.decode("utf-8"))


durations = distances['durations']
for i in range(1, len(durations)):
    print(durations[i][0])