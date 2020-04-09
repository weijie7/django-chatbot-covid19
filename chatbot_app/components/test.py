import numpy as np
import pandas as pd

data = pd.read_excel('database.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
print(data)

dlist = data["Responses"].tolist()
print(dlist)

nlist = [d.replace('\xa0',' ') for d in dlist]
print(nlist)
print(nlist[0])
