import pandas as pd
import glob
from datetime import datetime
import numpy as np
import shutil
import os,sys
from os import remove
from os import path
from datetime import datetime
import requests, argparse
from lxml import etree
import copy

#Definim el namespace perquè el trobi en el XML

def eliminar_columnes(csv_name):
  arxiu = pd.read_csv(csv_name)
<<<<<<< HEAD
  arxiu = arxiu.reindex(columns=["cruise_id","longitude", "latitude","Instrument", "instrument","vessel", "id", "met_cat"])
  arxiu = arxiu.rename (columns={'longitude': 'lon', 'latitude': 'lat', 'Instrument': 'instrument_id','cruise_id': 'cruiseid','id': 'cdiid'})
=======
  arxiu = arxiu.reindex(columns=["cruise_id","latitude", "longitude","Instrument", "instrument","vessel", "id", "met_cat" ,"Coments"])
  arxiu = arxiu.rename (columns={'latitude': 'lat', 'longitude': 'lon', 'Instrument': 'instrument_id','cruise_id': 'cruiseid','id': 'codiid'})
>>>>>>> main
  arxiu = arxiu.to_csv(csv_name,header=True, index=False)


def funcio_moc (cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final):
    cdi_model = "_moc"
    
    fila=0
    lista_id=[]
    lista_name=[]
    lista_abstract=[]
    lista_fecha=[]
    lista_hora =[]
    lista_hora_1=[]
    lista_min =[]
    lista_time=[]
    lista_fecha_final=[]
    lista_dia=[]
    lista_mes=[]
    lista_any=[]
    lista_date=[]
    lista_time=[]
    lista_date_final=[]
    lista_codi=[]
    lista_cruise_id=[]
    lista_vessel=[]
    lista_met_cat=[]

    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org'
  }
    cdi_individual =cruise_id + "_cdi.xml"
    input_file= cdi_individual
    output_file= cdi_individual

    #canviar paràmetres
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Microzooplankton taxonomic abundance in water bodies'
    posList_1.set ("codeListValue","MATX")
    

    tree.write(output_file)

    #canviar intruments ( de unknown al meteorological data)
    num_instruments = 2
    for _ in range(num_instruments-1):
        tree = etree.parse(input_file)
        root = tree.getroot()
        element_to_copy = root.find(".//sdn:SDN_DeviceCategoryCode", namespaces=namespace)
        # Crear una copia del elemento y su elemento padre
        copied_element = element_to_copy.makeelement(element_to_copy.tag, element_to_copy.attrib, nsmap=namespace)
        copied_element.text = element_to_copy.text
        parent_element = element_to_copy.getparent()
        copied_parent_element = parent_element.makeelement(parent_element.tag, parent_element.attrib, nsmap=namespace)
        # Agregar la copia del elemento en el elemento padre copiado
        copied_parent_element.append(copied_element)
        # Reemplazar el elemento original con el elemento padre copiado en el árbol XML
        parent_element.getparent().append(copied_parent_element)
        tree.write(output_file, xml_declaration=True, encoding="utf-8",method="xml")
    
    tree = etree.parse(input_file)    
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'multinet'
    posList_1.set ("codeListValue","68")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'CTD'
    posList_1.set ("codeListValue","130")

    tree.write(output_file)


    #canviar sensor segons el vaixell
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Sea-Bird SBE 19 SEACAT CTD'
    posList_1.set ("codeListValue","TOOL0042")
    tree.write(output_file)

    cdi_global=cruise_id + "/" + cruise_id + "_moc.xml"
    shutil.copy (cdi_individual,cdi_global)
    
    
    if vessel_input == "sdg":
      vessel_mode = "Sarmiento"
      vessel_reduit='sdg' 
      vessel = "Sarmiento de Gamboa"
      vessel_mayus = "SARMIENTO DE GAMBOA"
    elif vessel_input == "hes":
      vessel_mode ="Hesperides"
      vessel_reduit="hes"
      vessel = "Hespérides"
      vessel_mayus = "HESPERIDES"
<<<<<<< HEAD
    elif vessel_input == "odb":
      vessel = "Odón de Buen"
      vessel_mode = "Odón"
      vessel_reduit = "odb"
      vessel_mayus = "ODON DE BUEN"
      vessel_code = "29OD"
    elif vessel_input == "gdc":
      vessel = "García del Cid"
      vessel_mode = "García"
      vessel_reduit = "gdc"
      vessel_mayus = "GARCÍA DEL CID"
      vessel_code = "29GD"  
=======
    
>>>>>>> main



    header_list=['longitude', 'latitude', 'End_lat', 'End_long', 'First_time', 'End_time','Instrument', 'Coments']
    samples_and_stations = pd.read_csv(ruta_csv, names = header_list)
    samples = pd.DataFrame(samples_and_stations)

    if path.exists(cruise_id + "_moc.txt"):
      remove(cruise_id + "_moc.txt")

    #canviar segons el cdi:   

<<<<<<< HEAD
    select_instrument = "MOCNESS"
=======
    select_instrument = "MOC"
>>>>>>> main

    shutil.copy(cdi_individual, "static/csv/cdi_model_1.xml")
    filename = "cdi_model_1.xml"
    folder ="static/csv/"
    infilename = os.path.join(folder,filename)
    newname = infilename.replace('cdi_model_1.xml', 'cdi_model.txt')
    output = os.rename(infilename, newname)

    
    select_instrument=str(select_instrument)
    instrument = samples.loc[samples['Instrument'] == select_instrument]
    instrument.to_csv("static/csv/samples.csv", index=False)

    
    cdi_model = "_moc" #canviar  
    samples = pd.read_csv("static/csv/samples.csv")
    samples.index = np.arange(1, len(samples) + 1) # que els index comencin per 1 no per 0
    samples = samples.rename_axis('index').reset_index()
    samples.set_index('index')
    total_lines=len(samples.axes[0])
    for i in range(0,total_lines):    
      id=str(samples.loc [i,"index"])
      id2= cruise_id
      fila=fila+1
      lista_cruise_id.append(id2)
    samples['cruise_id'] = lista_cruise_id

    for i in range(0,total_lines):    
      
      id= '<a href="http://data.utm.csic.es/geonetwork/srv/eng/catalog.search#/metadata/urn:SDN:CDI:LOCAL:' + cruise_id + cdi_model + '"  target="_blank">View in metadata catalog</a>' 
      
      lista_met_cat.append(id)
    samples['met_cat'] = lista_met_cat
<<<<<<< HEAD
    
    lista_instrument=[]
    for i in range(0,total_lines):    
      instrument= 'Mocness'
      lista_instrument.append(instrument)
    samples['instrument'] = lista_instrument
=======

>>>>>>> main

#<a href="http://data.utm.csic.es/geonetwork/srv/eng/catalog.search#/metadata/urn:SDN:CDI:LOCAL:29SG20230719_ctd_ros_ladcp"  target="_blank">View in metadata catalog</a>
    for i in range(0,total_lines):    
      lista_vessel.append(vessel_mayus)
    samples['vessel'] = lista_vessel

    for i in range(0,total_lines):
      id=str(samples.loc [i,"index"])
      id = id.zfill(2) #fem que el id sigui de 2 digits i ho ompli amb 0 a la esquerre
      afegir=cdi_model
      id2= afegir + "_" + id
      id2= id2[1:]
      fila=fila+1
      lista_codi.append(id2)
    samples['codi'] = lista_codi

    for i in range(0,total_lines):
      name=str(samples.loc [i,"index"])
      name = name.zfill(2) #fem que el nom sigui de 2 digits i ho ompli amb 0 a la esquerre
      text = " MOC "  #canviar  

      name2= cruise_name  + text + name + " data"  
      fila=fila+1
      lista_name.append(name2)
    samples['name'] = lista_name

    for i in range(0,total_lines):

      name=str(samples.loc [i,"index"])
      name = name.zfill(2) #fem que el nom sigui de 2 digits i ho ompli amb 0 a la esquerre

      name3= "Data from biological samples acquired on board the R/V  "+ vessel +" during the " + cruise_name +" cruise." #canviar  
      fila=fila+1
      lista_abstract.append(name3)
    samples['abstract'] = lista_abstract


    for i in range(0,total_lines):
        id=str(samples.loc [i,"index"])
        id = id.zfill(2) #fem que el id sigui de 2 digits i ho ompli amb 0 a la esquerre
        afegir=cdi_model
        id2= cruise_id+afegir + "_" + id
        fila=fila+1
        lista_id.append(id2)
    samples['id'] = lista_id

    samples["csr_name"] = cruise_name
    for i in range(0,total_lines):
      fecha=str(samples.loc [i,"First_time"])
      fecha_corta = fecha.split(" ")[0]
      hora= fecha.split(" ")[1]
      fila=fila+1
      hora_1= hora.split(":")[0]
      min= hora.split(":")[1]
      lista_fecha.append(fecha_corta)
      lista_hora.append (hora)
      lista_hora_1.append (hora_1)
      lista_min.append (min)

    samples['fecha'] = lista_fecha
    samples['hora'] = lista_hora
    samples['hora_1'] = lista_hora_1
    samples['min'] = lista_min

    for i in range(0,total_lines):
      fecha_hora=str(samples.loc [i,"hora_1"])
      fecha_min=str(samples.loc [i,"min"])
      time = fecha_hora +":" + fecha_min + ":00"
      lista_time.append(time)
    samples["time"] = lista_time

    for i in range(0,total_lines):
      fecha=str(samples.loc [i,"fecha"])
<<<<<<< HEAD
      any = fecha.split("-")[0]
      mes= fecha.split("-")[1]
      dia= fecha.split("-")[2]
=======
      dia = fecha.split("-")[0]
      mes= fecha.split("-")[1]
      any= fecha.split("-")[2]
>>>>>>> main
      fila=fila+1
      lista_dia.append(dia)
      lista_mes.append(mes)
      lista_any.append (any)

    samples['dia'] = lista_dia
    samples['mes'] = lista_mes
    samples['any'] = lista_any

    for i in range(0,total_lines):
      fecha_dia=str(samples.loc [i,"dia"])
      fecha_mes=str(samples.loc [i,"mes"])
      fecha_any=str(samples.loc [i,"any"])
      date = fecha_any + "-" + fecha_mes + "-"+ fecha_dia
      fila=fila+1
      lista_date.append(date)
    samples["date"] = lista_date

    for i in range(0,total_lines):
        date=str(samples.loc [i,"date"])
        time=str(samples.loc [i,"time"])
        fila=fila+1
        fecha_final = date + "T"+ time

        lista_date_final.append(fecha_final)
    samples["date_time"] = lista_date_final


    csv_name= cruise_id  + "/" + cruise_id + cdi_model + ".csv"
    samples.to_csv(csv_name, header=True, index=False)
    #Primer fer un model de CDI amb les organitzacions i la pestanya CRUISE/STATION
    for i in samples.index:
        folder_copy= "static/csv/"+ samples["id"][i] + ".txt"
        shutil.copy("static/csv/cdi_model.txt",folder_copy)
        contenido = open(folder_copy, "r",encoding='UTF-8').read()
        contenido = contenido.replace("new_ID",samples["id"][i])
        contenido = contenido.replace("new_NAME",samples["name"][i])
        contenido = contenido.replace(str("90.00"),str(samples["latitude"][i]))
        contenido = contenido.replace(str("20.00"),str(samples["latitude"][i]))
        contenido = contenido.replace(str("80.00"),str(samples["longitude"][i]))
        contenido = contenido.replace(str("10.00"),str(samples["longitude"][i]))
        contenido = contenido.replace(str("2022-03-15T13:12:00"),str(samples["date_time"][i]))
        contenido = contenido.replace("new_ABSTRACT",samples["abstract"][i])
        nombre_archivo = cruise_id + "/" + samples["id"][i] + ".xml"
        with open(folder_copy, "w",encoding='UTF-8') as archivo:
              archivo.write(contenido)
              archivo.close()
              os.rename(folder_copy, nombre_archivo )

  #fem el cdi global
  
    #afegim BOUNDING BOX
    url_bbox = "http://datahub.utm.csic.es/ws/getBBox/?id="+vessel_reduit + cruise_id[4:12]
    print (url_bbox)
    tree = etree.parse(cdi_global)
<<<<<<< HEAD
    try:
      r = requests.get(url_bbox)
      r.raise_for_status()
      raw_bbox = r.text.strip()

      if raw_bbox.upper().startswith("BOX(") and raw_bbox.endswith(")"):
        bbox_text = raw_bbox[4:-1]
      elif "," in raw_bbox and " " in raw_bbox:
        bbox_text = raw_bbox
      else:
        raise ValueError(f"Unexpected bbox format: {raw_bbox!r}")

      pair_1, pair_2 = [p.strip() for p in bbox_text.split(",", 1)]
      w, s = pair_1.split()
      e, n = pair_2.split()

      posList_w = tree.xpath("//gco:Decimal[contains(text(), '80.00')]", namespaces=namespace)
      posList_e = tree.xpath("//gco:Decimal[contains(text(), '10.00')]", namespaces=namespace)
      posList_s = tree.xpath("//gco:Decimal[contains(text(), '90.00')]", namespaces=namespace)
      posList_n = tree.xpath("//gco:Decimal[contains(text(), '20.00')]", namespaces=namespace)

      if posList_w and posList_e and posList_s and posList_n:
        posList_w[0].text = w
        posList_e[0].text = e
        posList_s[0].text = s
        posList_n[0].text = n
        tree.write(cdi_global)
      else:
        print("Warning: Could not find gco:Decimal bbox placeholders in XML")

    except Exception as err:
      print(f"Warning: could not get/update bbox from {url_bbox}: {err}")
=======
    r = requests.get(url_bbox)
    coord= r.text[4:-2] #nomes coordenades 4separades per espais i comes
    posicio_primer_espai= r.text[4:-2].index(" ")
    posicio_coma= r.text[4:-2].index(",")
    w= coord[0:posicio_primer_espai]
    s= coord[posicio_primer_espai:posicio_coma].strip()
    coord_2=coord[posicio_coma:]
    coord_2= coord_2[1:]
    posicio_segon_espai= coord_2.index(" ")
    e= coord_2[0:posicio_segon_espai].strip()
    n= coord_2[posicio_segon_espai:].strip()

    posList_w= tree.xpath("//gco:Decimal[contains(text(), '80.00')]", namespaces=namespace)[0]
    posList_w.text=w
    posList_s = tree.xpath("//gco:Decimal[contains(text(), '10.00')]", namespaces=namespace)[0]
    posList_s.text= s
    posList_e = tree.xpath("//gco:Decimal[contains(text(), '90.00')]", namespaces=namespace)[0]
    posList_e.text= e
    posList_n = tree.xpath("//gco:Decimal[contains(text(), '20.00')]", namespaces=namespace)[0]
    posList_n.text=n

    tree.write(cdi_global)
>>>>>>> main

  #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(cdi_global)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
<<<<<<< HEAD
    posList.text ="urn:SDN:CDI:LOCAL:" + cruise_id + cdi_model
=======
    posList.text = cruise_id + cdi_model
>>>>>>> main
    tree.write(cdi_global)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + cdi_model
    tree.write(cdi_global)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
<<<<<<< HEAD
    posList.text ="urn:SDN:CDI:LOCAL:" + cruise_id + cdi_model
=======
    posList.text = cruise_id + cdi_model
>>>>>>> main
    tree.write(cdi_global)

    #afegir dataset name
    tree = etree.parse(cdi_global)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " mocness data"
    tree.write(cdi_global)

    #afegir ABSTRACT
    tree = etree.parse(cdi_global)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Data from " + str(total_lines) +" biological samples acquired on board the R/V" +vessel +" during the " + cruise_name +" cruise."
    tree.write(cdi_global)
    print(total_lines)

    dia= cruise_id[10:12]
    mes=cruise_id[8:10]
    any=cruise_id[4:8]

 
  #afegim data inicial
<<<<<<< HEAD
    # Normalize date_inicial: accepts DD/MM/YYYY HH:MM:SS or YYYY-MM-DD (with optional time)
    try:
        if "/" in date_inicial:
            dt_inicial = datetime.strptime(date_inicial.strip(), "%d/%m/%Y %H:%M:%S")
        elif "T" in date_inicial:
            dt_inicial = datetime.strptime(date_inicial.strip(), "%Y-%m-%dT%H:%M:%S")
        else:
            dt_inicial = datetime.strptime(date_inicial.strip()[:10], "%Y-%m-%d")
    except ValueError:
        dt_inicial = datetime.strptime(any + "-" + mes + "-" + dia, "%Y-%m-%d")
    begin_position = dt_inicial.strftime("%Y-%m-%dT%H:%M:%S")
=======
    hora_inicial = date_inicial[11:]
    begin_position = any + "-"+ mes + "-" + dia + "T" + hora_inicial
>>>>>>> main

    tree = etree.parse(cdi_global)
    posList = tree.xpath("//gml:beginPosition[contains(text(), '2022-03-15T13:12:00')]", namespaces=namespace)[0]
    posList.text = begin_position
    tree.write(cdi_global)

    #afegim data final
<<<<<<< HEAD
    # Normalize date_final: accepts DD/MM/YYYY HH:MM:SS or YYYY-MM-DD (with optional time)
    try:
        if "/" in date_final:
            dt_final = datetime.strptime(date_final.strip(), "%d/%m/%Y %H:%M:%S")
        elif "T" in date_final:
            dt_final = datetime.strptime(date_final.strip(), "%Y-%m-%dT%H:%M:%S")
        else:
            dt_final = datetime.strptime(date_final.strip()[:10], "%Y-%m-%d")
    except ValueError:
        dt_final = datetime.strptime(date_final.strip()[:10], "%Y-%m-%d")
    final_position = dt_final.strftime("%Y-%m-%dT%H:%M:%S")

=======
    hora_final = date_final[11:]
    data_final = date_final[:10]
    dia_final= data_final[0:2]
    mes_final=data_final[3:5]
    any_final=data_final[6:10]

    final_position = any_final + "-"+ mes_final + "-" + dia_final + "T" + hora_final
>>>>>>> main
    tree = etree.parse(cdi_global)
    posList = tree.xpath("//gml:endPosition[contains(text(), '2022-03-15T13:12:00')]", namespaces=namespace)[0]
    posList.text = final_position
    tree.write(cdi_global)

    eliminar_columnes(csv_name)
    os.remove ("static/csv/samples.csv")
    os.remove (cruise_id + "_cdi.xml")
    os.remove ("static/csv/cdi_model.txt")
