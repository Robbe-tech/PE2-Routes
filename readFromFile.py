import pandas as pd
from pathlib import Path

df = {
    'Start' : [],
    'neighbour' : []
}


text_file = open("N-wegen.txt", "r")
data = text_file.readlines()

for n in range(len(data)):
    if(n > 1 and n < (len(data) - 1)):
        if(data[n-2] == '\n'):
            #Vorige lijn is dan N-weg, begin N-weg
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n+1].strip())
        elif(data[n+1] == '\n'):
            #Einde N-weg
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n-1].strip())
        elif(data[n-1] != '\n'):
            #[ Data[n-1] = '\n' ] zijn de N-wegen
            #Midden van N-weg
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n+1].strip())
            df['Start'].append(data[n].strip())
            df['neighbour'].append(data[n-1].strip())
    

frame = pd.DataFrame(df)
frame.to_csv("connections.csv")
print(frame)
text_file.close()
