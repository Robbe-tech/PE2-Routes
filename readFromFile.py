import pandas as pd

df = {
    'start' : [],
    'neighbour' : []
}


text_file = open("N-wegen.txt", "r")
data = text_file.readlines()

for n in len(data):
    if(n == 0):
        1
    elif(n == 1):
        2
    elif(n == (len(data) - 1)):
        3
    else:
        if(data[n-2] == '\n'):
            #Vorige lijn is dan N-weg
            1
        elif(data[n-1] == '\n'):
            #Dit mijn N-weg
            2
        elif(data[n+1] == '\n'):
            #Einde N-weg
            3
        else:
            #Midden van N-weg
            4
    
    

    


print(data)
text_file.close()
