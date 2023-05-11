import pandas as pd
import re
from pathlib import Path

df = {
    'Start' : [],
    'neighbour' : []
}


text_file = open("N-wegen.txt", "r")
data = text_file.readlines()

print(data)

for n in range(1, len(data) - 1):
    if(data[n-2] == '\n'):
        #Vorige lijn is dan weg, begin weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n+1].strip())
    elif(data[n+1] == '\n'):
        #Einde N-weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n-1].strip())
    elif(data[n-1] != '\n'):
        #[ Data[n-1] = '\n' ] zijn de wegen
        #Midden van de weg
        if (re.findall("/d:", data[n-1])):
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n+1].strip())
        else:
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n+1].strip())
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n-1].strip())
    

frame = pd.DataFrame(df)
frame.to_csv("connections.csv", mode="w")
print(frame)
text_file.close()
