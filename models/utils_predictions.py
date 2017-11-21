#Aca tambien podemos agregar un archivo que haga un ensamble de los distintos modelos escribiendo el promedio de los distintos modelos
#en el archivo resultante

def make_predictions(model, test_set, final_features, file_name):

	"""model: el modelo entrenado
	   test_set: registros con los features que ayudan a predecir
           final_features: features usados para entrenar el modelo, si se usaron todos es test_set.columns
           file_name: nombre del archivo donde guardar los resultados"""

	i = 0
	with open('knn_predictions2.csv', 'wb') as csvfile:
    		scorewriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
		scorewriter.writerow("id","price_usd")
    		while i < len(ids):
        		scorewriter.writerow([ids[i],knn_predictions[i]])
        		i+=1
