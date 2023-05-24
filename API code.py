import requests
import json

Brussel = "50.8504,4.3488"
Antwerpen = "51.2213,4.4051"

url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + Brussel + "&destinations=" + Antwerpen + "&key=AIzaSyDSrzlCIqDzpxM7qP9GWqViU4tP0NvZEck"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
respond = json.loads(response.text)

print(respond["rows"][0]["elements"][0]["duration"]["value"])