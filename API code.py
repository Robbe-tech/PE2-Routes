import http.client

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

print(data.decode("utf-8"))