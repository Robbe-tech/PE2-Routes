import pandas as pd
import re
from pathlib import Path

df = {
    'Start' : [],
    'neighbour' : []
}

regex = "^[a-zA-Z]*$"

text_file = open("N-wegen.txt", "r")
data = text_file.readlines()

print(data)

for n in range(2, len(data) - 1):
    match_obj = re.search(regex, data[n])
    print(match_obj)
    print(n)
    if(data[n-2] == '\n'):
        #Vorige lijn is dan weg, begin weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n+1].strip())
    elif(data[n+1] == '\n'):
        #Einde N-weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n-1].strip())
    elif(data[n-1] != '\n' and data[n] != '\n'):
        #[ Data[n-1] = '\n' ] zijn de wegen
        #Midden van de weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n+1].strip())
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n-1].strip())


frame = pd.DataFrame(df)
frame.to_csv("connections.csv", mode="w")
print(frame)
text_file.close()
