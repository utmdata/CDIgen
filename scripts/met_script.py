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
 
            
def funcio_met (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org'
  }


    underway_general =cruise_id + "_underway.xml"

    underway_met =cruise_id + "/" + cruise_id + "_met.xml"
    
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"

   
    shutil.copy(underway_general, underway_met)
    input_file= underway_met
    output_file= underway_met

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text ="urn:SDN:CDI:LOCAL:" + cruise_id + "_met"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_met"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text = "urn:SDN:CDI:LOCAL:" + cruise_id + "_met"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " meteorological data"
    tree.write(output_file)

    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Meteorological data acquired on board the R/V "+ vessel + " with a Campbell CR 1000 Station in continuous mode during the "+cruise_name+" cruise."
    tree.write(output_file)

    #canviar paràmetres
    num_parametres = 4
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
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Air temperature'
    posList_1.set ("codeListValue","CDTA")
    posList_2 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_2.text =  'Air pressure'
    posList_2.set ("codeListValue","CAPH")
    posList_3 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_3.text=  'Atmospheric humidity'
    posList_3.set ("codeListValue","CHUM")
    posList_4 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_4.text =  'Solar Radiation'
    posList_4.set ("codeListValue","CSLR")
    posList_5 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_5.text =  'Wind strength and direction'
    posList_5.set ("codeListValue","EWSB")
    tree.write(output_file)

    #canviar intruments ( de unknown al meteorological data)
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'meteorological packages'
    posList_1.set ("codeListValue","102")
    tree.write(output_file)


    #canviar sensor segons el vaixell
    if vessel_input == "sdg":
        #tree = etree.parse(input_file)
        num_sensor = 5 #li hem restat un pq sino surt un unknown
        for _ in range(num_sensor):
            tree = etree.parse(input_file)
            root = tree.getroot()
            element_to_copy = root.find(".//sdn:SDN_SeaVoxDeviceCatalogueCode", namespaces=namespace)
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
        posList_1 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_1.text =  'Campbell Scientific CR1000 data logger'
        posList_1.set ("codeListValue","TOOL1541")
        posList_2 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_2.text =  'Vaisala HMP temperature and humidity sensor'
        posList_2.set ("codeListValue","TOOL0081")
        posList_3 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_3.text =  'Young MA05106 Wind Monitor anemometer'
        posList_3.set ("codeListValue","TOOL0195")
        posList_4 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_4.text =  'Young 61302 barometric pressure sensor'
        posList_4.set ("codeListValue","TOOL1001")
        posList_5 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_5.text =  'LI-COR LI-200R pyranometer'
        posList_5.set ("codeListValue","TOOL1770")
        posList_6 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_6.text =  'LI-COR LI-190 PAR sensor'
        posList_6.set ("codeListValue","TOOL0193")
        tree.write(output_file)
        print("S'ha guardat l'arxiu met")

    elif vessel_input == "hes":
        tree = etree.parse(input_file)
        num_sensor = 4
        for _ in range(num_sensor-1):
            tree = etree.parse(input_file)
            root = tree.getroot()
            element_to_copy = root.find(".//sdn:SDN_SeaVoxDeviceCatalogueCode", namespaces=namespace)
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
        posList_1 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_1.text =  'Campbell Scientific CR1000 data logger'
        posList_1.set ("codeListValue","TOOL1541")
        posList_2 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_2.text =  'Vaisala HMP 155 hygrometer series'
        posList_2.set ("codeListValue","TOOL1673")
        posList_3 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_3.text =  'Campbell Scientific MetSENS200 ultrasonic anemometer'
        posList_3.set ("codeListValue","TOOL1924")
        posList_4 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
        posList_4.text =  'Setra 278 barometer'
        posList_4.set ("codeListValue","TOOL1923")
        tree.write(output_file)
        print("S'ha guardat l'arxiu met")