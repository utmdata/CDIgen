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
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Definim el namespace perquè el trobi en el XML
def funcio_mbe (cruise_id, cruise_name, date_inicial, date_final, vessel_input):
    namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx',
      'xlink': 'http://www.w3.org/1999/xlink'
  }

    underway_general_org = cruise_id + "_underway_org.xml"
    underway_general_default = cruise_id + "_underway.xml"
    underway_general = underway_general_org if path.exists(underway_general_org) else underway_general_default
    cdi =cruise_id + "/" + cruise_id + "_mbe.xml"
    
    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
        instrument= "Atlas Hydrographic Hydrosweep DS multibeam echo sounder"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"
        instrument = "Kongsberg EM 122 multibeam echosounder"
    elif vessel_input == "odb":
        vessel = "Odón de Buen"
        vessel_mode = "Odón"
        vessel_reduit = "odb"
        vessel_mayus = "ODON DE BUEN"
        vessel_code = "29OD"
        instrument = "Kongsberg EM 712 multibeam echosounder" #També podria ser la 124
    elif vessel_input == "gdc":
        vessel = "García del Cid"
        vessel_mode = "García"
        vessel_reduit = "gdc"
        vessel_mayus = "GARCÍA DEL CID"
        vessel_code = "29GD"
        instrument = "Elac Seabeam 1050D echo-sounder" #

    shutil.copy(underway_general, cdi)
    input_file= cdi
    output_file= cdi

    logger.info(f"MBE Processing - Vessel: {vessel_input}, Cruise: {cruise_id}")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")

    #afegir dataset id (ho fem tres cops perque s'ha de canviar tres vegades)
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#1
    posList.text ="urn:SDN:CDI:LOCAL:" + cruise_id + "_mbe"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#2
    posList.text = cruise_id + "_mbe"
    tree.write(output_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ID')]", namespaces=namespace)[0]#3
    posList.text ="urn:SDN:CDI:LOCAL:" + cruise_id + "_mbe"
    tree.write(output_file)

    #afegir dataset name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name + " multibeam data"
    tree.write(output_file)
    
    #afegir ABSTRACT
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'new_ABSTRACT')]", namespaces=namespace)[0]
    posList.text = "Multibeam data acquired on board the R/V "+ vessel + " with a "+ instrument +" during the "+cruise_name+" cruise."
    tree.write(output_file)

    #canviar paràmetres
    num_parametres = 3
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
    posList_1.text =  'Bathymetry and Elevation'
    posList_1.set ("codeListValue","MBAN")
    posList_2 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_2.text =  'Sediment acoustics'
    posList_2.set ("codeListValue","SDAC")
    posList_3 = tree.xpath("//sdn:SDN_ParameterDiscoveryCode[contains(text(), 'Date and time')]", namespaces=namespace)[0]
    posList_3.text=  'Sound velocity and travel time in the water column'
    posList_3.set ("codeListValue","SVEL")
    tree.write(output_file)

    #canviar intruments 
    tree = etree.parse(input_file)
    device_codes = tree.xpath("//sdn:SDN_DeviceCategoryCode", namespaces=namespace)
    logger.debug(f"Found {len(device_codes)} SDN_DeviceCategoryCode elements")
    for i, elem in enumerate(device_codes):
        logger.debug(f"  [{i}] Current text: '{elem.text}'")
    
    try:
        posList_1 = tree.xpath("//sdn:SDN_DeviceCategoryCode[contains(text(), 'unknown')]", namespaces=namespace)
        logger.debug(f"Found {len(posList_1)} device codes with 'unknown' text")
        if posList_1:
            posList_1[0].text = 'multi-beam echosounders'
            posList_1[0].set("codeListValue", "157")
            logger.info(f"✓ Updated device category to 'multi-beam echosounders' with code '157'")
            tree.write(output_file)
        else:
            logger.warning("No device category codes with 'unknown' text found")
    except Exception as e:
        logger.error(f"Error updating device category code: {str(e)}")

    #canviar sensor
    tree = etree.parse(input_file)
    sensor_codes = tree.xpath(".//sdn:SDN_SeaVoxDeviceCatalogueCode", namespaces=namespace)
    logger.debug(f"Found {len(sensor_codes)} SDN_SeaVoxDeviceCatalogueCode elements")
    for i, elem in enumerate(sensor_codes):
        logger.debug(f"  [{i}] Current text: '{elem.text}'")
    
    try:
        if vessel_input == "hes":
            posList_1 = tree.xpath(".//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)
            logger.debug(f"Looking for sensor with 'unknown' for vessel 'hes': Found {len(posList_1)}")
            if posList_1:
                posList_1[0].text = 'Kongsberg EM 122 multibeam echosounder'
                posList_1[0].set("codeListValue", "TOOL0492")
                logger.info(f"✓ Updated sensor for HES to 'Kongsberg EM 122 multibeam echosounder'")
            else:
                logger.warning(f"No sensor codes with 'unknown' found for vessel {vessel_input}")
            tree.write(output_file)
            
        elif vessel_input == "sdg":
            posList_1 = tree.xpath(".//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)
            logger.debug(f"Looking for sensor with 'unknown' for vessel 'sdg': Found {len(posList_1)}")
            if posList_1:
                posList_1[0].text = 'Atlas Hydrographic Hydrosweep DS multibeam echo sounder'
                posList_1[0].set("codeListValue", "TOOL0911")
                logger.info(f"✓ Updated sensor for SDG to 'Atlas Hydrographic Hydrosweep DS multibeam echo sounder'")
            else:
                logger.warning(f"No sensor codes with 'unknown' found for vessel {vessel_input}")
            tree.write(output_file)
            
        elif vessel_input == "odb":
            posList_1 = tree.xpath(".//sdn:SDN_SeaVoxDeviceCatalogueCode[contains(text(), 'unknown')]", namespaces=namespace)
            logger.debug(f"Looking for sensor with 'unknown' for vessel 'odb': Found {len(posList_1)}")
            if posList_1:
                posList_1[0].text = 'Kongsberg EM 712 multibeam echosounder'
                posList_1[0].set("codeListValue", "TOOL1601")
                logger.info(f"✓ Updated sensor for ODB to 'Kongsberg EM 712 multibeam echosounder'")
            else:
                logger.warning(f"No sensor codes with 'unknown' found for vessel {vessel_input}")
            tree.write(output_file)
    except Exception as e:
        logger.error(f"Error updating sensor for vessel {vessel_input}: {str(e)}")

    #canviar llicencia
    tree = etree.parse(input_file)
    try:
        posList_1 = tree.xpath(".//gmx:Anchor[contains(text(), 'Creative Commons Attribution 4.0 International')]", namespaces=namespace)
        if not posList_1:
            posList_1 = tree.xpath(".//gmx:Anchor", namespaces=namespace)
        if posList_1:
            posList_1[0].text = 'by negotiation'
            posList_1[0].set("{http://www.w3.org/1999/xlink}href", "https://www.seadatanet.org/urnurl/SDN:L08::RS")
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        print(f"Error updating license: {str(e)}")

    #canviar data format
    tree = etree.parse(input_file)
    try:
        posList_1 = tree.xpath(".//sdn:SDN_FormatNameCode[contains(text(), 'Ocean Data View ASCII input')]", namespaces=namespace)
        if not posList_1:
            posList_1 = tree.xpath(".//sdn:SDN_FormatNameCode", namespaces=namespace)
        if posList_1:
            posList_1[0].text = 'Climate and Forecast NetCDF'
            posList_1[0].set("codeListValue", "CF")
            tree.write(output_file)
    except Exception as e:
        print(f"Error updating data format: {str(e)}")

    #canviar versio del data format
    tree = etree.parse(input_file)
    try:
        posList_1 = tree.xpath(".//gco:CharacterString[contains(text(), '0.4')]", namespaces=namespace)
        if posList_1:
            posList_1[0].text = '3.5'
            tree.write(output_file)
    except Exception as e:
        print(f"Error updating format version: {str(e)}")

    # Verification: Check what was actually set in the final XML
    logger.info("=" * 60)
    logger.info("MBE FINAL VERIFICATION")
    logger.info("=" * 60)
    
    tree = etree.parse(output_file)
    
    # Check device category
    device_cats = tree.xpath("//sdn:SDN_DeviceCategoryCode/text()", namespaces=namespace)
    logger.info(f"Device Category Codes: {device_cats}")
    
    # Check sensors
    sensors = tree.xpath(".//sdn:SDN_SeaVoxDeviceCatalogueCode/text()", namespaces=namespace)
    logger.info(f"Sensor Codes: {sensors}")
    
    # Check organization
    org_codes = tree.xpath("//sdn:SDN_EDMOCode/text()", namespaces=namespace)
    logger.info(f"Organization Codes: {org_codes}")
    
    logger.info("=" * 60)
