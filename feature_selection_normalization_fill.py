import pandas as pd
#  estadisticas_training = {}
#    df_training.fillna(df_training.mean(),inplace=True) # Esto despues variarlo con imputacion a ver que resultados da
#    for column in df_training: 
#        estadisticas_training[column] = (df_training[column].mean(), df_training[column].min(), df_training[column].max()) 
#    
#    for column in df_training:
#        df_testing.fillna(estadisticas_training[column][0]) #Relleno con promedio del training
#    
#    #Ahora normalizamos
#    
#    columnas_normalizar = df_training.columns
#    columnas_normalizar.remove("price_aprox_usd")
#    for column in columnas_normalizar:
#        minimo = estadisticas_training[column][1]
#        maximo = estadisticas_training[column][2]
#        df_training[column] = (df_training[column] - minimo)/(maximo - minimo)
#        df_testing[column] = (df_testing[column] - minimo)/(maximo - minimo)
#                
#    
# 
##    #re armo los ids, al testing les pongo los de antes para poder hacer bien el submit
 ##


#def fill_nans(dataFrame, mean, zeros):
#	"""mean y zeros valen True segun como se quieran rellenar los nans"""
#	if (mean & zeros):
#		raise ValueError("Solo uno de los dos puede ser True")
#	
#	if mean:
#		dataFrame.fillna(dataFrame.mean(), inplace = True)
#	elif zeros:
#		dataFrame.fillna(0, inplace = True)


def main():
    
    #Aca eliminamos columnas, normalizamos y rellenamos nulls
    df_training = pd.read_csv("training_set_sin_normalizar_ni_rellenar.csv",compression='gzip', low_memory = False)
    df_testing = pd.read_csv("test_set_sin_normalizar_ni_rellenar.csv", compression='gzip', low_memory = False)
    
    #1er prueba: Eliminamos expensas y floor porque tenian demasiados valores nulos y no eran algo sencillo de rellenar,
    #aunque dos propiedades tengan caracteristicas similares no significa que esten en el mismo piso ni que paguen expensas
    #descripcion la sacamos porque a partir de esta columna ya creamos otras con la informacion que esta nos da
    #ademas dropeamos los nans, place_name tiene la informacion suficiente de place_with_parent_names
    print "Dropping labels"
    df_training.drop(labels = ["floor","expenses","description", "place_with_parent_names"], axis =1, inplace = True)
    df_testing.drop(labels = ["floor","expenses","description", "place_with_parent_names"], axis =1, inplace = True)
    
    #Probamos primero dropeando los nulos, quedan alrededor de 100k registros para el entrenamiento
    df_training.dropna(inplace = True)

    print "Normalizing data"
    #estadisticas_training = {}
    #for column in df_training: 
    #    estadisticas_training[column] = (df_training[column].mean(), df_training[column].min(), df_training[column].max()) 

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
    
main() 
