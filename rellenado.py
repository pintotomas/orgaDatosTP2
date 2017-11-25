# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


posibles_descripciones_ambientes = {"1 ambiente": 1, "monoambiente": 1, "mono ambiente":1, "2 ambientes": 2,"3 ambientes": 3,
                          "4 ambientes": 4,"5 ambientes": 5, "6 ambientes": 6, "7 ambientes": 7,"8 ambientes": 8,
                          "9 ambientes": 1, "10 ambientes": 10,
                         "ambientes: 1": 1, "ambientes: 2": 2, "ambientes: 3": 3, "ambientes: 4": 4, "ambientes: 5": 5,
                         "ambientes: 6": 6, "ambientes: 7": 7, "un ambiente": 1, "dos ambientes": 2, "tres ambientes": 3,
                         "cuatro ambientes": 4,"cinco ambientes": 5," seis ambientes": 6, "siete ambientes": 7,
                         "2 impecables ambientes": 2, "3 impecables ambientes": 3, "4 amplios ambientes": 4, "2 amplios ambientes": 2,
                          "3 amplios ambientes": 3, "5 amplios ambientes": 5, "2  ambientes": 2, "3  ambientes": 3,
                          "2 grandes ambientes": 2, "6 amplios ambientes": 6, "1 ambientes": 1
                         ,"3 amplios  ambientes": 3, "3 y ½ ambientes": 3.5,"2 y ½ ambientes": 2.5, "2 y medio ambiente": 2.5,
                         "(2) ambientes":2, "2 amplisimos ambientes": 2,"4  ambientes":4,"3 grandes ambientes":3,
                                   "4 ½ ambientes": 4.5, "4 cÃ²modos y confortables ambientes":4, "cantidad de ambientes 4":4,
                                   "cantidad de ambientes 3": 3,"ambientes : 4":4,"ambientes : 5":5,"ambientes : 3":3,"ambientes : 2":2,
                                   "ambientes : 1":1,"chalet de 5  ambientes":5,"4 cÃ³modos y confortables ambientes":4,"4   ambientes":4,
                                   "3 buenos ambientes":3,"4 còmodos y confortables ambientes":4,"2 amb.":2,"3 amb.":3,"4 amb.":4,"1 amb.":1, "5 amb.":5,"6 amb.":6,"7 amb.":7,
                                   "3 (tres) ambientes": 3, "2 (dos) ambientes":2, "4 (cuatro) ambientes":4, "5 (cinco) ambientes": 5, "1 (uno) ambientes": 1, "1 (uno) ambiente":1,
                                   "6 (seis) ambientes":6, "7 (siete) ambientes":7, "8 (ocho) ambientes":8, "9 (nueve) ambientes":9, "10 (diez) ambientes":10, "1 amb":1, "2 amb":2,
                                   "3 amb":3, "4 amb":4, "5 amb":5, "6 amb":6,"7 amb":7,"8 amb":8,"2 ambiente":2,"3 ambiente":3,"4 ambiente":4, "1amb":1,"2amb":2,"3amb":3,"4amb":4,
                                   "5amb":5,"6amb":6,"8amb":8,"7amb":7,"mnonoambiente":1}

def fix_ambientes(row, search_title, search_extra, search_description):
    
    if pd.isnull(row["rooms"]):
        return np.nan#Ya fueron fixeadas
    cols = []
    if search_description:
        descripcion = row["description"]
        cols.append(descripcion)
    if search_extra:
        extra = row["extra"]
        cols.append(extra)
    if search_title:
        title = row["title"]
        cols.append(title)
        
    ambiente_actual = row["rooms"]
    for col in cols:
        if not(pd.isnull(col)):
            for k in posibles_descripciones_ambientes:
        
                if k in col:
                    value_found = float(posibles_descripciones_ambientes[k])
                    if float(row["rooms"]) != value_found:
                        return value_found
    return row["rooms"]

def fix_rooms_sup_cubierta_ilegal(row):
    rooms = row["rooms"]
    description = row["description"]
    if pd.isnull(rooms):
        return np.nan
    for k in posibles_descripciones_ambientes:
        if k in description: #Si lo encuentra, ya habia sido corregido y entonces esta bien
            return rooms
    
    covered_surface = row["surface_covered_in_m2"]
    
    if pd.isnull(covered_surface):
        return rooms
    if rooms == 1:
        
        if covered_surface > 65:
            return np.nan
        elif covered_surface < 9: #El minimo aceptado para un ambiente es de 3x3
            return np.nan
        else:
            return 1
        
    elif rooms == 2:
       
        if (covered_surface >= 18) & (covered_surface < 628):
            return 2
        elif (covered_surface < 18) & (covered_surface >= 9):
            return 1
        else: #es menor a 9
            return np.nan
        
        
    elif rooms == 3:
        if covered_surface > 650:
            return np.nan
        elif (covered_surface >= 27):
            return 3
        elif (covered_surface >= 18):
            return 2
        elif (covered_surface >= 9):
            return 1
        else: #es menor a 9
            return np.nan
       
    elif rooms == 4:
        if covered_surface > 660:
            return np.nan
        elif (covered_surface >= 36):
            return 4 
        elif (covered_surface >= 27):
            return 3 #En realidad podria ser ser 2 o 1 tambien.. 
        elif (covered_surface >= 18):
            return 2
        elif (covered_surface >= 9):
            return 1
        else:
            return np.nan
    elif rooms == 5:
        if covered_surface > 780:
            return np.nan
        elif (covered_surface >= 45):
            return 5
        elif (covered_surface >= 36):
            return 4 #En realidad podria ser ser 2 o 1 tambien.. 
        elif (covered_surface >= 27):
            return 3
        elif (covered_surface < 27):
            return 2
        elif (covered_surface >= 9):
            return 1
        else:
            return np.nan
    
    elif rooms == 6:
        #No lo acoto superiormente, son pocos los puntos, tal vez no son outliers
        if (covered_surface >= 6*9):
            return 6
        elif (covered_surface >= 45):
            return 5
        elif (covered_surface >= 36):
            return 4 #En realidad podria ser ser 2 o 1 tambien.. 
        elif (covered_surface >= 27):
            return 3
        elif (covered_surface < 27):
            return 2
        elif (covered_surface >= 9):
            return 1
        else:
            return np.nan
    
    elif rooms == 7:
        #No lo acoto superiormente, son pocos los puntos, tal vez no son outliers
        if (covered_surface >= 7*9):
            return 7
        elif (covered_surface >= 6*9):
            return 6
        elif (covered_surface >= 45):
            return 5
        elif (covered_surface >= 36):
            return 4 #En realidad podria ser ser 2 o 1 tambien.. 
        elif (covered_surface >= 27):
            return 3
        elif (covered_surface < 27) :
            return 2
        elif (covered_surface >= 9):
            return 1
        else:
            return np.nan
    elif rooms == 8:
        #No lo acoto superiormente, son pocos los puntos, tal vez no son outliers
        if (covered_surface >= 8*9):
            return 8
        elif (covered_surface >= 7*9):
            return 7
        elif (covered_surface >= 6*9):
            return 6
        elif (covered_surface >= 45):
            return 5
        elif (covered_surface >= 36):
            return 4 #En realidad podria ser ser 2 o 1 tambien.. 
        elif (covered_surface >= 27):
            return 3
        elif (covered_surface < 27) :
            return 2
        elif (covered_surface >= 9):
            return 1
        else:
            return np.nan
        
        
    elif covered_surface >= rooms*9:
        return rooms
    else:
        return np.nan # no cumple con lo minimo y ya son bastantes ambientes

#A los que tengan una superficie total < a la cubierta: Les asigno la cubierta
def fix_surface_total_menor_cubierta(row):
    if pd.isnull(row["surface_total_in_m2"]) or pd.isnull(row["surface_covered_in_m2"]):
        return row["surface_total_in_m2"]
    elif row["surface_total_in_m2"] < row["surface_covered_in_m2"]:
        return row["surface_covered_in_m2"]
    else:
        return row["surface_total_in_m2"]


saved_results = {}
#A partir de la superficie total y la cantidad de ambientes empiezo a arreglar la sup. cubierta
def fill_superficie_cubierta_con_total_y_ambientes(row, df):
    
    if not(pd.isnull(row["surface_covered_in_m2"])):
        return row["surface_covered_in_m2"]
    ambientes = row["rooms"]
    sup_total = row["surface_total_in_m2"]
    avg_cubierta = np.nan
    dif = 0
    if (ambientes,sup_total) in saved_results:
        return saved_results[(ambientes,sup_total)]
    while pd.isnull(avg_cubierta):    
        lim_inf = sup_total - dif
        lim_sup = sup_total + dif
        act_vecindario = df[(df["surface_total_in_m2"] < lim_sup) & (df["rooms"] == ambientes)]
        act_vecindario = act_vecindario[act_vecindario["surface_total_in_m2"] > lim_inf]
        avg_cubierta = act_vecindario["surface_covered_in_m2"].mean()
        dif += 1
        if (dif > 20): #para que sea mas rapido
            dif += 20
    #Guardo el resultado 
    saved_results[(ambientes, sup_total)] = avg_cubierta
    return avg_cubierta

def fill_superficie_cubierta_con_total_y_ambientes_set_test(row,df):
    ambientes = row["rooms"]
    sup_total = row["surface_total_in_m2"]
    
    if not(pd.isnull(row["surface_covered_in_m2"])):
        
        return row["surface_covered_in_m2"]
    if pd.isnull(ambientes) | pd.isnull(sup_total):
        return np.nan
    
    avg_cubierta = np.nan
    dif = 0
    if (ambientes,sup_total) in saved_results:
        return saved_results[(ambientes,sup_total)]
    while pd.isnull(avg_cubierta):    
        lim_inf = sup_total - dif
        lim_sup = sup_total + dif
        act_vecindario = df[(df["surface_total_in_m2"] < lim_sup) & (df["rooms"] == ambientes)]
        act_vecindario = act_vecindario[act_vecindario["surface_total_in_m2"] > lim_inf]
        avg_cubierta = act_vecindario["surface_covered_in_m2"].mean()
        dif += 1
        if (dif > 20): #para que sea mas rapido
            dif += 20
    #Guardo el resultado 
    saved_results[(ambientes, sup_total)] = avg_cubierta
    return avg_cubierta

#para rellenar los rooms
saved_surface_total_rooms = {}
def fix_nan_rooms(row, df):
    if not(pd.isnull(row["rooms"])):
        return row["rooms"] #Si ya tenia la cantidad de rooms, esto esta bien
    
    sup_cub = row["surface_covered_in_m2"]
    if sup_cub in saved_surface_total_rooms:
        return saved_surface_total_rooms[sup_cub]
    avg_rooms = np.nan
    dif = 0
    while pd.isnull(avg_rooms):    
        lim_inf = sup_cub - dif
        lim_sup = sup_cub + dif
        act_vecindario = df[df["surface_covered_in_m2"] < lim_sup]
        act_vecindario = df[df["surface_covered_in_m2"] > lim_inf]
        avg_rooms = act_vecindario["rooms"].mean()
        dif += 5
    saved_surface_total_rooms[sup_cub] = avg_rooms
    return avg_rooms
        
def fix_nan_rooms_set_test(row, df):
    if not(pd.isnull(row["rooms"])):
        return row["rooms"] 
    if pd.isnull(row["surface_covered_in_m2"]):
        return np.nan
    
    sup_cub = row["surface_covered_in_m2"]
    if sup_cub in saved_surface_total_rooms:
        return saved_surface_total_rooms[sup_cub]
    avg_rooms = np.nan
    dif = 0
    while pd.isnull(avg_rooms):    
        lim_inf = sup_cub - dif
        lim_sup = sup_cub + dif
        act_vecindario = df[df["surface_covered_in_m2"] < lim_sup]
        act_vecindario = df[df["surface_covered_in_m2"] > lim_inf]
        avg_rooms = act_vecindario["rooms"].mean()
        dif += 5
    saved_surface_total_rooms[sup_cub] = avg_rooms
    return avg_rooms

#A las que tengan place_name nulo le asigno su state_name
def fix_null_place_name(row):
    if pd.isnull(row["place_name"]):
        return row["state_name"]
    return row["place_name"]

#A los de lat-lon nula, busco entre los que tengan el mismo place name y le asigno algun lat lon 
#de ellos
saved_lat_lons = {}
def fix_lat_lon(row, df):
    if not(pd.isnull(row["lat-lon"])):
        return row["lat-lon"]
    place = row["place_name"]
    if place in saved_lat_lons:
        return saved_lat_lons[place]
    same_place = df[df["place_name"] == place]
    same_place_w_lat_lon = same_place[~same_place["lat-lon"].isnull()]
    try:
        final_pos = same_place_w_lat_lon["lat-lon"].values[0]
    except:
        return np.nan
    saved_lat_lons[place] = final_pos
    return final_pos

#¿que dicen estas descripciones?
def recover_expensas(row):
    v = row["description"]
    if (pd.isnull(row["expenses"])) or (row["expenses"] < 10):
        
        if "expensas" in v:
            dsplit = v.split(" ")
            for x in range (0, len(dsplit)):
                if "expensas" in dsplit[x]:
                    start = x - 5
                    end = x + 5
                    if end >= len(dsplit):
                        end = len(dsplit) - 1
                    if start <= 0:
                        start = 0
                    expensa_recuperada = 0
                    if "$" in " ".join(dsplit[start:end]):
                        for j in range(x,end):
                            act = dsplit[j].replace(".","").replace("consultas","").replace("(","").replace("apto","").replace(")","").replace(".-"," ").replace("$","").replace("abl:","").replace(".","").replace("-no","").replace("-","").replace("!","").split(" ")
                            for n in act:
                                if n.isdigit():
                                    expensa_recuperada = float(n)
                                    if expensa_recuperada != 2017: #Se confunde con el año
                                        return expensa_recuperada
           
        return 0 #Devuelvo 0 si no estaba
    else:
        return row["expenses"]

def mean_surf_cov(row, df):
    ambientes = row["rooms"]
    sup_tot = row["surface_total_in_m2"]
    if pd.isnull(ambientes):
        if pd.isnull(sup_tot):
            return np.nan
        else:
            try:
                alrededor_misma_sup_tot = df[(df["surface_total_in_m2"] > sup_tot - 10) & (df["surface_total_in_m2"] < sup_tot + 10)]
                return alrededor_misma_sup_tot["surface_covered_in_m2"].mean()
            except:
                return np.nan
    else:
        mismos_ambientes = df[df["rooms"] == ambientes]
        return mismos_ambientes["surface_covered_in_m2"].mean()

def main():

    data = pd.read_csv("properati_data_fixed_all_years_duplicated_with_outliers.csv", compression = "gzip")
    data_2017 = data[data["year"] == 2017]
	#Sacamos las de Zona Norte porque no tenemos que predecir casi ninguna de esa zona.
    data_2017_zo_zs_caba = data_2017[(data_2017["state_name"] == "Capital Federal") | (data_2017["state_name"] == "Bs.As. G.B.A. Zona Sur") | (data_2017["state_name"] == "Bs.As. G.B.A. Zona Oeste")]
    #Vuelvo a aplicar fix_rooms porque agregue unos keywords mas
    data_2017_zo_zs_caba["rooms"] = data_2017_zo_zs_caba.apply(lambda row: fix_ambientes(row, False, False, True), axis = 1)

    #Los que se les desconoce de a pares la cantidad de ambientes, superficie total, cubierta,
    #son registros que describen muy poco a la propiedad. Los eliminamos
    data_2017_zo_zs_caba.dropna(axis = 0,how='all', subset=["rooms","surface_total_in_m2"], inplace = True)
    data_2017_zo_zs_caba.dropna(axis = 0,how='all', subset=["rooms","surface_covered_in_m2"], inplace = True)
    data_2017_zo_zs_caba.dropna(axis = 0,how='all', subset=["surface_covered_in_m2","surface_total_in_m2"], inplace = True)
    df = data_2017_zo_zs_caba.copy()
    df["rooms"] = df.apply(lambda row: fix_rooms_sup_cubierta_ilegal(row), axis = 1)
    df["surface_total_in_m2"] = df.apply(lambda row: row["surface_total_in_m2"] if row["surface_total_in_m2"] >= 9 else np.nan, axis = 1)
    df["surface_covered_in_m2"] = df.apply(lambda row: row["surface_covered_in_m2"] if row["surface_covered_in_m2"] >= 9 else np.nan, axis = 1)
    df.dropna(axis = 0,how='all', subset=["rooms","surface_total_in_m2"], inplace = True)
    df.dropna(axis = 0,how='all', subset=["rooms","surface_covered_in_m2"], inplace = True)
    df.dropna(axis = 0,how='all', subset=["surface_covered_in_m2","surface_total_in_m2"], inplace = True)
    df["surface_total_in_m2"] = df.apply(lambda row: fix_surface_total_menor_cubierta(row), axis=1)
    #Elimino propiedades que tengan una superficie total muy alta y un precio muy bajo
    df = df[(df["surface_total_in_m2"] < 2000) | ((df["surface_total_in_m2"] >= 2000) & df["price_aprox_usd"] > 600000)]
    df = df[df.index != 1127206] #propiedaad outlier
    df["surface_covered_in_m2"]= df.apply(lambda row: fill_superficie_cubierta_con_total_y_ambientes(row, df), axis = 1)
    df["rooms"] = df.apply(lambda row: fix_nan_rooms(row,df), axis = 1)
    #fill con 0 las que no se pudo obtener info del piso
    df["floor"].fillna(0, inplace = True)
    df["place_name"] = df.apply(lambda row: fix_null_place_name(row), axis = 1)
    df["lat-lon"] = df.apply(lambda row: fix_lat_lon(row,df), axis = 1)
    grandBell = "-34.905998,-58.071173"
    altosDeHudsonI = "-34.802731,-58.168713"
    elMetejon = "-34.951520,-58.666861"
    latlonNuls = {"Grand Bell":grandBell,"Altos de Hudson I": altosDeHudsonI,"El Metejon":elMetejon} 
    df["lat-lon"] = df.apply(lambda row: row["lat-lon"] if not(pd.isnull(row["lat-lon"])) else latlonNuls[row["place_name"]], axis = 1)
    saved_lat_lons = {}
    df["expenses"] = df.apply(lambda row: float(row["expenses"]), axis = 1)
    df["expenses"] = df.apply(lambda row: recover_expensas(row), axis = 1)
    #https://www.infobae.com/economia/2017/04/11/las-expensas-aumentaran-35-por-ajuste-de-tarifas-e-inflacion/
    #las expensas promedio para 1/2 ambientes son de 2000, las que tienen expensas muy bajas
    #las pongo como cero
    df["expenses"] = df.apply(lambda row: row["expenses"] if row["expenses"] > 500 else 0, axis = 1)
    df.drop(labels = ["year"], axis = 1, inplace = True)
    df.drop_duplicates(inplace = True)
    df.to_csv("training_set_filling_nans_con_vecinos.csv", compression ="gzip", index = False)

    print "Ahora ejecutando el programa para df_testing"
    df_pred = pd.read_csv("LO IMPORTANTE/properati_testing_noprice_fixed.csv", compression = 'gzip')
    df_pred["rooms"] = df_pred.apply(lambda row: fix_rooms_sup_cubierta_ilegal(row), axis = 1)
    df_pred["surface_total_in_m2"] = df_pred.apply(lambda row: row["surface_total_in_m2"] if row["surface_total_in_m2"] >= 9 else np.nan, axis = 1)
    df_pred["surface_covered_in_m2"] = df_pred.apply(lambda row: row["surface_covered_in_m2"] if row["surface_covered_in_m2"] >= 9 else np.nan, axis = 1)
    df_pred["surface_total_in_m2"] = df_pred.apply(lambda row: fix_surface_total_menor_cubierta(row), axis=1)
    df_pred["surface_covered_in_m2"] = df_pred.apply(lambda row: fill_superficie_cubierta_con_total_y_ambientes_set_test(row, df), axis = 1)
    df_pred["surface_covered_in_m2"] = df_pred.apply(lambda row: row["surface_covered_in_m2"] if (row["surface_covered_in_m2"] < 2000) else np.nan, axis = 1)
    df_pred["rooms"] = df_pred.apply(lambda row: fix_nan_rooms_set_test(row,df), axis = 1)
    df_pred["floor"].fillna(0, inplace = True)
    df_pred["place_name"] = df_pred.apply(lambda row: fix_null_place_name(row), axis = 1)
    df_pred["lat-lon"] = df_pred.apply(lambda row: fix_lat_lon(row,df), axis = 1)
    original = pd.read_csv("LO IMPORTANTE/properati_dataset_testing_noprice.csv", low_memory = False)
    df_pred["expenses"] = original["expenses"]
    df_pred["expenses"] = df_pred.apply(lambda row: float(row["expenses"]) if (str(row["expenses"]).isdigit()) else np.nan, axis = 1)
    df_pred["expenses"] = df_pred.apply(lambda row: recover_expensas(row), axis = 1)
    df_pred["expenses"] = df_pred.apply(lambda row: row["expenses"] if row["expenses"] > 500 else 0, axis = 1)
    #A los que tienen superficie total nula en los de prediccion los relleno con su superficie cubierta 
    df_pred["surface_total_in_m2"] = df_pred.apply(lambda row: row["surface_total_in_m2"] if not(pd.isnull(row["surface_total_in_m2"])) else row["surface_covered_in_m2"], axis = 1)

    #Si conozco la cantidad de ambientes y no la superficie cubierta, lleno con la superficie promedio para esa cantidad de ambientes
    df_pred["surface_covered_in_m2"] = df_pred.apply(lambda row: row["surface_covered_in_m2"] if not(pd.isnull(row["surface_covered_in_m2"])) else mean_surf_cov(row, df), axis = 1)
    #Con esto vuelvo a aplicar la primer funcion para rellnar el total

    df_pred["surface_total_in_m2"] = df_pred.apply(lambda row: row["surface_total_in_m2"] if not(pd.isnull(row["surface_total_in_m2"])) else row["surface_covered_in_m2"], axis = 1)
    #Si solo conozco la superficie total y no la cubierta ni cantidad de ambiente, busco para su sup. total la cubierta promedio
    df_pred["surface_covered_in_m2"] = df_pred.apply(lambda row: row["surface_covered_in_m2"] if not(pd.isnull(row["surface_covered_in_m2"])) else mean_surf_cov(row,df), axis = 1)
    #aplico esto devuelta
    df_pred["rooms"] = df_pred.apply(lambda row: fix_nan_rooms_set_test(row,df), axis = 1)
    df_pred["lat-lon"].fillna("a", inplace = True)
	  renames = {"departamento":"apartment","casa":"house","ph":"PH"}
	  df_pred["property_type"] = df_pred.apply(lambda row: renames[row["property_type"]], axis = 1)
    df_pred.to_csv("testing_set_filling_nans_con_vecinos.csv", compression ="gzip", index = False)

main()
