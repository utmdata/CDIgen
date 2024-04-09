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
  arxiu = arxiu.reindex(columns=["longitude", "latitude", "time", "date", "id", "codi", "cruise_id","Instrument","Coments"])
  arxiu = arxiu.to_csv(csv_name,header=True, index=False)


def funcio_xbt (cruise_id, cruise_name, vessel_input, ruta_csv):
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

    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org'
  }
    cdi_individual =cruise_id + "_cdi.xml"

    cdi_xbt =cruise_id + "/" + cruise_id + "_xbt.xml"

    if vessel_input == "sdg":
      vessel_mode = "Sarmiento"
      vessel_reduit='sdg' 
      vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
      vessel_mode ="Hesperides"
      vessel_reduit="hes"
      vessel = "Hespérides"

    header_list=['longitude', 'latitude', 'End_lat', 'End_long', 'First_time', 'End_time','Instrument', 'Coments']
    samples_and_stations = pd.read_csv(ruta_csv, names = header_list)
    samples = pd.DataFrame(samples_and_stations)

    shutil.copy(cdi_individual, cdi_xbt)
    input_file= cdi_xbt
    output_file= cdi_xbt

    select_instrument = "XBT"
    select_instrument=str(select_instrument)
    instrument = samples.loc[samples['Instrument'] == select_instrument]
    instrument.to_csv("static/csv/samples.csv", index=False)
    cdi_model = "_xbt"
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
      xbt_text = " XBT "

      name2= cruise_name  + xbt_text + name + " data"
      fila=fila+1
      lista_name.append(name2)
    samples['name'] = lista_name

    for i in range(0,total_lines):

      name=str(samples.loc [i,"index"])
      name = name.zfill(2) #fem que el nom sigui de 2 digits i ho ompli amb 0 a la esquerre

      name3= "Water column data launched on board the R/V "+ vessel +" during the " + cruise_name +" cruise."
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
      dia = fecha.split("-")[0]
      mes= fecha.split("-")[1]
      any= fecha.split("-")[2]
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


    csv_name= cdi_xbt + cruise_id + cdi_model + ".csv"
    samples.to_csv(csv_name, header=True, index=False)
    #Primer fer un model de CDI amb les organitzacions i la pestanya CRUISE/STATION
    for i in samples.index:
        folder_copy= cdi_xbt+ samples["id"][i] + ".txt"
        shutil.copy(cdi_xbt,folder_copy)
        contenido = open(folder_copy, "r",encoding='UTF-8').read()
        contenido = contenido.replace("new_ID",samples["id"][i])
        contenido = contenido.replace("new_NAME",samples["name"][i])
        contenido = contenido.replace(str("90.00"),str(samples["latitude"][i]))
        contenido = contenido.replace(str("180.00"),str(samples["longitude"][i]))
        contenido = contenido.replace(str("2022-03-15T13:12:00"),str(samples["date_time"][i]))
        
        
        
        contenido = contenido.replace("new_ABSTRACT",samples["abstract"][i])

        nombre_archivo = cdi_xbt+ samples["id"][i] + ".xml"
        with open(folder_copy, "w",encoding='UTF-8') as archivo:
              archivo.write(contenido)
              archivo.close()
              os.rename(folder_copy, nombre_archivo )

    print("CDIs guardats a la carpeta XBT. Recorda guardar-los a la carpeta CDI corresponent i eliminarlos de la carpeta compartida")
    eliminar_columnes(csv_name)
    os.remove ("static/csv/samples.csv")
    







    """#afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text = cruise_id + "_ctd"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_ctd"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text = cruise_id + "_ctd"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " CTD data"
    tree.write(output_file)

    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Water column data acquired on board the R/V "+ vessel + " with a SeaBird SBE911 plus CTD during the "+cruise_name+" cruise."
    tree.write(output_file)


    #canviar paràmetres
    num_parametres = 9
    for _ in range(num_parametres):
        tree = etree.parse(input_file)
        root = tree.getroot()
        element_to_copy = root.find(".//sdn:SDN_ParameterDiscoveryCode", namespaces=namespace)
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
    #mirar si es poden treure els números
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Salinity of the water column'
    posList_1.set ("codeListValue","PSAL")
    posList_2 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_2.text =  'Temperature of the water column'
    posList_2.set ("codeListValue","TEMP")
    posList_3 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_3.text=  'Electrical conductivity of the water column'
    posList_3.set ("codeListValue","CNDC")
    posList_4 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_4.text =  'Transmittance and attenuance of the water column'
    posList_4.set ("codeListValue","ATTN")
    posList_5 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_5.text =  'Dissolved oxygen parameters in the water column'
    posList_5.set ("codeListValue","DOXY")
    tree.write(output_file)
    tree = etree.parse(input_file)
    #mirar si es poden treure els números
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Density of the water column'
    posList_1.set ("codeListValue","SIGT")
    posList_2 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_2.text =  'Chlorophyll pigment concentrations in water bodies'
    posList_2.set ("codeListValue","CPWC")
    posList_3 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_3.text=  'Visible waveband radiance and irradiance measurements in the water column'
    posList_3.set ("codeListValue","VSRW")
    posList_4 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_4.text =  'Vertical spatial coordinates'
    posList_4.set ("codeListValue","AHGT")

    tree.write(output_file)

    #canviar instruments
    num_parametres = 8
    for _ in range(num_parametres-1):
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
    posList_1.text =  'CTD'
    posList_1.set ("codeListValue","130")
    posList_2 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_2.text =  'fluorometers'
    posList_2.set ("codeListValue","113")
    tree.write(output_file)
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'dissolved gas sensors'
    posList_1.set ("codeListValue","351")
    posList_2 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_2.text =  'salinity sensor'
    posList_2.set ("codeListValue","350")
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'water temperature sensor'
    posList_1.set ("codeListValue","134")
    posList_2 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_2.text =  'transmissometers'
    posList_2.set ("codeListValue","124")
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'radiometers'
    posList_1.set ("codeListValue","122")
    posList_2 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_2.text =  'altimeters'
    posList_2.set ("codeListValue","379")
    tree.write(output_file)

    #canviar sensor segons el vaixell
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Sea-Bird SBE 911plus CTD'
    posList_1.set ("codeListValue","TOOL0058")
    tree.write(output_file)

    
    print("S'ha guardat l'arxiu ctd")


    url= "http://www.utm.csic.es/metadata/"+ vessel_mode + "/generated/"+ cruise_id +"/cdi/"+ cruise_id + "_samples_and_stations_with_pos.csv"
    header_list=['First_lat', 'First_long', 'End_lat', 'End_long', 'First_time', 'End_time','Instrument', 'Coments']
    samples_and_stations = pd.read_csv(url, names = header_list)
    print("Information obtained from the following link:")
    print(" ")
    print(url)

    samples = pd.DataFrame(samples_and_stations)
    #list of CDIs that have been made in the campaign
    instrument_list = samples["Instrument"].unique().tolist()
    print(" ")
    print("The CDIs available in the following campaign are:")
    print(" ")
    print(instrument_list)"""
