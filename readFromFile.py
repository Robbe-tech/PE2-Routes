import panda as pd


text_file = open("N-wegen.txt", "r")
data = text_file.read()
text_file.close()
print(data)