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

for n in range(2, len(data) - 1):
    if(data[n-2] == '\n' and data[n] != '\n'):
        #Vorige lijn is dan weg, begin weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n+1].strip())
        if(data[n] == '\n'):
            print(n)
        if(data[n+1] == '\n'):
            print(n+1)
    elif(data[n+1] == '\n' and data[n] != '\n'):
        #Einde N-weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n-1].strip())
        if(data[n] == '\n'):
            print(n)
        if(data[n-1] == '\n'):
            print(n-1)
    elif(data[n-1] != '\n' and data[n] != '\n'):
        #[ Data[n-1] = '\n' ] zijn de wegen
        #Midden van de weg
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n+1].strip())
        df['Start'].append(data[n].strip())
        df['neighbour'].append(data[n-1].strip())
        if(data[n] == '\n'):
            print(n)
        if(data[n+1] == '\n'):
            print(n+1)
        if(data[n-1] == '\n'):
            print(n-1)


frame = pd.DataFrame(df)
frame.to_csv("connections.csv", mode="w")
print(frame)
text_file.close()
