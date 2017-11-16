# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
def recuperar_superficie(rowProperati):
    if pd.isnull(rowProperati['surface_total_in_m2']):

        if (not((pd.isnull(rowProperati['price_aprox_usd']))) and (not(pd.isnull(rowProperati['price_usd_per_m2'])))):
            
            return rowProperati['price_aprox_usd']/rowProperati['price_usd_per_m2']
           
        else:
            return rowProperati['surface_total_in_m2']
    else:
        return rowProperati['surface_total_in_m2']

def recuperar_precio_usd(rowProperati):
    
    if pd.isnull(rowProperati['price_aprox_usd']):
    
        if (not(pd.isnull(rowProperati['surface_total_in_m2'])) and (not(pd.isnull(rowProperati['price_usd_per_m2'])))):
            
            return rowProperati['surface_total_in_m2']*rowProperati['price_usd_per_m2']
           
        else:
            return rowProperati['price_aprox_usd']
    else:
        return rowProperati['price_aprox_usd']

def recuperar_ppm2(rowProperati):
    if pd.isnull(rowProperati['price_usd_per_m2']):
        
        if (not(pd.isnull(rowProperati['price_aprox_usd'])) and (not(pd.isnull(rowProperati['surface_total_in_m2'])))):
        
            try:
                return rowProperati['price_aprox_usd']/rowProperati['surface_total_in_m2']
                
            except ZeroDivisionError:
                #Despues se filtra
                return 0
        else:
            return rowProperati['price_usd_per_m2']
    else:
        return rowProperati['price_usd_per_m2']


#Hay bastantes registros de capital federal que tienen como 'place_name' a 'Capital Federal'
#Se intenta recuperar la verdadera localidad usando geopy.
from geopy.geocoders import Nominatim

geolocator = Nominatim()
from time import sleep

def recuperar_barrios(barrios_zona, posiciones, zona):
	"""PRE: Posiciones es una lista de strings "lat-lon" a las que se les quiere buscar
	el barrio de capital a la cual hace referencia.
	POST: devuelve un diccionario con cada posicion como key, y valor su barrio correspondiente
	Si no se encuentra el barrio, quedara indicado como 'Capital Federal''"""
	number = 0
	posiciones_corregidas = dict()
	for pos in posiciones:
		try:
    

			direccion_definitiva = zona
			info = geolocator.reverse(pos,timeout = 10)
			a = info.address
			if (a != None):
				direccion = a.split(",")
			else:
				posiciones_corregidas[pos] = direccion
				continue
		
			for posible_barrio in direccion:
				if posible_barrio in barrios_zona:
					direccion_definitiva = posible_barrio
					break
	
			sleep(1)
			posiciones_corregidas[pos] = direccion_definitiva
		except GeocoderTimedOut as e:
			print "error"
			continue
	return posiciones_corregidas

def merge_files(directorio):
	"""Devuelve todos los archivos de properati juntados, sin ningun procesamiento"""
	import os
	#ignoro archivos ocultos
	filesProperati = filter( lambda f: not f.startswith('.'), os.listdir("datos/properati"))
	dataframes = []

	for file_name in filesProperati:
    
		newDataFrame = pd.read_csv("datos/properati/"+file_name, error_bad_lines = False)
		dataframes.append(newDataFrame)
	
	return dataframes


def filtrarCapitalYGBA(serie):
	"""Devuelve una lista de booleans de los registros de la serie que pertenecen a CABA, zs, zo o zn """

	deseados = ["Bs.As. G.B.A. Zona Norte", "Bs.As. G.B.A. Zona Sur", "Bs.As. G.B.A. Zona Oeste", "Capital Federal"]
	booleans = []
	for item in serie:
		if item.split("|")[2] in deseados:
			booleans.append(True)
		else:
			booleans.append(False)
	return booleans

def find_price(texto, start, end, min_price):
    """ texto es un texto spliteado por espacios, start es el indice de texto
    que contiene la palabra clave 'u$d', end es hasta donde buscamos
    en la tupl, min_price es el minimo precio que 
    consideramos valido """
    for j in range(start, end):
        split_act = texto[j]
        if split_act.replace(".","").isdigit():
                       
    	    num = float(split_act.replace(".",""))
            if num < min_price:
            #No tiene sentido
    	        return np.nan
            else:
    	        return num
	

def recuperar_precio_dolar_del_titulo(rowprop):
    """PRE: rowprop tiene la columna 'title' donde se puede buscar el precio"""
    if not(pd.isnull(rowprop["price_aprox_usd"])):
        return rowprop["price_aprox_usd"]
    title = rowprop["title"]
    if ("u$d" in title):
        split = title.split(" ")
        for x in range(0, len(split)):
            
            if ("u$d" in split[x]):
               return find_price(split, x + 1, x + 3, 900)

# Los que se pueden recuperar de la descripcion son unos pocos pero aun asi lo hacemos: 
def recuperar_precio_dolar_descripcion(rowprop):
    """PRE: rowprop tiene la columna 'description' donde se puede buscar el precio"""
    if not(pd.isnull(rowprop["price_aprox_usd"])):
        return rowprop["price_aprox_usd"]
    desc = rowprop["description"]
    if ("u$d" in desc):
        split = desc.split(" ")
        for x in range(0, len(split)):
    
            if ("u$d" in split[x]):

                return find_price(split, x + 1, x + 3, 900)
               
    return np.nan

#Hay bastantes con precio 0 que podemos arreglarlo con el precio encontrado en el titulo
def fix_prices(row):
    """PRE: Tiene la columna title"""
    if np.isfinite(row["price_aprox_usd"]):
        if row["price_aprox_usd"] > 1:
            return row["price_aprox_usd"]
        elif "u$d" in row["title"]:
            split = row["title"].split(" ")
                
            for x in range(0, len(split)):
    
                if ("u$d" in split[x]):

                    return find_price(split, x + 1, x + 3, 900)
        else:
            return row["price_aprox_usd"]
    else:
        return row["price_aprox_usd"]


def recuperar_sup_tot(row):
    if not(pd.isnull(row["surface_total_in_m2"])):
        return row["surface_total_in_m2"]
    try:
        desc = row["description"]

        if (("sup. total" in desc) or ("sup.total" in desc) or ("superficie total" in desc) or ("superficietotal" in desc)) and ("hectáreas" not in desc):
            split = desc.split(" ")
           
            for x in range(0, len(split)):
                
                if ("superficie total" in " ".join([split[x], split[x + 1]])) or ("sup. total" in " ".join([split[x], split[x + 1]])) or ("superficietotal" in split[x]) or ("sup.total" in split[x]):
   #Intentamos encontrar ese valor:
                    for j in range(x + 1, x+4):
                        act = split[j]
                        #Si es con coma solo me quedo con la parte entera
                        act2 = act.replace(","," ").replace("."," ").replace(":"," ").replace("m2"," ").split(" ")
                        for v in act2:
                            
                            if v.isdigit():
                                return float(v)     
    except:
         return np.nan
    return np.nan


def fix_superficie(row, error_value):
    """Intenta recuperar el valor de la superficie total en m2 de la descripcion
    error_value es lo minimo que consideramos como correcto para la superficie total"""
    if row["surface_total_in_m2"] >= error_value:
        return row["surface_total_in_m2"]
    try:
        row["description"]
    except:
        return row["surface_total_in_m2"]
    
    desc = row["description"]
    if (pd.isnull(desc)):
        return row["surface_total_in_m2"]

    if (("sup. total" in desc) or ("sup.total" in desc) or ("superficie total" in desc) or ("superficietotal" in desc)) and ("hectáreas" not in desc) and ("hectÃ¡reas" not in desc):
        split = desc.split(" ")
    try:
        for x in range(0, len(split)):
                
            if ("superficie total" in " ".join([split[x], split[x + 1]])) or ("sup. total" in " ".join([split[x], split[x + 1]])) or ("superficietotal" in split[x]) or ("sup.total" in split[x]):
   #Intentamos encontrar ese valor:
               
                for j in range(x + 1, x+4):
                    act = split[j]
                    #Si es con coma solo me quedo con la parte entera
                    act2 = act.replace(","," ").replace("."," ").replace(":"," ").replace("m2"," ").split(" ")
                    for v in act2:
                           
                        if v.isdigit():
                            if (float(v) != row["surface_total_in_m2"]):
                                return float(v)
          
    except:
        return row["surface_total_in_m2"]
    
    return row["surface_total_in_m2"]


def recuperar_superficie_cubierta(row):
    """PRE: row tiene la columna description"""
    try:
        if not(pd.isnull(row["surface_covered_in_m2"])):
            return row["surface_covered_in_m2"]
    except: #no tiene la columna
        pass
    
    desc = row["description"]
    keys = ["sup.cubierta","sup. cubierta", "superficie cubierta", "superficiecubierta"]
    if not(pd.isnull(desc)):
       
        split = desc.split(" ")
        
        for x in range(0, len(split)):
            if (split[x] in keys) or (" ".join([split[x - 1], split[x]]) in keys):
                
                if (x != len(split) - 1):
                    lim = x + 8
                    if (lim) > len(split):
                        lim = len(split)
                    for k in range(x, lim): #busco hasta 3 lugares despues
                        posible_num = split[k].replace("mts2","").replace("mÂ²","").replace(" ","").replace("?mts?^2,","").replace("m2c.","").replace("mts","").replace("(m²):","").replace("superficie","").replace("mtrs","").replace("*","").replace("de:","").replace("m2living","").replace("m²,","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").replace("(m2):","").replace("mtrs2","").replace("-","").replace("?","").replace(")","").replace("~","").replace("mts2","").replace("m2","").replace(":","").replace("."," ").replace(","," ").replace("m","").replace("m²","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").split(" ")

                        for u in posible_num:
                           
                            if u.isdigit() and (float(u) > 5):
                              
                                return u
                else: #debo buscar atras
                    
                    for k in range(x-3, x+1): #busco hasta 3 lugares despues
                      
                        posible_num = split[k].replace("mts2","").replace("mÂ²","").replace(" ","").replace("?mts?^2,","").replace("m2c.","").replace("mts","").replace("(m²):","").replace("superficie","").replace("mtrs","").replace("*","").replace("de:","").replace("m2living","").replace("m²,","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").replace("(m2):","").replace("mtrs2","").replace("-","").replace("?","").replace(")","").replace("~","").replace("mts2","").replace("m2","").replace(":","").replace("."," ").replace(","," ").replace("m","").replace("m²","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").split(" ")
                        for u in posible_num:
                            if u.isdigit() and (float(u) > 5):
                                return u
    return np.nan


#De los que son 0, cuantos hay de diferentes en la descripcion?
def recuperar_superficie_cubierta_ceros(row):
    """PRE: row tiene la columna description y surface_covered_in_m2"""
    if (pd.isnull(row["surface_covered_in_m2"])):
        return np.nan
    if (row["surface_covered_in_m2"] > 0):
        return row["surface_covered_in_m2"]
    desc = row["description"]
    keys = ["sup.cubierta","sup. cubierta", "superficie cubierta", "superficiecubierta"]
    if not(pd.isnull(desc)):
       
        split = desc.split(" ")
        
        for x in range(0, len(split)):
            if (split[x] in keys) or (" ".join([split[x - 1], split[x]]) in keys):
                
                if (x != len(split) - 1):
                    lim = x + 8
                    if (lim) > len(split):
                        lim = len(split)
                    for k in range(x, lim): #busco hasta 3 lugares despues
                        posible_num = split[k].replace("mÂ²","").replace(" ","").replace("?mts?^2,","").replace("m2c.","").replace("mts","").replace("(m²):","").replace("superficie","").replace("mtrs","").replace("*","").replace("de:","").replace("m2living","").replace("m²,","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").replace("(m2):","").replace("mtrs2","").replace("-","").replace("?","").replace(")","").replace("~","").replace("mts2","").replace("m2","").replace(":","").replace("."," ").replace(","," ").replace("m","").replace("m²","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").split(" ")

                        for u in posible_num:
                           
                            if u.isdigit() and (float(u) > 0) and (float(u) != row["surface_covered_in_m2"]) and (row["surface_covered_in_m2"] == 0):
                              
                                return u
                else: #debo buscar atras
                    
                    for k in range(x-3, x+1): #busco hasta 3 lugares despues
                      
                        posible_num = split[k].replace("mÂ²","").replace(" ","").replace("?mts?^2,","").replace("m2c.","").replace("mts","").replace("(m²):","").replace("superficie","").replace("mtrs","").replace("*","").replace("de:","").replace("m2living","").replace("m²,","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").replace("(m2):","").replace("mtrs2","").replace("-","").replace("?","").replace(")","").replace("~","").replace("mts2","").replace("m2","").replace(":","").replace("."," ").replace(","," ").replace("m","").replace("m²","").replace("ms","").replace("m2realizada","").replace("?mts?^2","").split(" ")
                        for u in posible_num:
                            if u.isdigit() and (float(u) > 0) and (float(u) != row["surface_covered_in_m2"]) and (row["surface_covered_in_m2"] == 0):
                                
                                return u

from datetime import datetime
from datetime import timedelta
def recuperar_precio_m2_en_dolares(rowProperati):
    if ~pd.isnull(rowProperati["price_per_m2"]) & pd.isnull(rowProperati["price_usd_per_m2"]):
    
        fechaCreacionPropiedad = rowProperati["created_on"]
        anho = int(fechaCreacionPropiedad.split("-")[0])
        mes = int(fechaCreacionPropiedad.split("-")[1])
        dia = int(fechaCreacionPropiedad.split("-")[2])
        fechaConCotizacion = datetime(anho, mes, dia)
        fechaEncontrada = False
        while not(fechaEncontrada):
            try:
                cotizFechaCreacProp = float(datosDolar.ix[fechaConCotizacion.strftime('%Y-%m-%d')]["Cotizacion Dolar"])
                fechaEncontrada = True
            except:
                #En esa fecha no se habia publicado informacion del dolar (no vario)
                #Me fijo en el dia anterior
                try:
                    fechaConCotizacion = fechaConCotizacion - timedelta(days = 1)
                except:
                    return np.nan
        return cotizFechaCreacProp*rowProperati["price_per_m2"]
    else:
        return rowProperati["price_per_m2"]

posibles_descripciones_piso = {'1° piso': 1,
'2° piso': 2,
'3° piso': 3,
'4° piso': 4,
'5° piso': 5,
'6° piso': 6,
'7° piso': 7,
'8° piso': 8,
'9° piso': 9,
'10° piso': 10,
'11° piso': 11,
'12° piso': 12,
'13° piso': 13,
'14° piso': 14,
'15° piso': 15,
'16° piso': 16,
'17° piso': 17,
'18° piso': 18,
'19° piso': 19,
'20° piso': 20,
'21° piso': 21,
'22° piso': 22,
'23° piso': 23,
'24° piso': 24,
'25° piso': 25,
'26° piso': 26,
'27° piso': 27,
'28° piso': 28,
'29° piso': 29,
'30° piso': 30,
'31° piso': 31,
'32° piso': 32,
'33° piso': 33,
'34° piso': 34,
'35° piso': 35,
'36° piso': 36,
'37° piso': 37,
'38° piso': 38,
'39° piso': 39,
'40° piso': 40,
'41° piso': 41,
'42° piso': 42,
'43° piso': 43,
'44° piso': 44,
'45° piso': 45,
'46° piso': 46,
'47° piso': 47,
'48° piso': 48,
'49° piso': 49,
'50° piso': 50,
"primer piso":1,
"segundo piso":2,
"tercer piso":3,"cuarto piso":4,"quinto piso":5,"sexto piso":6,"septimo piso":7,"octavo piso":8,
"noveno piso":9,"decimo piso":10,"décimo piso":10,"1er piso":1,"2do piso":2,"3er piso":3,"4to piso":4,
"5to piso":5,"6to piso":6,"7mo piso":7,"8vo piso":8,"9no piso":9,"10mo piso":10,"11vo piso":11,"12vo piso":12,"13vo piso":13, "14vo piso":14,
"15vo piso":15,"16vo piso":16,"17vo piso":17,"18vo piso":18,"19vo piso":19, "20vo piso":20}

posibles_descripciones_ambientes = {"1 ambiente": 1, "monoambiente": 1, "mono ambiente":1, "2 ambientes": 2,"3 ambientes": 3,
                          "4 ambientes": 4,"5 ambientes": 5, "6 ambientes": 6, "7 ambientes": 7,"8 ambientes": 8,
                          "9 ambientes": 1, "10 ambientes": 10,
                         "ambientes: 1": 1, "ambientes: 2": 2, "ambientes: 3": 3, "ambientes: 4": 4, "ambientes: 5": 5,
                         "ambientes: 6": 6, "ambientes: 7": 7, "un ambiente": 1, "dos ambientes": 2, "tres ambientes": 3,
                         "cuatro ambientes": 4,"cinco ambientes": 5," seis ambientes": 6, "siete ambientes": 7,
                         "2 impecables ambientes": 2, "3 impecables ambientes": 3, "4 amplios ambientes": 4, "2 amplios ambientes": 2,
                          "3 amplios ambientes": 3, "5 amplios ambientes": 5, "2  ambientes": 2, "3  ambientes": 3,
                          "2 grandes ambientes": 2, "6 amplios ambientes": 6, "1 ambientes": 1
                         ,"3 amplios  ambientes": 3, "3 y ½ ambientes": 3.5, "2 y medio ambiente": 2.5,
                         "(2) ambientes":2, "2 amplisimos ambientes": 2,"4  ambientes":4,"3 grandes ambientes":3,
                                   "4 ½ ambientes": 4.5, "4 cÃ²modos y confortables ambientes":4, "cantidad de ambientes 4":4,
                                   "cantidad de ambientes 3": 3,"ambientes : 4":4,"ambientes : 5":5,"ambientes : 3":3,"ambientes : 2":2,
                                   "ambientes : 1":1,"chalet de 5  ambientes":5,"4 cÃ³modos y confortables ambientes":4,"4   ambientes":4,
                                   "3 buenos ambientes":3,"4 còmodos y confortables ambientes":4}


def generar_barrios(data):
    barrios_caba = data[data["place_with_parent_names"].str.contains("Capital Federal")]["place_name"].value_counts().index
    barrios_caba.delete(0) #Elimino barrio 'Capital Federal'
    barrios_zn = []
    barrios_zo = []
    barrios_zs = []
    data_barrios = data["place_with_parent_names"]
    for v in data_barrios:
   
        if v.split("|")[2] == "Bs.As. G.B.A. Zona Oeste":
            try:
                if v.split("|")[4] not in barrios_zo:
                    barrios_zo.append(v.split("|")[4])
            except:
                if v.split("|")[3] not in barrios_zo:
                    barrios_zo.append(v.split("|")[3])
        elif v.split("|")[2] == "Bs.As. G.B.A. Zona Sur":
            try:
                if v.split("|")[4] not in barrios_zs:
                    barrios_zs.append(v.split("|")[4])
            except:
                if v.split("|")[3] not in barrios_zs:
                    barrios_zs.append(v.split("|")[3])
        elif v.split("|")[2] == "Bs.As. G.B.A. Zona Norte":
            try:
                if v.split("|")[4] not in barrios_zn:
                    barrios_zn.append(v.split("|")[4])
            except:
                if v.split("|")[3] not in barrios_zn:
                    barrios_zn.append(v.split("|")[3])

    barrios_zn.remove("")
    barrios_zo.remove("")
    barrios_zs.remove("")
    barrios = {"Capital Federal": barrios_caba, "Bs.As. G.B.A. Zona Oeste": barrios_zo, "Bs.As. G.B.A. Zona Sur":barrios_zs,
          "Bs.As. G.B.A. Zona Norte": barrios_zn}
    return barrios

def recuperar_barrio(row, info_barrios):
    place_actual = row["place_name"]
    #Si es nulo hacemos una busqueda mas exhaustiva 
    descripcion = row["description"]
    if (pd.isnull(place_actual)):
        zona = "Capital Federal"
        if row["place_with_parent_names"] == "Bs.As. G.B.A. Zona Norte":
            zona = "Bs.As. G.B.A. Zona Norte"
        
        elif row["place_with_parent_names"] == "Bs.As. G.B.A. Zona Sur":
            zona = "Bs.As. G.B.A. Zona Sur"
        elif row["place_with_parent_names"] == "Bs.As. G.B.A. Zona Oeste":
            zona = "Bs.As. G.B.A. Zona Oeste"
        barrios_posibles = info_barrios[zona]
        if not(pd.isnull(descripcion)):
            for b in barrios_posibles:
                if b in descripcion:
                    return b
    elif row["place_name"] in info_barrios:
        barrios_posibles = info_barrios[row["place_name"]]
        if not(pd.isnull(descripcion)):
            for b in barrios_posibles:
                if b in descripcion:
                    return b
       
    else:
        return row["place_name"]

def recuperar_atributo(row, atributo, info_atributo, search_title_and_extra = True):


    atributo_act = row[atributo]
    if not(pd.isnull(atributo_act)):
        return atributo_act
    
    descripcion = row["description"]
    atributo_corregido = atributo_act

    if not(search_title_and_extra):
        cols = [descripcion]
        for col in cols:
            if not(pd.isnull(col)):
                for k in info_atributo:
                    if k in col:
                        atributo_corregido = info_atributo[k]
                        return atributo_corregido
        return atributo_corregido #devuelvo nan si no lo consegui

    else:

        extra = row["extra"]
        title = row["title"]
        cols = [descripcion, extra, title]
        for col in cols:
            if not(pd.isnull(col)):
                for k in info_atributo:
                    if k in col:
                        atributo_corregido = info_atributo[k]
                        return atributo_corregido
        return atributo_corregido #Si no se logro encontro nunca, devuelvo el NaN

def fix_room_7071_floors(row):
    try:
        if row["floor"] == 7071:
            return 2 
        else:
            return row["rooms"]
    except:
        return row["rooms"]

def fixes_ambientes(row):
    if row["rooms"] == 34:
        return 4
    elif row["rooms"] == 33:
        return 3
    elif row["rooms"] == 32 or row["rooms"] == 30:
        desc = row["description"]
        if pd.isnull(desc):
            return row["rooms"]
        if "apartamento" in desc or "departamento" in desc:
            return 3
    return row["rooms"]

def fix_floors(row):
    try:
        if row["floor"] == 7071:
            return 1
        elif row["floor"] > 53:
            return 0 #Alvear Tower(54 pisos) y los de 54 no estan ahi
        return row["floor"]
    except:
        return row["floor"]

def main_fix_properati(directorio_propiedades_properati = "datos/properati"):
    dataframes = merge_files(directorio_propiedades_properati)
    
    #################################
    #################################
    ######AGREGAR LOS LOWER##########
    ######DE TITLE DESC Y EXTRA######
    #################################
    #################################
        
    #Filtro las de bs as
    print "Filtrando propiedades de CABA y GBA.."
    filtrados =[]
    for df in dataframes:
  
        df = df[filtrarCapitalYGBA(df['place_with_parent_names'])]
        filtrados.append(df)
	
	#Primero recuperamos algunos precios que estan en nulo y se pueden recuperar del titulo
    print "Recuperando informacion de los precios.."
    for df in filtrados:
	    if "title" in df.columns:
	        df["price_aprox_usd"] = df.apply(lambda row: recuperar_precio_dolar_del_titulo(row), axis = 1)

    for df in filtrados:
	    if "description" in df.columns:
	        df["price_aprox_usd"] = df.apply(lambda row: recuperar_precio_dolar_descripcion(row), axis = 1)

	#fixeamos algunos precios que se encontraban en 0, se vio en el notebook que eran los unicos
	#que se podian arreglar.
    for df in filtrados:
		if "title" in df.columns:
    			df["price_aprox_usd"] = df.apply(lambda row: fix_prices(row), axis = 1)
    	
    print "Arreglando datos sobre superficies totales/ cubiertas.."
    #recuperamos superficies totales nulas
    #Primero renombras la columna "surface_in_m2" que tienen algunos DF's en vez de superficie total
    for df in filtrados:
        if "surface_in_m2" in df.columns:
            df.rename(columns={'surface_in_m2': 'surface_total_in_m2'}, inplace = True)
    for df in filtrados:
        df["surface_total_in_m2"] = df.apply(lambda row: recuperar_sup_tot(row), axis = 1)
	
    minimo_superficie_total_aceptado = 9
    for df in filtrados:
  	    df["surface_total_in_m2"] = df.apply(lambda row: fix_superficie(row, minimo_superficie_total_aceptado),axis = 1)
	
    for df in filtrados:
        if "description" in df.columns:
            df["surface_covered_in_m2"] = df.apply(lambda row: recuperar_superficie_cubierta(row), axis = 1)

    for df in filtrados:
        if ("surface_covered_in_m2" in df) and ("description" in df):
        		df["surface_covered_in_m2"] = df.apply(lambda row: recuperar_superficie_cubierta_ceros(row), axis = 1)

	datosDolar = pd.read_csv("info_dolar.csv",index_col = "Fecha")
    
    
    for df in filtrados:
        if "price_per_m2" in df.columns:
            df["price_usd_per_m2"] = df.apply(lambda row: recuperar_precio_m2_en_dolares(row),axis=1)
    print "Calculando algunos datos faltantes.."
    for df in filtrados:
        df['surface_total_in_m2'] = df.apply(lambda row: recuperar_superficie(row),axis=1)
        df['price_aprox_usd'] = df.apply(lambda row: recuperar_precio_usd(row),axis=1)
        df['price_usd_per_m2'] = df.apply(lambda row: recuperar_ppm2(row),axis=1)

    
	unificacion = pd.concat(filtrados, axis=0, ignore_index=True)
    #Elimino los registros que tengan todas las columnas identicas
    a = unificacion.drop_duplicates(keep = "first")
    #Los que no tienen ni precio aproximado en dolares  ya no me interesan
    b = a[~a["price_aprox_usd"].isnull()]
    data = b.drop(["country_name","lat","lon","image_thumbnail",\
               "operation","price",'price_per_m2',"price_usd_per_m2","price_aprox_local_currency",
               "currency","created_on","geonames_id","id"," ",],axis=1)
#title y extra lo elimino despues porque lo uso para information retrieval
    #Elimino registros con misma url de properati, mismo precio y misma cantidad de habitaciones y piso 
    data = data.drop_duplicates(subset=["property_type","properati_url","price_aprox_usd","rooms","floor","place_name","surface_covered_in_m2","surface_total_in_m2","lat-lon","expenses","description","title","extra"])
    print "Recuperando barrios, ambientes y cantidad de pisos.."
    barrios_por_zona = generar_barrios(data)
    data["place_name"] = data.apply(lambda row: recuperar_barrio(row, barrios_por_zona), axis = 1)
    data["floor"] = data.apply(lambda row: recuperar_atributo(row, "floor", posibles_descripciones_piso), axis = 1)
    data["rooms"] = data.apply(lambda row: recuperar_atributo(row, "rooms", posibles_descripciones_ambientes), axis = 1)
    #No vale la pena recuperar nada de expensas, cambian con el tiempo y ademas esta el precio en ARS
    data["state_name"] = data.apply(lambda row: row["place_with_parent_names"].split("|")[2] if pd.isnull(row["state_name"]) else row["state_name"], axis = 1)
    data.drop(["extra", "title", "properati_url","expenses"], axis = 1, inplace = True)
    #Elimino algunos registros que no aportan nada ya que tienen columnas clave como nulas:
    print "Arreglando algunos outliers.."
    data.dropna(subset = ['rooms',
   'surface_total_in_m2'],how='all' ,axis = 0, inplace = True)

    #no tienen descripcion para arreglarlas
    data = data[data["floor"] != data["floor"].max()]
    data = data[data["price_aprox_usd"] != 0]
    data = data[data["price_aprox_usd"] > 5000]
    nul_rooms = data[data["rooms"].isnull()]
    data = data[data["rooms"] > 0]
    data = pd.concat([data, nul_rooms])
    data = data[data["rooms"] != 25] #descripcion rara
    data = data[data["rooms"] != 39] #sin descripcion
    data.drop_duplicates(inplace = True)
    data["rooms"] = data.apply(lambda row: fixes_ambientes(row), axis = 1)
    data["rooms"] = data.apply(lambda row: fix_room_floor_7071(row), axis = 1)
    data["floors"] = data.apply(lambda row: fix_floor_7071(row), axis = 1)
    data["surface_covered_in_m2"] = data.apply(lambda row: float(row["surface_covered_in_m2"])
                                           if not(pd.isnull(row["surface_covered_in_m2"])) else np.nan, axis = 1)
    data.to_csv("properati_data_fixed.csv", compression = "gzip", index = False)

def main_fix_test_set(filename):
    data = pd.read_csv(filename, low_memory = False)
    data["description"] = data["description"].str.lower()
    data["surface_total_in_m2"] = data.apply(lambda row: recuperar_sup_tot(row), axis = 1)
    minimo_superficie_total_aceptado = 9
    data["surface_total_in_m2"] = data.apply(lambda row: fix_superficie(row, minimo_superficie_total_aceptado),axis = 1)
    data["surface_covered_in_m2"] = data.apply(lambda row: recuperar_superficie_cubierta(row), axis = 1)
    data["surface_covered_in_m2"] = data.apply(lambda row: recuperar_superficie_cubierta_ceros(row), axis = 1)
    barrios_por_zona = generar_barrios(data)
    data["place_name"] = data.apply(lambda row: recuperar_barrio(row, barrios_por_zona), axis = 1)
    data["floor"] = data.apply(lambda row: recuperar_atributo(row, "floor", posibles_descripciones_piso, False), axis = 1)
    data["rooms"] = data.apply(lambda row: recuperar_atributo(row, "rooms", posibles_descripciones_ambientes, False), axis = 1)
    #No vale la pena recuperar nada de expensas, cambian con el tiempo y ademas esta el precio en ARS
    data["state_name"] = data.apply(lambda row: row["place_with_parent_names"].split("|")[2] if pd.isnull(row["state_name"]) else row["state_name"], axis = 1)
    data = data[['description', 'floor', 'lat-lon', 'place_name',
       'place_with_parent_names', 'property_type',
       'rooms', u'state_name', 'surface_covered_in_m2',
       'surface_total_in_m2']]
    data.to_csv("properati_testing_noprice_fixed.csv", compression = "gzip", index = False)
    ceros_imposibles = ["rooms","surface_total_in_m2"]
    for v in ceros_imposibles:
        #Despues se imputan o se llena con el promedio
        data[v] = data.apply(lambda row: np.nan if (row[v] == float(0)) else row[v], axis = 1)

import sys

def main():
    
    if len(sys.argv) != 2:
        print "ERROR! Solo se acepta 1 argumento, 1: arreglar datos de properati, 2: arreglar test set, 3: features training set, 4: features test set"
        return
    elif (sys.argv[1] == "1"):
        print "Se ejecutara 'Arreglar datos de properati'"
        main_fix_properati()
        return
    elif (sys.argv[1] == "2"):
        print "Se arreglara el set de test"
        main_fix_test_set("properati_dataset_testing_noprice.csv")
    else:
        print "TBD"
        return
main()
