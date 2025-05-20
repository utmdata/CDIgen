#Script per generar els fitxers posicion, meteo i termosal entre dues dates

#1 (la primera vegada)crear entorn virtual python3 -m venv venv
#2 Entrar a lentorn virtual source venv/bin/activate
#3 Instal·lar els requeriments: pip install -r requirements.txt
#4 Run el fitxer


import os
import pandas as pd
from urllib import request
from datetime import datetime, timedelta
import sys
import shutil
import zipfile

def main(vessel_input, date_inicial, date_final):
    carpeta_temp = "./temp"
    # Eliminar els arxius a la carpeta temp després de processar-los
    for archivo in os.listdir(carpeta_temp):
        archivo_path = os.path.join(carpeta_temp, archivo)
        
        if os.path.isfile(archivo_path):
            os.remove(archivo_path)

    
    
    inicial_sin_hora = date_inicial.split(" ")[0]
    print(inicial_sin_hora)
    dia, mes, any = inicial_sin_hora.split("/")
    # Demanar el rang de dates a l'usuari
    dia_inicial = int(dia[:2])
    print (dia_inicial)
    mes_inicial = int(mes [:2])
    any_inicial = int (any [:4])
    final_sin_hora = date_final.split(" ")[0]
    dia2, mes2, any2 = final_sin_hora.split("/")
    dia_final = int(dia2 [:2])
    mes_final = int(mes2[:2])
    any_final = int(any2[:4])


    # Assignar el mode i el codi del vaixell segons l'elecció de l'usuari
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_code = "SG"
    elif vessel_input == "hes":
        vessel_mode = "Hesperides" 
        vessel_code = "HE"   
    elif vessel_input == "odb":
        vessel_mode = "Odon" 
        vessel_code = "OB"

    # Crear el rang de dates
    fecha_inicio = datetime(any_inicial, mes_inicial, dia_inicial)
    fecha_fin = datetime(any_final, mes_final, dia_final)
    # Generar la llista de dates entre l'inici i el final
    lista_fechas = [(fecha_inicio + timedelta(days=d)).strftime("%d%m%Y")
                    for d in range((fecha_fin - fecha_inicio).days + 1)]

    # Crear la carpeta temporal per desar els arxius descarregats
    carpeta_temp = "./temp"
    os.makedirs(carpeta_temp, exist_ok=True)

    # Descarregar els arxius per a cada data
    for fecha in lista_fechas:
        try:
            # Construir l'URL per descarregar les dades de posició segons la data
            url = f"http://161.111.139.31/datos/{vessel_mode}/{fecha[2:4]}-{fecha[4:8]}/posicion.proc/{fecha}.posicion.proc"
            local_path = os.path.join(carpeta_temp, f"{fecha}.posicion.csv")
            request.urlretrieve(url, local_path)  # Descarregar l'arxiu
            
        except Exception as e:
            print(f"Error al descarregar arxiu {fecha}: {e}")
    print(f"generant...: ")
    # Processar els arxius descarregats
    archivos_posicion = [os.path.join(carpeta_temp, f) for f in os.listdir(carpeta_temp) if f.endswith(".csv")]
    dataframes = []

    # Llegir i emmagatzemar els arxius CSV descarregats
    for archivo in archivos_posicion:
        try:
            df = pd.read_csv(archivo, sep=None, engine="python", header=None)  # Llegir l'arxiu CSV
            dataframes.append(df)  # Afegir el DataFrame a la llista
            
        except Exception as e:
            print(f"Error al processar {archivo}: {e}")

    # Si hi ha arxius per combinar
    if dataframes:
        # Concatenar tots els DataFrames en un sol
        df_combinado = pd.concat(dataframes, ignore_index=True)

        # Eliminar les capçaleres repetides
        cabecera = df_combinado.iloc[0]  # Primera fila com a capçalera
        df_combinado = df_combinado[~df_combinado.apply(lambda x: x.equals(cabecera), axis=1)]  # Eliminar files que coincideixen amb la capçalera
        df_combinado.columns = cabecera  # Assignar les capçaleres correctes

        # Canviar el format de la columna 0 (data)
        df_combinado[df_combinado.columns[0]] = pd.to_datetime(df_combinado[df_combinado.columns[0]], format='%d-%m-%Y %H:%M:%S')

        # Ordenar per la columna de data (completa: any, mes, dia, hora, minut, segon)
        df_combinado = df_combinado.sort_values(by=df_combinado.columns[0], ascending=True)

        # Nou format AAAA-MM-DD hh:mm:ss.0
        df_combinado[df_combinado.columns[0]] = df_combinado[df_combinado.columns[0]].dt.strftime('%Y-%m-%d %H:%M:%S.0')

        # Guardar l'arxiu final amb les dades combinades
        nombre_csv_final = f"29{vessel_code}{fecha_inicio.strftime('%Y%m%d')}_posicion.csv"
        df_combinado.to_csv(nombre_csv_final, index=False)
        
        print(f"Arxiu generat: {nombre_csv_final}")
    else:
        print("No s'han trobat arxius per combinar.")

    # Eliminar els arxius de la carpeta temporal després de processar-los
    for archivo in os.listdir(carpeta_temp):
        archivo_path = os.path.join(carpeta_temp, archivo)
        
        if os.path.isfile(archivo_path):
            os.remove(archivo_path)  # Eliminar arxiu


    # Descarregar els arxius per a cada data METEO
    for fecha in lista_fechas:
        try:
            url = f"http://161.111.139.31/datos/{vessel_mode}/{fecha[2:4]}-{fecha[4:8]}/meteo.proc/{fecha}.meteo.proc"
            local_path = os.path.join(carpeta_temp, f"{fecha}.meteo.csv")
            request.urlretrieve(url, local_path)
        except Exception as e:
            print(f"Error al descarregar arxiu {fecha}: {e}")

    # Processar els arxius descarregats
    archivos_meteo = [os.path.join(carpeta_temp, f) for f in os.listdir(carpeta_temp) if f.endswith(".csv")]
    dataframes = []

    # Llegir i emmagatzemar els arxius en DataFrame
    for archivo in archivos_meteo:
        try:
            df = pd.read_csv(archivo, sep=None, engine="python", header=None)
            dataframes.append(df)
        except Exception as e:
            print(f"Error al processar {archivo}: {e}")

    # Si hi ha arxius per combinar, procedim
    if dataframes:
        # Concatenar tots els DataFrames
        df_combinado = pd.concat(dataframes, ignore_index=True)

        # Eliminar les capçaleres repetides
        cabecera = df_combinado.iloc[0]  # Primera fila com a capçalera
        df_combinado = df_combinado[~df_combinado.apply(lambda x: x.equals(cabecera), axis=1)]  # Eliminar files que coincideixen amb la capçalera
        df_combinado.columns = cabecera  # Assignar les capçaleres correctes

        # Canviar el format de la columna 0 (data)
        df_combinado[df_combinado.columns[0]] = pd.to_datetime(df_combinado[df_combinado.columns[0]], format='%d-%m-%Y %H:%M:%S')

        # Ordenar per la columna de data (completa: any, mes, dia, hora, minut, segon)
        df_combinado = df_combinado.sort_values(by=df_combinado.columns[0], ascending=True)

        # Formatejar la data en el nou format AAAA-MM-DD hh:mm:ss.0
        df_combinado[df_combinado.columns[0]] = df_combinado[df_combinado.columns[0]].dt.strftime('%Y-%m-%d %H:%M:%S.0')

        # Guardar l'arxiu final
        nombre_meteo_final = f"29{vessel_code}{fecha_inicio.strftime('%Y%m%d')}_meteo.csv"
        df_combinado.to_csv(nombre_meteo_final, index=False)
        print(f"generant...: {nombre_meteo_final}")
            # Eliminar els arxius a la carpeta temp després de processar-los
        for archivo in os.listdir(carpeta_temp):
            archivo_path = os.path.join(carpeta_temp, archivo)
            
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)

        # Nom de l'arxiu de posició
        nombre_posicion = f"29{vessel_code}{fecha_inicio.strftime('%Y%m%d')}_posicion.csv"
        # Llegir els arxius de meteo i de posició
        meteo_df = pd.read_csv(nombre_meteo_final)  # Substitueix 'meteo.csv' pel nom del teu arxiu
        posicion_df = pd.read_csv(nombre_posicion)  # Substitueix 'posicion.csv' pel nom del teu arxiu de posicions

        # Netegem la columna 'fecha' per eliminar qualsevol text extra
        meteo_df['fecha'] = meteo_df['fecha'].str.replace(r'\.0$', '', regex=True)
        posicion_df['fecha'] = posicion_df['fecha'].str.replace(r'\.0$', '', regex=True)

        # Assegura't que les columnes de data i hora en ambdós arxius estiguin en format datetime
        meteo_df['datetime'] = pd.to_datetime(meteo_df['fecha'], format='%Y-%m-%d %H:%M:%S')
        posicion_df['datetime'] = pd.to_datetime(posicion_df['fecha'], format='%Y-%m-%d %H:%M:%S')

        # Realitzar la combinació per data i hora
        merged_df = pd.merge(meteo_df, posicion_df[['datetime', 'latitud', 'longitud']], 
                            on='datetime', how='left')

        # Eliminar la columna 'fecha' de meteo ja que anem a utilitzar 'datetime' com 'fecha'
        merged_df = merged_df.drop(columns=['fecha'])

        # Renombrar la columna 'datetime' a 'fecha'
        merged_df = merged_df.rename(columns={'datetime': 'fecha'})

        # Reordenar les columnes perquè 'fecha', 'longitud', 'latitud' siguin les primeres, seguides de les columnes de meteo
        merged_df = merged_df[['fecha', 'longitud', 'latitud','velocidad_media_viento', 'velocidad_inst_viento', 'direccion_viento', 'temperatura_aire', 'humedad', 'radiacion_solar', 'presion_atm', 'fecha_instrumento']]

        # Afegir el '.0' al final de cada valor a la columna 'fecha'
        merged_df['fecha'] = merged_df['fecha'].astype(str) + '.0'

        # Guardar l'arxiu final amb les columnes adequades
        merged_df.to_csv(nombre_meteo_final, index=False)
        print(f"Arxiu generat: {nombre_meteo_final}")


    else:
        print("No s'han trobat arxius per combinar. No hi ha meteo")



    # Descarregar els arxius per a cada data TERMOSAL
    for fecha in lista_fechas:
        try:
            url = f"http://161.111.139.31/datos/{vessel_mode}/{fecha[2:4]}-{fecha[4:8]}/termosal.proc/{fecha}.termosal.proc"
            local_path = os.path.join(carpeta_temp, f"{fecha}.termosal.csv")
            request.urlretrieve(url, local_path)
        except Exception as e:
            print(f"Error al descarregar arxiu {fecha}: {e}")

    # Processar els arxius descarregats
    archivos_termosal = [os.path.join(carpeta_temp, f) for f in os.listdir(carpeta_temp) if f.endswith(".csv")]
    dataframes = []

    # Llegir i emmagatzemar els arxius en DataFrame
    for archivo in archivos_termosal:
        try:
            df = pd.read_csv(archivo, sep=None, engine="python", header=None)
            dataframes.append(df)
        except Exception as e:
            print(f"Error al processar {archivo}: {e}")

    # Si hi ha arxius per combinar, procedim
    if dataframes:
        # Concatenar tots els DataFrames
        df_combinado = pd.concat(dataframes, ignore_index=True)

        # Eliminar les capçaleres repetides
        cabecera = df_combinado.iloc[0]  # Primera fila com a capçalera
        df_combinado = df_combinado[~df_combinado.apply(lambda x: x.equals(cabecera), axis=1)]  # Eliminar files que coincideixen amb la capçalera
        df_combinado.columns = cabecera  # Assignar les capçaleres correctes

        # Canviar el format de la columna 0 (data)
        df_combinado[df_combinado.columns[0]] = pd.to_datetime(df_combinado[df_combinado.columns[0]], format='%d-%m-%Y %H:%M:%S')

        # Ordenar per la columna de data (completa: any, mes, dia, hora, minut, segon)
        df_combinado = df_combinado.sort_values(by=df_combinado.columns[0], ascending=True)

        # Formatejar la data en el nou format AAAA-MM-DD hh:mm:ss.0
        df_combinado[df_combinado.columns[0]] = df_combinado[df_combinado.columns[0]].dt.strftime('%Y-%m-%d %H:%M:%S.0')

        # Guardar l'arxiu final
        nombre_termosal_final = f"29{vessel_code}{fecha_inicio.strftime('%Y%m%d')}_termosal.csv"
        df_combinado.to_csv(nombre_termosal_final, index=False)
        print(f"generant...: {nombre_termosal_final}")
        
        # Eliminar els arxius a la carpeta temp després de processar-los
        for archivo in os.listdir(carpeta_temp):
            archivo_path = os.path.join(carpeta_temp, archivo)
            
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)

        # Nom de l'arxiu de posició
        nombre_posicion = f"29{vessel_code}{fecha_inicio.strftime('%Y%m%d')}_posicion.csv"
        # Llegir els arxius de termosal i de posició
        termosal_df = pd.read_csv(nombre_termosal_final)  # Substitueix 'termosal.csv' pel nom del teu arxiu
        posicion_df = pd.read_csv(nombre_posicion)  # Substitueix 'posicion.csv' pel nom del teu arxiu de posicions

        # Netegem la columna 'fecha' per eliminar qualsevol text extra
        termosal_df['fecha'] = termosal_df['fecha'].str.replace(r'\.0$', '', regex=True)
        posicion_df['fecha'] = posicion_df['fecha'].str.replace(r'\.0$', '', regex=True)

        # Assegura't que les columnes de data i hora en ambdós arxius estiguin en format datetime
        termosal_df['datetime'] = pd.to_datetime(termosal_df['fecha'], format='%Y-%m-%d %H:%M:%S')
        posicion_df['datetime'] = pd.to_datetime(posicion_df['fecha'], format='%Y-%m-%d %H:%M:%S')

        # Realitzar la combinació per data i hora
        merged_df = pd.merge(termosal_df, posicion_df[['datetime', 'latitud', 'longitud']], 
                            on='datetime', how='left')

        # Eliminar la columna 'fecha' de termosal ja que anem a utilitzar 'datetime' com 'fecha'
        merged_df = merged_df.drop(columns=['fecha'])

        # Renombrar la columna 'datetime' a 'fecha'
        merged_df = merged_df.rename(columns={'datetime': 'fecha'})

        # Reordenar les columnes perquè 'fecha', 'longitud', 'latitud' siguin les primeres, seguides de les columnes de termosal
        merged_df = merged_df[['fecha', 'longitud', 'latitud','salinidad','temperatura','fluor','conductividad','sigmat','fecha_instrumento']]

        # Afegir el '.0' al final de cada valor a la columna 'fecha'
        merged_df['fecha'] = merged_df['fecha'].astype(str) + '.0'

        # Guardar l'arxiu final amb les columnes adequades
        merged_df.to_csv(nombre_termosal_final, index=False)
        print(f"Arxiu generat: {nombre_termosal_final}")

    else:
        print("No s'han trobat arxius per combinar. No hi ha termosal")
    
    destination_folder = "./static/data"
    try:
        shutil.move (nombre_meteo_final,destination_folder)
    except:
        print("no hi ha meteo")
    try: 
        shutil.move (nombre_termosal_final,destination_folder)
    except: 
        print("no hi ha ts")
    try:
        shutil.move (nombre_csv_final,destination_folder)
    except:
        print("no hi ha pos")

    zip_filename = "archivos_resultado.zip"
    zip_path = os.path.join(destination_folder, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
            try:
                zipf.write(os.path.join(destination_folder, nombre_meteo_final), nombre_meteo_final)
            except:
                print("no hi ha pos")
            try:
                zipf.write(os.path.join(destination_folder, nombre_termosal_final), nombre_termosal_final)
            except:
                print("no hi ha pos")
            try:
                zipf.write(os.path.join(destination_folder, nombre_csv_final), nombre_csv_final)
            except:
                print("no hi ha pos")

    try:
        os.remove(os.path.join(destination_folder, nombre_meteo_final))
    except: print ("no hi ha")
    try:
        os.remove(os.path.join(destination_folder, nombre_termosal_final))
        
    except: print ("no hi ha")
    try:
        os.remove(os.path.join(destination_folder, nombre_csv_final))
    except: print ("no hi ha")



if __name__ == '__main__':
    # Los argumentos pasados desde Flask
    vessel_input = sys.argv[1]
    date_inicial = sys.argv[2]
    date_final = sys.argv[3]

    main(vessel_input, date_inicial, date_final)
