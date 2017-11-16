import pandas as pd
import numpy as np
import hashlib

def string2numeric_hash(text):
  
    return int(hashlib.md5(text).hexdigest()[:8], 16)

def transformar(data, column):
	""" data es el dataframe ya abierto, column es una columna de strings a hashear
en el intervalo (0,1)"""
	data[column] = data.apply(lambda row:  string2numeric_hash(row[column]) if not(pd.isnull(row[column])) else np.nan, axis = 1)
	
