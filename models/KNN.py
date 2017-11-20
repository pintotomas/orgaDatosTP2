import pandas as pd

from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split


def main():

	test_set = pd.read_csv("test_set.csv", compression = "gzip", low_memory = False)
	training_set = pd.read_csv("training_set.csv", compression = "gzip", low_memory = False)
    features = list(training_set.columns)
    features.remove("id")
    features.remove("price_aprox_usd")
    cant_features = len(features) - 2 #No tengo en cuenta Id y price_aprox_usd

    feature_actual = 1
    final_features = [features[0]] #empiezo probando con un solo feature y voy agregando si mejora la prediccion
    final_features.append("id")
    final_features.append("price_aprox_usd")
    
    scores_previos = []
    best_score = 0
    features_best_score = []

    

    while feature_actual < cant_features:
    
        print "Inicio"
        print "Best score actual: "+str(best_score)+" y hasta ahora las cols son: "+str(features_best_score)
        final_features.append(features[feature_actual])
        train_actual = training_set[final_features]
    
        labels = train_actual["price_aprox_usd"]
        train = train_actual.drop(["id","price_aprox_usd"], axis=1)
        x_train, x_test, y_train, y_test = train_test_split(train, labels, test_size = 0.30, random_state = 1)
        scores_actuales = []
        for x in range(8,30):
            print "Ahora probando con: "+str(x)+" vecinos"
            neigh = KNeighborsRegressor(n_neighbors= x)
            neigh.fit(x_train, y_train) 
            scores_actuales.append((x,neigh.score(x_test, y_test),list(final_features)))
        
        suma_actual = 0
        for score in scores_actuales:
            suma_actual += score[1]
        #si no se mejoro con este feature, lo remuevo
        if suma_actual < best_score:
            final_features.remove(features[feature_actual])
        else:
            best_score = suma_actual
            features_best_score = list(final_features)
        feature_actual += 1
        scores_previos.append(scores_actuales)
        print "fin"

main()
