import http.client

conn = http.client.HTTPSConnection("trueway-matrix.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "871bf0c6a2msh23c0570c42956d3p1eec5fjsn8bfa2c9e0d94",
    'X-RapidAPI-Host': "trueway-matrix.p.rapidapi.com"
    }

dest1 = "40.629041,-74.025606;"
route = "/CalculateDrivingMatrix?origins=" + dest1 + "40.630099%2C-73.993521%3B40.644895%2C-74.013818%3B40.627177%2C-73.980853&destinations=40.629041%2C-74.025606%3B40.630099%2C-73.993521%3B40.644895%2C-74.013818%3B40.627177%2C-73.980853"

conn.request("GET", route, headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))