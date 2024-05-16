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
 
            
def funcio_srs (cruise_id, cruise_name, date_inicial, date_final, vessel_input):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx',
      'xlink': 'http://www.w3.org/1999/xlink'
  }


    underway_general =cruise_id + "_underway.xml"

    underway_srs =cruise_id + "/" + cruise_id + "_srs.xml"
    
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"

   
    shutil.copy(underway_general, underway_srs)
    input_file= underway_srs
    output_file= underway_srs

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text ="urn:SDN:CDI:LOCAL:" +  cruise_id + "_srs"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text ="urn:SDN:CDI:LOCAL:" +  cruise_id + "_srs"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text = "urn:SDN:CDI:LOCAL:" + cruise_id + "_srs"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " seismic refraction data"
    tree.write(output_file)

    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Seismic refraction data acquired on board the R/V "+ vessel + " during the "+cruise_name+" cruise."
    tree.write(output_file)

    #canviar paràmetres
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Seismic refraction'
    posList_1.set ("codeListValue","SRFR")
   
    tree.write(output_file)
    
    #canviar INSTRUMENTS
    num_parametres = 3
    for _ in range(num_parametres):
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
    posList_1.text =  'seismic refraction systems'
    posList_1.set ("codeListValue","155")
    posList_2 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_2.text =  'seismometers'
    posList_2.set ("codeListValue","368")
    posList_3 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_3.text=  'airgun array'
    posList_3.set ("codeListValue","ARAG")
    tree.write(output_file)

    #no canviem el sensor pq no existeix
    """#canviar sensor
    tree = etree.parse(input_file)
    posList_1 = tree.xpath(".//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Teledyne RDI Ocean Surveyor 75kHz vessel-mounted ADCP'
    posList_1.set ("codeListValue","TOOL0362")
    tree.write(output_file)"""

    #canviar llicencia
    tree = etree.parse(input_file)
    posList_1 = tree.xpath(".//gmx:Anchor[contains(text(), 'Creative Commons Attribution 4.0 International')]", namespaces=namespace)[0]
    posList_1.text =  'by negotiation'
    posList_1.set("{http://www.w3.org/1999/xlink}href","https://www.seadatanet.org/urnurl/SDN:L08::RS") 
    tree.write(output_file,encoding='utf-8', xml_declaration=True)

    #canviar data format
    tree = etree.parse(input_file)
    posList_1 = tree.xpath(".//sdn:SDN_FormatNameCode[contains(text(), 'Ocean Data View ASCII input')]", namespaces=namespace)[0]
    posList_1.text =  'Society of Exploration Geophysicists SEG Y'
    posList_1.set ("codeListValue","SEGY")
    tree.write(output_file)    #canviar versio del data format
    tree = etree.parse(input_file)
    posList_1 = tree.xpath(".//gco:CharacterString[contains(text(), '0.4')]", namespaces=namespace)[0]
    posList_1.text =  '1'
    tree.write(output_file)
