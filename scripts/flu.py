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
 
            
def funcio_flu (cruise_id, cruise_name, date_inicial, date_final, vessel_input):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx',
      'xlink': 'http://www.w3.org/1999/xlink'
  }


    underway_general =cruise_id + "_underway.xml"

    underway_adcp =cruise_id + "/" + cruise_id + "_flu.xml"
    
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"
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

   
    shutil.copy(underway_general, underway_adcp)
    input_file= underway_adcp
    output_file= underway_adcp

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text = "urn:SDN:CDI:LOCAL:" + cruise_id + "_flu"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_flu"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text = "urn:SDN:CDI:LOCAL:" + cruise_id + "_flu"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " fluorometer data"
    tree.write(output_file)


    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Fluorometry data acquired on board the R/V "+ vessel + " during the "+cruise_name+" cruise."
    tree.write(output_file)

    #canviar paràmetres
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Raw fluorometer output'
    posList_1.set ("codeListValue","FVLT")
   
    tree.write(output_file)


    #canviar intruments ( de unknown al meteorological data)
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'fluorometers'
    posList_1.set ("codeListValue","113")
    tree.write(output_file)

