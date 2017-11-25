import pandas as pd
import numpy as np

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


def procesar(df, relleno_nuls = None):
    """Antes de correr esto tiene que haber pasado por recuperacion de datos
    relleno_nuls es un diccionario (feature:valor) que indica con que valor rellenar
    los nulos"""


    #Agregamos algunos features
    cualidades = {"pileta":["pileta","piscina"], "chalet":["chalet"], "patio":["patio"], "esquina":["esquina"], "a estrenar":["a estrenar"], "amenities":["amenities"], "quincho":["quincho"], "cochera": ["cochera"], "transporte":["subte","tren"], "parrilla":["parrilla"],"aire acondicionado":["aire acondicionado"],"cocina":["cocina"],"living":["living"], "antigua":["antigua"]}

    for key in cualidades:
        df[key] = df.apply(lambda row: propiedad_tiene(cualidades[key], row), axis = 1)
    
    string_columns = ["lat-lon" ,'place_name',
       'place_with_parent_names', 'property_type', 'state_name']
    
    #Transformo texto a numeros
    for f in string_columns:

        df[f] = df.apply(lambda row:  hash(row[f]) if not(pd.isnull(row[f])) else np.nan, axis = 1)
	

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
    #Solo entrenamos con las de 2015 en adelante
    
    df_training = pd.read_csv("2015-2017_fixed_noduplicates_removed_outliers.csv",compression='gzip', low_memory = False)
    df_testing = pd.read_csv("properati_testing_noprice_fixed.csv", compression='gzip', low_memory = False)
    df_training["expenses"] = df_training.apply(lambda row: recover_expenses(row), axis = 1)
    df_testing["expenses"] = df_training.apply(lambda row: recover_expenses(row), axis = 1)
   
    cols_finales = list(df_testing.columns)
    cols_finales.append("price_aprox_usd")
    df_training = df_training[cols_finales]

    #Saco algunas columnas que no interesan
    to_drop =["created_on", "operation", "country_name", "lat","lon","title","extra","geonames_id"]
    for c in to_drop:
        if c in df_training:
            df_training.drop(c, axis = 1, inplace = True)
        if c in df_testing.columns:
            df_testing.drop(c, axis = 1, inplace = True)
    print "Se dropearon columnas"
    columnas_training = df_training.columns
    columnas_testing = df_testing.columns
    for c in columnas_training:
        if c not in columnas_testing and c != "price_aprox_usd":
            print "ERROR: "+c
            return
    for c in columnas_testing:
        if c not in columnas_training and c != "price_aprox_usd":
            print "Error "+c
            return

    print "se procesara df_training"
    procesar(df_training)
    print "Se procesara df_testing"
    procesar(df_testing)
	#Habia borrado los id's sin querer
    test_noprice = pd.read_csv("properati_dataset_testing_noprice.csv", low_memory = False)
    ids = test_noprice["id"].values
    df_testing["id"] = ids
    df_training.reset_index(inplace = True)
    df_training.rename(columns={'index': 'id'}, inplace = True)
    df_training.to_csv("training_set_sin_normalizar_ni_rellenar.csv", compression = "gzip", index = False)
    df_testing.to_csv("test_set_sin_normalizar_ni_rellenar.csv", compression = "gzip", index = False)
main()
