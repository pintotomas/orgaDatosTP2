#Aca tambien podemos agregar un archivo que haga un ensamble de los distintos modelos escribiendo el promedio de los distintos modelos
#en el archivo resultante

def make_predictions(model, test_set, final_features, file_name):

	"""model: el modelo entrenado
	   test_set: registros con los features que ayudan a predecir
           final_features: features usados para entrenar el modelo, si se usaron todos es test_set.columns
           file_name: nombre del archivo donde guardar los resultados
	   
	   escribe un archivo con (id,price_usd) con las predicciones del modelo y lo guarda con el nombre
	   file_name"""

	i = 0
	ids = list(test_set["id"].values)
	predictions = model.predict(test_set[final_features])
	with open(file_name, 'wb') as csvfile:
    		scorewriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
		scorewriter.writerow(["id,price_usd"])
    		while i < len(ids):
        		scorewriter.writerow([ids[i],predictions[i]])
        		i+=1
