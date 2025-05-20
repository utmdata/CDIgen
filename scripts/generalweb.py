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
import logging, json
#importem els scripts de cada cdi

def crear_carpeta(nombre_carpeta):
    try:
        os.mkdir(nombre_carpeta)
        logging.info(f"Created folder '{nombre_carpeta}'")
    except FileExistsError:
        logging.info(f"Folder '{nombre_carpeta}' already exists")
    except Exception as e:
        logging.error(f"Error creating folder '{nombre_carpeta}': {str(e)}")
        raise

def process_xml_file(input_file, output_file, namespace, updates):
    try:
        tree = etree.parse(input_file)
        for xpath, value in updates:
            try:
                posList = tree.xpath(xpath, namespaces=namespace)[0]
                if isinstance(value, tuple):
                    posList.text = value[0]
                    posList.set("codeListValue", value[1])
                else: 
                    posList.text = value
            except IndexError as e:
                logging.error(f"Error finding element with xpath {xpath}: {str(e)}")
                raise
            except Exception as e:
                logging.error(f"Error updating element with xpath {xpath}: {str(e)}")
                raise
        tree.write(output_file)
        logging.info(f"Successfully updated XML file: {output_file}")
    except Exception as e:
        logging.error(f"Error processing XML file: {str(e)}")
        raise

def get_organization_info(valor_org):
    try:
        # Load metadata from JSON file
        json_path = os.path.join("static", "csv", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Find the organization data using the `valor_org` URI
        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

        # Extract the required fields
        org_info = {
            'org': matched.get("org", {}).get("value", "N/A"),
            'org_name': matched.get("orgName", {}).get("value", "N/A"),
            'notation': matched.get("notation", {}).get("value", "N/A"),
            'street': matched.get("street", {}).get("value", "N/A"),
            'country': matched.get("country", {}).get("value", "N/A")
        }
        
        logging.info(f"Organization Info: {org_info}")
        return org_info
    except Exception as e:
        logging.error(f"Error getting organization info from JSON: {str(e)}")
        raise

def get_organization_email(valor_org):
    try:
        # Load metadata from JSON file
        json_path = os.path.join("static", "csv", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Find the organization data using the `valor_org` URI
        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            logging.info("No email found, using default email")
            return "sdn-userdesk@seadatanet.org"

        email = matched.get("email", {}).get("value", "N/A")
        return email.replace("mailto:", "").replace("%40", "@")
    except Exception as e:
        logging.error(f"Error getting organization email from JSON: {str(e)}")
        raise

def get_csr_info(csr_code):
    try:
        if csr_code == "UNKNOWN":
            return {
                'id_csr': '2004 - Unknown(ZZ99)',
                'description_csr': "20050002"
            }

        # Download the XML file first
        xml_url = "https://161.111.137.92:8001/static/csrCodeList.xml"
        response = requests.get(xml_url, verify=False)  # verify=False for self-signed certificates
        if response.status_code != 200:
            raise Exception(f"Failed to download CSR code list: {response.status_code}")
            
        # Parse the XML content
        root = etree.fromstring(response.content)
        
        # Find the matching cruisename
        for cruisename in root.findall(".//{http://www.opengis.net/gml}cruisename"):
            if cruisename.text == csr_code:
                parent = cruisename.getparent()
                return {
                    'id_csr': parent.find("{http://www.opengis.net/gml}identifier").text,
                    'description_csr': parent.find("{http://www.opengis.net/gml}description").text
                }
        
        raise Exception(f"CSR code {csr_code} not found")
    except Exception as e:
        logging.error(f"Error getting CSR info: {str(e)}")
        raise

def general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final): #copia sense_sensor
        # Handle CSR code
        print(csr_code)
        if csr_code != "UNKNOWN":
            xml_url = "https://161.111.137.92:8001/static/csrCodeList.xml"
            response = requests.get(xml_url, verify=False)
            if response.status_code != 200:
                raise Exception(f"Failed to download CSR code list: {response.status_code}")
            root = etree.fromstring(response.content)
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
        json_path = os.path.join("static", "csv", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

        # Extract metadata
        org = matched.get("org", {}).get("value", "N/A")
        org_name = matched.get("orgName", {}).get("value", "N/A")
        notation = matched.get("notation", {}).get("value", "N/A")
        tel = matched.get("tel", {}).get("value", "N/A")
        alt_name = matched.get("altName", {}).get("value", "N/A")
        street = matched.get("street", {}).get("value", "N/A")
        codepostal = matched.get("codepostal", {}).get("value", "N/A")
        locality = matched.get("locality", {}).get("value", "N/A")
        country = matched.get("country", {}).get("value", "N/A")
        web = matched.get("web", {}).get("value", "N/A")
        email = matched.get("email", {}).get("value", "sdn-userdesk@seadatanet.org").replace("mailto:", "").replace("%40", "@")

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


        # Asignar información del buque
        if vessel_input == "sdg":
            vessel = "Sarmiento de Gamboa"
            vessel_mode = "Sarmiento"
            vessel_reduit = "sdg"
        elif vessel_input == "hes":
            vessel = "Hespérides"
            vessel_mode = "Hesperides"
            vessel_reduit = "hes"
        else:
            raise ValueError(f"Invalid vessel_input: {vessel_input}")

        # Extraer fecha
        dia = cruise_id[10:12]
        mes = cruise_id[8:10]
        any = cruise_id[4:8]
        short_date = f"{any}-{mes}-{dia}"

        # Crear carpeta y preparar archivo CDI individual
        cdi_individual = f"{cruise_id}_cdi.xml"
        nombre_carpeta = cruise_id
        crear_carpeta(nombre_carpeta)

        # Copiar plantilla XML
        if path.exists("model_cdi_sensegml.txt"):
            remove("model_cdi_sensegml.txt")
        shutil.copy("model_cdi_sensegml.xml", cdi_individual)
        logging.info(f"Created CDI file: {cdi_individual}")

          #Posem la url perque trobi el gml i l'enganxi en el xml
        input_file = cdi_individual
        input_url = 'http://datahub.utm.csic.es/ws/getTrack/GML/?id=' + vessel_input + cruise_id[4:12] + '&n=999'
        output_file = cdi_individual

        # Definir namespaces
        namespace = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gml': 'http://www.opengis.net/gml',
            'gco': 'http://www.isotc211.org/2005/gco',
            'sdn': 'http://www.seadatanet.org',
            'gmx': 'http://www.isotc211.org/2005/gmx'
        }

        # GML y BBOX
        #gml_result, bbox = extract_gml_and_bbox(ruta_csv)
        #logging.info(f"GML result: {gml_result}")
        #logging.info(f"BBOX: {bbox}")

        # Reemplazos en el XML
        #afegim short id
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'SHORT_ID')]", namespaces=namespace)[0]
        posList.text = cruise_id
        tree.write(output_file)

        #afegim csr id
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

        #afegim org_name
        tree = etree.parse(input_file)
        posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
        posList.text = org_name
        posList.set ("codeListValue",notation)
        tree.write(output_file)

        #afegim org_name
        tree = etree.parse(input_file)
        posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
        posList.text = org_name
        posList.set ("codeListValue",notation)
        tree.write(output_file)
        
        #afegim street
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)[0]
        posList.text = street
        tree.write(output_file)
        #afegim street
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)[0]
        posList.text = street
        tree.write(output_file)
        #afegim city
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)[0]
        posList.text = country
        tree.write(output_file)

        #afegim city
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)[0]
        posList.text = country
        tree.write(output_file)

        #afegim email
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)[0]
        posList.text = email
        tree.write(output_file)
        #afegim email
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)[0]
        posList.text = email
        tree.write(output_file)

        #afegim csrcodelist
        tree = etree.parse(input_file)
        posList = tree.xpath("//sdn:SDN_CSRCode[contains(text(), '2004 - Unknown(ZZ99)')]", namespaces=namespace)[0]
        posList.text = description_csr
        posList.set ("codeListValue",id_csr)
        tree.write(output_file)

        print("fet generalweb----------------") 



def general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final):
        # Handle CSR code
        print(csr_code)
        if csr_code != "UNKNOWN":
            xml_url = "https://161.111.137.92:8001/static/csrCodeList.xml"
            response = requests.get(xml_url, verify=False)
            if response.status_code != 200:
                raise Exception(f"Failed to download CSR code list: {response.status_code}")
            root = etree.fromstring(response.content)
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
        json_path = os.path.join("static", "csv", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

        # Extract metadata
        org = matched.get("org", {}).get("value", "N/A")
        org_name = matched.get("orgName", {}).get("value", "N/A")
        notation = matched.get("notation", {}).get("value", "N/A")
        tel = matched.get("tel", {}).get("value", "N/A")
        alt_name = matched.get("altName", {}).get("value", "N/A")
        street = matched.get("street", {}).get("value", "N/A")
        codepostal = matched.get("codepostal", {}).get("value", "N/A")
        locality = matched.get("locality", {}).get("value", "N/A")
        country = matched.get("country", {}).get("value", "N/A")
        web = matched.get("web", {}).get("value", "N/A")
        email = matched.get("email", {}).get("value", "sdn-userdesk@seadatanet.org").replace("mailto:", "").replace("%40", "@")

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


        # Asignar información del buque
        if vessel_input == "sdg":
            vessel = "Sarmiento de Gamboa"
            vessel_mode = "Sarmiento"
            vessel_reduit = "sdg"
        elif vessel_input == "hes":
            vessel = "Hespérides"
            vessel_mode = "Hesperides"
            vessel_reduit = "hes"
        else:
            raise ValueError(f"Invalid vessel_input: {vessel_input}")

        # Extraer fecha
        dia = cruise_id[10:12]
        mes = cruise_id[8:10]
        any = cruise_id[4:8]
        short_date = f"{any}-{mes}-{dia}"

        # Crear carpeta y preparar archivo CDI individual
        cdi_individual = f"{cruise_id}_cdi.xml"
        nombre_carpeta = cruise_id
        crear_carpeta(nombre_carpeta)

        # Copiar plantilla XML
        if path.exists("model_cdi_sensegml_sensesensor.txt"):
            remove("model_cdi_sensegml_sensesensor.txt")
        shutil.copy("model_cdi_sensegml_sensesensor.xml", cdi_individual)
        logging.info(f"Created CDI file: {cdi_individual}")

          #Posem la url perque trobi el gml i l'enganxi en el xml
        input_file = cdi_individual
        input_url = 'http://datahub.utm.csic.es/ws/getTrack/GML/?id=' + vessel_input + cruise_id[4:12] + '&n=999'
        output_file = cdi_individual

        # Definir namespaces
        namespace = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gml': 'http://www.opengis.net/gml',
            'gco': 'http://www.isotc211.org/2005/gco',
            'sdn': 'http://www.seadatanet.org',
            'gmx': 'http://www.isotc211.org/2005/gmx'
        }

        # GML y BBOX
        #gml_result, bbox = extract_gml_and_bbox(ruta_csv)
        #logging.info(f"GML result: {gml_result}")
        #logging.info(f"BBOX: {bbox}")

        # Reemplazos en el XML
        #afegim short id
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'SHORT_ID')]", namespaces=namespace)[0]
        posList.text = cruise_id
        tree.write(output_file)

        #afegim csr id
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

        #afegim org_name
        tree = etree.parse(input_file)
        posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
        posList.text = org_name
        posList.set ("codeListValue",notation)
        tree.write(output_file)
        
        #afegim org_name
        tree = etree.parse(input_file)
        posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
        posList.text = org_name
        posList.set ("codeListValue",notation)
        tree.write(output_file)
        
        #afegim street
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)[0]
        posList.text = street
        tree.write(output_file)
        #afegim street
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)[0]
        posList.text = street
        tree.write(output_file)
        #afegim city
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)[0]
        posList.text = country
        tree.write(output_file)

        #afegim city
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)[0]
        posList.text = country
        tree.write(output_file)

        #afegim email
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)[0]
        posList.text = email
        tree.write(output_file)
        #afegim email
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)[0]
        posList.text = email
        tree.write(output_file)

        #afegim csrcodelist
        tree = etree.parse(input_file)
        posList = tree.xpath("//sdn:SDN_CSRCode[contains(text(), '2004 - Unknown(ZZ99)')]", namespaces=namespace)[0]
        posList.text = description_csr
        posList.set ("codeListValue",id_csr)
        tree.write(output_file)