import pandas as pd
import numpy as np
from transformar_data import transformar

def propiedad_tiene(cualidades, propiedad):

    """Devuelve un 1 si la propiedad tiene alguna de las cualidades en 'cualidades', 0 si no."""
    tiene_cualidad = False
    if not(pd.isnull(propiedad["description"])):
        
        for cualidad in cualidades:
            tiene_cualidad = tiene_cualidad or (cualidad in propiedad["description"])
    return int(tiene_cualidad)


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return value[idx] #estan raros los nombres


def preocesar(df, relleno_nuls = None):
	"""Antes de correr esto tiene que haber pasado por recuperacion de datos
    relleno_nuls es un diccionario (feature:valor) que indica con que valor rellenar
    los nulos"""


    #Agregamos algunos features
    cualidades = {"pileta":["pileta","piscina"], "chalet":["chalet"], "patio":["patio"], "esquina":["esquina"], "a estrenar":["a estrenar"], "amenities":["amenities"], "quincho":["quincho"], "cochera": ["cochera"], "transporte":["subte","tren"], "parrilla":["parrilla"],"aire acondicionado":["aire acondicionado"],"cocina":["cocina"],"living":["living"]}

    for key in cualidades:
        df[key] = df.apply(lambda row: propiedad_tiene(cualidades[key], row), axis = 1)
    
    string_columns = ['description',"lat-lon" ,'place_name',
       'place_with_parent_names', 'property_type', 'state_name']
    
    #Transformo texto a numeros
    for f in string_columns:

        transformar(df, f)

    if relleno_nuls:
        for f in relleno_nuls:
            df[f].fillna(relleno_nuls[f], inplace = True)
    else:
        df.fillna(df.mean(), inplace = True)

    #Creo otras columnas:
    buckets_superficies1 = np.arange(0, 200000, 5)
    buckets_superficies2 = np.arange(0,200000,10)
    buckets_rooms1 = np.arange(0,12,2)
    buckets_rooms2 = np.arange(0,12,3)

    df["rooms1"] = df.apply(lambda row: find_nearest(row["rooms"], buckets_rooms1), axis = 1)
    df["rooms2"] = df.apply(lambda row: find_nearest(row["rooms"], buckets_rooms2), axis = 1)
    df["surface_total_in_m21"] = df.apply(lambda row: find_nearest(row["rooms"], buckets_superficies1), axis = 1)
    df["surface_total_in_m22"] = df.apply(lambda row: find_nearest(row["rooms"], buckets_superficies2), axis = 1)
    
def main():
    df = pd.read_csv("properati_data_fixed.csv",compression='gzip', low_memory = False)
    df2 = pd.read_csv("properati_testing_noprice_fixed.csv", compression='gzip', low_memory = False)
    procesar(df)
    cols_means = {}
    #Ver como hacer esto directamente usando el promedio del training set antes de rellenar
    for col in df_transformada.columns:
        cols_means[col] = df_transformada[col].mean()
    procesar(df2, cols_means)
    df.to_csv("training_set.csv", compression = "gzip", index = False)
    df.to_csv("test_set.csv", compression = "gzip", index = False)

main()
