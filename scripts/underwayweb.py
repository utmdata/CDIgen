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
import copy, json
import csv
from flask import send_file
import logging
from logging.handlers import RotatingFileHandler 
#importem els scripts de cada cdi

def crear_carpeta (nombre_carpeta):
    try:
        # Intenta crear la carpeta
        os.mkdir(nombre_carpeta)
        print(f"La carpeta '{nombre_carpeta}' se ha creado correctamente.")
    except FileExistsError:
            # Si la carpeta ya existe, imprime un mensaje
            print(f"La carpeta '{nombre_carpeta}' ya existe.")


def get_country_code_by_label(label):
    with open("static/c32_countries.csv", encoding="latin1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["preflabel"].strip().lower() == label.strip().lower():
                return row["conceptid"]
    return "99"


def compose_org_name(name, alt_name):
    name = (name or "").strip()
    alt_name = (alt_name or "").strip()

    has_name = name not in ("", "N/A")
    has_alt_name = alt_name not in ("", "N/A")

    if has_name and has_alt_name and alt_name != name:
        return f"{name} ({alt_name})"
    if has_name:
        return name
    if has_alt_name:
        return alt_name
    return "N/A"


def set_xpath_text(tree, xpath, namespaces, value, code_list_value=None):
    nodes = tree.xpath(xpath, namespaces=namespaces)
    if not nodes:
        logging.warning(f"No XML nodes found for xpath: {xpath}")
        return 0

    for node in nodes:
        node.text = value
        if code_list_value is not None:
            node.set("codeListValue", code_list_value)

    return len(nodes)
            

def underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, data, valor_org, csr_code):
    # Handle CSR code
    
    if csr_code != "UNKNOWN":
        # Download and parse the XML file
        xml_url = "http://datahub.utm.csic.es/cdigen/static/csrCodeList.xml"
        response = requests.get(xml_url, verify=False)  # verify=False for self-signed certificates
        if response.status_code != 200:
            raise Exception(f"Failed to download CSR code list: {response.status_code}")
            
        root = etree.fromstring(response.content)

        # Search for the cruisename element
        for cruisename in root.findall(".//{http://www.opengis.net/gml}cruisename"):
            if cruisename.text == csr_code:
                description_csr = cruisename.getparent().find("{http://www.opengis.net/gml}description").text
                id_csr = cruisename.getparent().find("{http://www.opengis.net/gml}identifier").text
                break
        else:
            raise Exception(f"CSR code {csr_code} not found in the XML file.")
    else:
    
        id_csr = '2004 - Unknown(ZZ99)'
        description_csr = "20050002"

    print(f"CSR ID: {id_csr}")
    print(f"CSR Description: {description_csr}")

    # Load metadata from JSON
    json_path = os.path.join("static", "sparql.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("results", {}).get("bindings", [])
    matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

    if not matched:
        raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")
    
    # Extract the required fields
    org = matched.get("org", {}).get("value", "N/A")
    org_name = matched.get("name", {}).get("value", "N/A")
    notation = matched.get("notation", {}).get("value", "N/A")
    tel = matched.get("tel", {}).get("value", "N/A")
    alt_name = matched.get("altName", {}).get("value", "N/A")
    street = matched.get("street", {}).get("value", "N/A")
    codepostal = matched.get("codepostal", {}).get("value", "N/A")
    locality = matched.get("locality", {}).get("value", "N/A")
    country = matched.get("country", {}).get("value", "N/A")
    web = matched.get("web", {}).get("value", "N/A")
    email = matched.get("email", {}).get("value", "sdn-userdesk@seadatanet.org").replace("mailto:", "").replace("%40", "@")
    name = matched.get("name", {}).get("value", "N/A")

    org_name = compose_org_name(name, alt_name)

    print(f"Organization URI: {org}")
    print(f"Organization Name: {org_name}")
    print(f"Notation: {notation}")
    print(f"Telephone: {tel}")
    print(f"Alternative Name: {alt_name}")
    print(f"Street: {street}")
    print(f"Postal Code: {codepostal}")
    print(f"Locality: {locality}")
    print(f"Country: {country}")
    print(f"Web: {web}")
    print(f"Email: {email}")

    departure_country_code = get_country_code_by_label(country)

    if vessel_input == "sdg":
        vessel_mode = "Sarmiento"
        vessel_reduit='sdg' 
        vessel = "Sarmiento de Gamboa"
    elif vessel_input == "hes":
        vessel_mode ="Hesperides"
        vessel_reduit="hes"
        vessel = "Hespérides"
    elif vessel_input == "odb":
        vessel_mode = "Odon de Buen"
        vessel_reduit = "odb"
        vessel = "Odon de Buen"
    elif vessel_input == "gdc":
        vessel_mode = "Garcia del Cid"
        vessel_reduit = "gdc"
        vessel = "Garcia del Cid"
        
    dia= cruise_id[10:12]
    mes=cruise_id[8:10]
    any=cruise_id[4:8]
    short_date = any +"-"+ mes +"-"+ dia

    fila=0

    if path.exists("model_underway.txt"):
        remove("model_underway.txt")

    # Create the directory for the cruise
    nombre_carpeta = cruise_id
    crear_carpeta(nombre_carpeta)

    # Define the input and output XML file paths
    underway_general = cruise_id + "_underway.xml"
    underway_met = os.path.join(nombre_carpeta, f"{cruise_id}_met.xml")
    underway_ts = os.path.join(nombre_carpeta, f"{cruise_id}_ts.xml")
    underway_sbe = os.path.join(nombre_carpeta, f"{cruise_id}_sbe.xml")

    # Remove existing files if they exist
    if path.exists(underway_met):
        remove(underway_met)
    if path.exists(underway_ts):
        remove(underway_ts)
    if path.exists(underway_sbe):
        remove(underway_sbe)

    # Copy the template file to the new directory
    if not os.path.exists("model_underway.xml"):
        raise Exception("Template file 'model_underway.xml' does not exist.")
    shutil.copy("model_underway.xml", underway_general)
    print(underway_general)
    
    # Set input and output file paths
    input_file = underway_general
    input_url = f"http://datahub.utm.csic.es/ws/getTrack/GML/?id={vessel_input}{cruise_id[4:12]}&n=999"
    output_file = underway_general
    
    # Define the namespace
    namespace = {
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gml': 'http://www.opengis.net/gml',
        'gco': 'http://www.isotc211.org/2005/gco',
        'sdn': 'http://www.seadatanet.org',
        'gmx': 'http://www.isotc211.org/2005/gmx'
    }

    # Parse the XML and update the fields
    tree = etree.parse(input_file)

    # Add GML
    input_url = f"http://datahub.utm.csic.es/ws/getTrack/GML/?id={vessel_input}{cruise_id[4:12]}&n=999"
    posList = tree.xpath("//gml:posList[contains(text(), '-1 -1 -1 -1')]", namespaces=namespace)[0]
    posList.text = requests.get(input_url).text.strip()
    tree.write(output_file)
    
    # Add Bounding Box
    url_bbox = f"http://datahub.utm.csic.es/ws/getBBox/?id={vessel_input}{cruise_id[4:12]}"
    r = requests.get(url_bbox)
    coord = r.text[4:-2]
    posicio_primer_espai = coord.index(" ")
    posicio_coma = coord.index(",")
    w = coord[0:posicio_primer_espai]
    s = coord[posicio_primer_espai:posicio_coma].strip()
    coord_2 = coord[posicio_coma + 1:]
    posicio_segon_espai = coord_2.index(" ")
    e = coord_2[0:posicio_segon_espai].strip()
    n = coord_2[posicio_segon_espai:].strip()

    posList_w = tree.xpath("//gco:Decimal[contains(text(), '80.00')]", namespaces=namespace)[0]
    posList_w.text = w
    posList_s = tree.xpath("//gco:Decimal[contains(text(), '10.00')]", namespaces=namespace)[0]
    posList_s.text = s
    posList_e = tree.xpath("//gco:Decimal[contains(text(), '90.00')]", namespaces=namespace)[0]
    posList_e.text = e
    posList_n = tree.xpath("//gco:Decimal[contains(text(), '20.00')]", namespaces=namespace)[0]
    posList_n.text = n
    tree.write(output_file)

    #Afegir SHORT ID
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'SHORT_ID')]", namespaces=namespace)[0]
    posList.text = cruise_id
    tree.write(output_file)

    #afegim cruise name
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:CharacterString[contains(text(), 'CSR_CRUISE_NAME')]", namespaces=namespace)[0]
    posList.text = cruise_name
    tree.write(output_file)

    #afegim short date
    data=any +"-" + mes + "-"+ dia
    tree = etree.parse(input_file)
    posList = tree.xpath("//gco:Date[contains(text(), '2023-05-04')]", namespaces=namespace)[0]
    posList.text = data
    tree.write(output_file)
    
    #afegim data inicial
    hora_inicial = date_inicial[11:]
    begin_position = any + "-"+ mes + "-" + dia + "T" + hora_inicial
    tree = etree.parse(input_file)
    posList = tree.xpath("//gml:beginPosition[contains(text(), '2023-01-01T00:00:00')]", namespaces=namespace)[0]
    posList.text = begin_position
    tree.write(output_file)
    
    #afegim data final
    hora_final = date_final[11:]
    data_final = date_final[:10]
    dia_final= data_final[0:2]
    mes_final=data_final[3:5]
    any_final=data_final[6:10]

    final_position = any_final + "-"+ mes_final + "-" + dia_final + "T" + hora_final
    tree = etree.parse(input_file)
    posList = tree.xpath("//gml:endPosition[contains(text(), '2023-01-02T00:00:00')]", namespaces=namespace)[0]
    posList.text = final_position
    tree.write(output_file)

    tree = etree.parse(input_file)
    set_xpath_text(
        tree,
        "//gmd:CI_ResponsibleParty/gmd:organisationName/sdn:SDN_EDMOCode",
        namespace,
        org_name,
        notation,
    )
    set_xpath_text(
        tree,
        "//gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString",
        namespace,
        street,
    )
    set_xpath_text(
        tree,
        "//gmd:CI_Address/gmd:city/gco:CharacterString",
        namespace,
        locality,
    )
    set_xpath_text(
        tree,
        "//gmd:CI_Address/gmd:country/sdn:SDN_CountryCode",
        namespace,
        country,
        departure_country_code,
    )
    set_xpath_text(
        tree,
        "//gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString",
        namespace,
        email,
    )
    tree.write(output_file)

    #afegim csrcodelist
    tree = etree.parse(input_file)
    posList = tree.xpath("//sdn:SDN_CSRCode[contains(text(), '2004 - Unknown(ZZ99)')]", namespaces=namespace)[0]
    posList.text = description_csr

    posList.set ("codeListValue",id_csr)
    tree.write(output_file)