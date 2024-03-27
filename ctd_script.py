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

        
def funcio_ctd (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org'
  }
    cdi_general =cruise_id + "_cdi.xml"

    cdi_ctd =cruise_id + "/" + cruise_id + "_ctd.xml"

    if vessel_input == "sdg":
      vessel_mode = "Sarmiento"
      vessel_reduit='sdg' 
      vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
      vessel_mode ="Hesperides"
      vessel_reduit="hes"
      vessel = "Hespérides"

    shutil.copy(cdi_general, cdi_ctd)
    input_file= cdi_ctd
    output_file= cdi_ctd

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
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
    print(instrument_list)
