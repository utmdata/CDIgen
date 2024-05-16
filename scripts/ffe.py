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
 
            
def funcio_ffe (cruise_id, cruise_name, date_inicial, date_final, vessel_input):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx',
      'xlink': 'http://www.w3.org/1999/xlink'
  }


    underway_general =cruise_id + "_underway.xml"

    underway_ffe =cruise_id + "/" + cruise_id + "_ffe.xml"
    
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"

   
    shutil.copy(underway_general, underway_ffe)
    input_file= underway_ffe
    output_file= underway_ffe

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text = cruise_id + "_ffe"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_ffe"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text = cruise_id + "_ffe"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " biomass data"
    tree.write(output_file)

    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Biomass data acquired on board the R/V "+ vessel + " with a Kongsberg EK 60 biological echosounder during the "+cruise_name+" cruise."
    tree.write(output_file)

    #canviar paràmetres
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Fish biomass in water bodies'
    posList_1.set ("codeListValue","FIBM")
   
    tree.write(output_file)


    #canviar intruments ( de unknown al meteorological data)
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Fish-finder echosounders'
    posList_1.set ("codeListValue","FFES")
    tree.write(output_file)
    #no canviem el sensor pq no existeix la Kongsberg EK 60 biological echosounder
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
    posList_1.text =  'XYZ ASCII'
    posList_1.set ("codeListValue","XYZ")
    tree.write(output_file)    #canviar versio del data format
    tree = etree.parse(input_file)
    posList_1 = tree.xpath(".//gco:CharacterString[contains(text(), '0.4')]", namespaces=namespace)[0]
    posList_1.text =  '1'
    tree.write(output_file)
