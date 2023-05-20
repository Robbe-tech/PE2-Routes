import pandas as pd
import pgeocode

bel = pgeocode.Nominatim(country="BE")
connections = pd.read_csv("connections.csv")
print(connections)