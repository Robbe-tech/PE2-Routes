import pandas as pd
import re
import pgeocode
from pathlib import Path

df = {
    'Start' : [],
    'neighbour' : []
}

def convert():
    x = 0

i = 0

text_file = open("N-wegen.txt", "r", encoding='utf-8')
data = text_file.readlines()

bel = pgeocode.Nominatim(country="BE")
steden = pd.DataFrame(bel._data)

for n in range(2, len(data) - 1):
    if(data[n-2] == '\n' and data[n] != '\n'):
        #Vorige lijn is dan weg, begin weg
        stad = steden.loc[steden['place_name'] == data[n].strip()]
        if stad.empty:
            print(n)
            i += 1
            print(data[n].strip())
    elif(data[n+1] == '\n' and data[n] != '\n'):
        #Einde N-weg
        stad = steden.loc[steden['place_name'] == data[n].strip()]
        if stad.empty:
            print(n)
            i += 1
            print(data[n].strip())
    elif(data[n-1] != '\n' and data[n] != '\n'):
        #[ Data[n-1] = '\n' ] zijn de wegen
        #Midden van de weg
        stad = steden.loc[steden['place_name'] == data[n].strip()]
        if stad.empty:
            print(n)
            i += 1
            print(data[n].strip())
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n+1].strip())
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n-1].strip())


frame = pd.DataFrame(df)
print(frame)
frame.to_csv("connections.csv", mode="w", index=False)
text_file.close()
print(i)