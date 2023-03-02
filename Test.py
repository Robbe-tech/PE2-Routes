dict = {1:2, 2:1, 3:1}
print(min(dict.values(), key=dict.get))