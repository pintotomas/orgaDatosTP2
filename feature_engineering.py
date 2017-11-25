# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
def propiedad_tiene(cualidades, propiedad):

    """Devuelve un 1 si la propiedad tiene alguna de las cualidades en 'cualidades', 0 si no."""
    tiene_cualidad = False
    if not(pd.isnull(propiedad["description"])):
        descripcion = propiedad["description"]
	descripcion.replace(":"," ").replace("*"," ").replace("."," ").replace(","," ").replace("-"," ").replace("/"," ").replace("'"," ").replace("¿"," ").replace("?"," ").replace("á","a").replace("é","e").replace("á","a").replace("í"," ").replace("ó","o").replace("ú","u").replace("_"," ")
        for cualidad in cualidades:
            tiene_cualidad = tiene_cualidad or (cualidad in propiedad["description"])
    return int(tiene_cualidad)


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return value[idx] #estan raros los nombres


def agregar_features(df, relleno_nuls = None):
    """Antes de correr esto tiene que haber pasado por recuperacion de datos
    relleno_nuls es un diccionario (feature:valor) que indica con que valor rellenar
    los nulos"""


    #Agregamos algunos features
    cualidades = {"pileta":["pileta","piscina"],
		  "chalet":["chalet"],
		  "patio":["patio"],
		  "esquina":["esquina"],
		  "estrenar":["estrenar","nuevo"],
		  "amenities":["amenities"],
		  "quincho":["quincho"],
		  "cochera": ["cochera","cocheras","garaje","garage"],
		  "transporte_rapido":["subte","tren"],
		  "transporte_lento":["colectivo","colectivos","linea de colectivo","linea de colectivos"],
		  "parrilla":["parrilla","parrillas"],
		  "aire_acondicionado":["aire acondicionado","aires acondicionados","aire acondicionados","aires acondicionado"],
		  "cocina":["cocina","horno"],
		  "living":["living","living comedor"],
		  "comedor":["comedor","living comedor"],
		  "antigua":["antigua","antiguedad"],
		  "balcon_terraza":["balcon","terraza"],
		  "suite":["suite"],"hall":["hall"],
		  "espacios_verdes":["parque","jardin","plaza"],
		  "seguridad":["seguridad","guardia","vigilancia","camaras de seguridad"],
		  "terreno":["terreno"],
		  "gimnasio":["gimnasio","gim","gym"],
		  "solarium":["solarium"],
          "sauna":["sauna"],
          "jacuzzi":["jacuzzi"],
          "hidromasaje":["hidromasaje"],
          "sum":["sum"],
		  "terreno":["terreno"],
		  "laundry":["laundry","lavarropas","lavanderia","lavadero"],
		  "shopping":["shopping"],
		  "educacion":["colegio","colegios","universidad","biblioteca"],
		  "buen_estado":["excelente estado","excelente","buen estado"],
		  "lujoso":["lujoso"],
		  "vista":["excelente vista", "especatacular vista","ventanal","hermosa vista","hermoso paisaje","paisaje","linda vista","vista al rio","vista a la ciudad"],
          "toilette":["toilette"],
          "palier":["palier"],
          "parquet":["parquet"],
          "luminosidad":["luminoso","luminosidada","iluminado","luz"],
          "terreno":["terreno"],
          "dormitorio":["dormitorio"],
          "torre":["torre"],
          "edificio":["edificio"]
		 }

    for key in cualidades:
        df[key] = df.apply(lambda row: propiedad_tiene(cualidades[key], row), axis = 1)
    
    string_columns = ["lat-lon" ,'place_name', 'property_type', 'state_name','place_with_parent_names']
    
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
    df["surface_total_in_m21"] = df.apply(lambda row: find_nearest(row["surface_total_in_m2"], buckets_superficies1), axis = 1)
    df["surface_total_in_m22"] = df.apply(lambda row: find_nearest(row["surface_total_in_m2"], buckets_superficies2), axis = 1)
    df["surface_covered_in_m21"] = df.apply(lambda row: find_nearest(row["surface_covered_in_m2"], buckets_superficies1), axis = 1)
    df["surface_covered_in_m22"] = df.apply(lambda row: find_nearest(row["surface_covered_in_m2"], buckets_superficies2), axis = 1)


def main():
    df_training = pd.read_csv("training_set_filling_nans_con_vecinos.csv",compression='gzip', low_memory = False)
    df_testing = pd.read_csv("testing_set_filling_nans_con_vecinos.csv", compression='gzip', low_memory = False)
   
    cols_finales = list(df_testing.columns)
    cols_finales.append("price_aprox_usd")

    #Saco algunas columnas que no interesan
    to_drop =["created_on", "operation", "country_name", "lat","lon","title","extra","geonames_id","year"]
    for c in to_drop:
        if c in df_training:
            df_training.drop(c, axis = 1, inplace = True)
        if c in df_testing.columns:
            df_testing.drop(c, axis = 1, inplace = True)

    #Orden de las columnas:
    df_training = df_training[[u'description', u'expenses', u'floor', u'id', u'lat-lon', u'place_name',
       u'place_with_parent_names' , u'property_type',
       u'rooms', u'state_name', u'surface_covered_in_m2',
       u'surface_total_in_m2',u'price_aprox_usd']]

  
    print "se estan agregando features a df_training"
    agregar_features(df_training)
    print "Se estan agregando features a df_testing"
    agregar_features(df_testing)

    print "Dropping labels"
    df_training.drop(labels = ["description"], axis =1, inplace = True)
    df_testing.drop(labels = ["description"], axis =1, inplace = True)

    print "Normalizing data"
    columnas_normalizar = list(df_training.columns)
    columnas_normalizar.remove("price_aprox_usd")
    columnas_normalizar.remove("id")

    for column in columnas_normalizar:
    	minimo=df_training[column].min()
    	maximo=df_training[column].max()
        df_training[column] = (df_training[column] - minimo)/(maximo - minimo)
        df_testing[column] = (df_testing[column] - minimo)/(maximo - minimo)

    print "Saving"
    df_training.to_csv("training_set_normalizado_sacando_nans.csv",compression="gzip", index = False)
   
    df_testing.to_csv("testing_set_normalizado_sacando_nans.csv",compression="gzip", index = False)    

    #df_training.to_csv("training_set_sin_normalizar_ni_rellenar.csv", compression = "gzip", index = False)
    #df_testing.to_csv("test_set_sin_normalizar_ni_rellenar.csv", compression = "gzip", index = False)
main()
