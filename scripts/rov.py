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
 
            
def funcio_rov (cruise_id, cruise_name, date_inicial, date_final, vessel_input):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx',
      'xlink': 'http://www.w3.org/1999/xlink'
  }


    underway_general =cruise_id + "_underway.xml"

    underway_rov =cruise_id + "/" + cruise_id + "_rov-MODIFICAR_ABSTRACT_PARAMETRES.xml"
    
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"

   
    shutil.copy(underway_general, underway_rov)
    input_file= underway_rov
    output_file= underway_rov

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text ="urn:SDN:CDI:LOCAL:" +  cruise_id + "_rov"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_rov"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text ="urn:SDN:CDI:LOCAL:" +  cruise_id + "_rov"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " ROV data"
    tree.write(output_file)

    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "ROV dive data from INSERT ROV acquired during the " +cruise_name+" cruise on board the R/V " + vessel + "."
    tree.write(output_file)

        #canviar paràmetres
    num_parametres = 11
    for _ in range(num_parametres-1):
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
    posList_1.text =  'Salinity of the water column'
    posList_1.set ("codeListValue","PSAL")
    posList_2 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_2.text =  'Temperature of the water column'
    posList_2.set ("codeListValue","TEMP")
    posList= tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList.text =  'Electrical conductivity of the water column'
    posList.set ("codeListValue","CNDC")
    posList= tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList.text =  'Transmittance and attenuance of the water column'
    posList.set ("codeListValue","ATTN")
    posList= tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList.text =  'Dissolved oxygen parameters in the water column'
    posList.set ("codeListValue","DOXY")
    posList= tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList.text =  'Density of the water column'
    posList.set ("codeListValue","SIGT")    
    posList= tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList.text =  'Chlorophyll pigment concentrations in water bodies'
    posList.set ("codeListValue","CPWC")
    posList= tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList.text =  'Visible waveband radiance and irradiance measurements in the water column'
    posList.set ("codeListValue","VSRW")
    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Horizontal velocity of the water column (currents)'
    posList_1.set ("codeListValue","RFVL")

    posList_2 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_2.text =  'Vertical velocity of the water column (currents)'
    posList_2.set ("codeListValue","LRZA")

    posList_1 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_1.text =  'Seabed photography'
    posList_1.set ("codeListValue","SBPH")

    tree.write(output_file)
    #canviar instruments
    num_instruments = 10
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
    posList_1.text =  'CTD'
    posList_1.set ("codeListValue","130")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'fluorometers'
    posList_1.set ("codeListValue","113")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'dissolved gas sensors'
    posList_1.set ("codeListValue","351")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'salinity sensor'
    posList_1.set ("codeListValue","350")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'water temperature sensor'
    posList_1.set ("codeListValue","134")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'transmissometers'
    posList_1.set ("codeListValue","124")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'radiometers'
    posList_1.set ("codeListValue","122")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'altimeters'
    posList_1.set ("codeListValue","379")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'current profilers'
    posList_1.set ("codeListValue","115")

    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'cameras'
    posList_1.set ("codeListValue","311")
    posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Ultra short baseline positioning systems'
    posList_1.set ("codeListValue","POS26")    

    tree.write(output_file)


    """#canviar sensor segons el vaixell
    tree = etree.parse(input_file)
    posList_1 = tree.xpath("//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)[0]
    posList_1.text =  'Sea-Bird SBE 911plus CTD'
    posList_1.set ("codeListValue","TOOL0058")
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
