
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


def funcio_sbe (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org'
  }
  
    underway_general =cruise_id + "_underway.xml"
    underway_sbe = cruise_id + "/" + cruise_id + "_sbe.xml"
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"

    shutil.copy(underway_general, underway_sbe)
    input_file= underway_sbe
    output_file= underway_sbe

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text = "urn:SDN:CDI:LOCAL:" + cruise_id + "_sbe"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_sbe"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text = "urn:SDN:CDI:LOCAL:" + cruise_id + "_sbe"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " singlebeam data"
    tree.write(output_file)

    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Singlebeam data acquired on board the R/V "+ vessel + " with a Kongsberg EA 600 echosounder during the "+cruise_name+" cruise."
    tree.write(output_file)

    #canviar paràmetres
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Bathymetry and Elevation'
    posList_1.set ("codeListValue","MBAN")
    tree.write(output_file)

    #canviar intruments ( de unknown al meteorological data)
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'single-beam echosounder'
    posList_1.set ("codeListValue","156")
    tree.write(output_file)


    #canviar sensor segons el vaixell
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Kongsberg (Simrad) EA600 Echosounder'
    posList_1.set ("codeListValue","TOOL0319")
    tree.write(output_file)
    print("S'ha guardat l'arxiu sbe")
